# 📊 Personal Finance Management API

## 📌 Basic Information

- **Name:** Personal Finance Management API
- **Technologies:** FastAPI, SQLite/PostgreSQL, JWT
- **Purpose:** Manage income, expenses, and financial summaries with secure authentication.

---

## 🚀 Quick Start

```bash
git clone [https://github.com/KevDhev/personal-finance-api.git]
cd personal-finance-api
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
fastapi dev app/main.py
```

---

## 🔐 Authentication

### Register

`POST /register`  
**Body:**

```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

### Login

`POST /login`  
**Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

---

## 💰 Main Endpoints

| Method | Route                | Description                        |
| ------ | -------------------- | ---------------------------------- |
| POST   | `/movements/`        | Create a movement (income/expense) |
| GET    | `/movements/`        | List movements (optional filters)  |
| GET    | `/movements/{id}`    | Get a movement by ID               |
| PUT    | `/movements/{id}`    | Update a movement                  |
| DELETE | `/movements/{id}`    | Delete a movement                  |
| GET    | `/movements/summary` | Financial summary (totals/balance) |

---

## 🔄 Advanced Filters (Query Parameters)

Example for `GET /movements/`:

```
/movements/?start_date=2025-01-01&end_date=2025-12-31&movement_type=income&skip=0&limit=10
```

**Supported parameters:**

- `start_date` / `end_date`: Filter by date range
- `movement_type`: `income` or `expense`
- `skip` / `limit`: Pagination

---

## 📦 Key Schemas

### Movement

```python
amount: float         # > 0
type: str             # "income" or "expense"
description: Optional[str]
date: Optional[datetime]
```

### User

```python
username: str         # 3-50 characters
email: str            # valid format
password: str         # minimum 8 characters
```

---

## 🔧 Key Dependencies

- **FastAPI** - Main web framework
- **SQLAlchemy** - ORM for database interaction
- **Pydantic** - Data validation
- **python-jose** - JWT authentication
- **bcrypt** - Password hashing
- **uvicorn** - ASGI server

---

## ⚠️ Minimum Requirements

- Python **3.10+** (for support of `|` in types and `model_dump` from Pydantic v2)
- Essential libraries listed in `requirements.txt`

---

## 📂 Project Structure

```
app/
├── auth/
│   ├── dependencies.py   # JWT logic
│   ├── schemas.py        # Auth schemas
│   |── crud.py           # Auth operations
│   └── router.py         # Auth endpoints
├── models/
│   ├── user.py           # User model
│   └── movement.py       # Movement model
├── routers/
│   └── movement.py       # Movement endpoints
├── schemas/
│   |── movement.py       # Movement schemas
│   |── summary.py        # Summary schemas
│   └── user.py           # User schemas
├── crud.py               # Database operations
├── database.py           # SQLAlchemy config
└── main.py               # FastAPI app
```

---

## ⚙️ Initial Setup

### Environment Variables (.env)

```
SECRET_KEY=generated_with_openssl_rand_hex_32
DATABASE_URL=sqlite:///./prod.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Installation

```
pip install -r requirements.txt
```

### Run the App

```
fastapi dev app/main.py
```

---

## 📚 API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📜 License

MIT License - Free to use and modify.
