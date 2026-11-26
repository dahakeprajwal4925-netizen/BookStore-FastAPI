
# 📚 The Reading Room | BookStore API

A Book Management REST API built using Python and FastAPI, with a modern bookstore frontend.

## About

**The Reading Room** is a full-stack bookstore project designed to manage books, inventory, shopping carts, and orders.

The project combines a FastAPI backend with a PostgreSQL database and a simple frontend built using HTML, CSS, and JavaScript.

## Features

### 📖 Book Management
- Create, view, update, and delete books
- Search books by title and author
- Filter books by category
- Sort books
- PostgreSQL database integration

### 🛒 Shopping Cart
- Add books to cart
- Remove books from cart
- Increase and decrease quantities
- Stock-based quantity restrictions
- Cart persistence using localStorage
- Automatic total price calculation

### 📦 Order System
- SQLAlchemy Order model
- SQLAlchemy OrderItem model
- Order processing system (in development)

### 🎨 Frontend
- Responsive bookstore interface
- Book details modal
- Search and category filters
- Shopping cart interface
- Modern bookstore design

## Tech Stack

**Backend**
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic

**Database**
- PostgreSQL

**Frontend**
- HTML
- CSS
- JavaScript

**Tools**
- Git
- GitHub
- PyCharm

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/dahakeprajwal4925-netizen/BookStore-FastAPI.git
```

### 2. Navigate to the project directory

```bash
cd BookStore-FastAPI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root and configure your PostgreSQL database credentials.

### 7. Run the application

```bash
python -m uvicorn app.main:app --reload --port 8002
```

## API Documentation

Once the application is running:

- Swagger UI: http://127.0.0.1:8002/docs
- ReDoc: http://127.0.0.1:8002/redoc

## Project Status

🚧 Currently under development.

Implemented features include book management APIs, database integration, frontend catalogue, search and filtering, and shopping cart functionality.

Order processing, checkout, and stock management are currently being developed.

## Developer

**Prajwal Dahake**

GitHub: [dahakeprajwal4925-netizen](https://github.com/dahakeprajwal4925-netizen)
