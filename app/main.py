import httpx

from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.routers import orders

import os
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.routers.books import router as books_router
from app.database import Base, engine
from app.models import book


app = FastAPI(
    title="BookStore API",
    description="A Book Management REST API",
    version="1.0.0"
)
class VerificationRequest(BaseModel):
    token: str

# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    session_cookie="bookstore_session",
    same_site="lax",
    https_only=False,
    max_age=86400
)

# Frontend configuration
templates = Jinja2Templates(directory="frontend/templates")

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)


# Create database tables
Base.metadata.create_all(bind=engine)
app.include_router(
    books_router,
    prefix="/api/v1/books",
    tags=["Books"]
)

app.include_router(orders.router)

@app.get("/")
async def verification_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="verify.html",
        context={}
    )


@app.post("/verify-human")
async def verify_human(
    data: VerificationRequest,
    request: Request
):
    @app.get("/session-check")
    async def session_check(request: Request):
        return {
            "human_verified": request.session.get("human_verified", False),
            "session_exists": bool(request.session)
        }

    secret_key = os.getenv("TURNSTILE_SECRET_KEY")

    if not secret_key:
        raise HTTPException(
            status_code=500,
            detail="Turnstile secret key is not configured."
        )

    # Ask Cloudflare to verify the token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": secret_key,
                "response": data.token
            }
        )

    result = response.json()

    if result.get("success"):
        request.session["human_verified"] = True
        return {"success": True, "message": "Verification successful"}

    return {
        "success": False,
        "message": "Verification failed. Please try again."
    }


@app.get("/store")
async def bookstore_page(request: Request):
    if not request.session.get("human_verified"):
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="bookstore.html",
        context={}
    )

