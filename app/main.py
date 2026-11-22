
from fastapi import FastAPI
from app.routers.books import router as books_router

app = FastAPI(
    title="BookStore API",
    description="A Book Management REST API",
    version="1.0.0"
)

@app.get("/")
async def home():
    return {"message": "Welcome to BookStore API"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Register Books Router
app.include_router(
    books_router,
    prefix="/api/v1/books",
    tags=["Books"]
)
