# 🏖️ Vacation SaaS API

A REST API built with **FastAPI** and **SQLAlchemy** to manage employee vacation calculations, balances, and requests — following **Mexican labor law** standards (Ley Federal del Trabajo).

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Examples](#api-examples)

---

## About the Project

This API allows companies to manage their employees' vacation entitlements end-to-end. It handles:

- **Seniority calculation** — tracks exact years of service per employee
- **Vacation balance** — accumulates entitled days across all completed years
- **Proportional days** — calculates partial days for employees with less than one year of service
- **Vacation bonus (prima vacacional)** — computes the bonus based on company policy and daily salary
- **Vacation requests** — create, approve, reject, and cancel requests with full audit trail
- **Custom policies** — each company can define its own vacation rules per seniority range

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic V2 |
| Database | SQLite (dev) / PostgreSQL (prod-ready) |
| Testing | Pytest + HTTPX |
| Language | Python 3.10+ |

---

## Project Structure

```
├── app/
│   ├── api/                        # Route handlers
│   │   ├── company_routes.py
│   │   ├── employee_routes.py
│   │   ├── vacation_policy_routes.py
│   │   └── vacation_request_routes.py
│   ├── core/                       # Pure business logic (no DB dependency)
│   │   ├── bonus.py                # Prima vacacional calculation
│   │   ├── proportional.py         # Proportional days for < 1 year
│   │   ├── seniority.py            # Years of service calculation
│   │   ├── service.py              # Bonus orchestration
│   │   └── vacation_policy.py      # Policy rule resolution
│   ├── models/                     # SQLAlchemy models
│   │   ├── company.py
│   │   ├── employee.py
│   │   ├── vacation_calculation.py
│   │   ├── vacation_policy.py
│   │   ├── vacation_policy_rule.py
│   │   ├── vacation_request.py
│   │   └── vacation_status.py
│   ├── schemas/                    # Pydantic schemas
│   │   ├── company.py
│   │   ├── employee.py
│   │   └── vacation_policy.py
│   ├── services/                   # Application services
│   │   ├── date_utils.py           # Business days calculation
│   │   ├── vacation_calculator.py  # Balance calculator (source of truth)
│   │   └── vacation_service.py     # Request state management
│   ├── database.py
│   └── main.py
├── tests/
│   ├── test_routes/
│   │   ├── test_company_routes.py
│   │   ├── test_employee_routes.py
│   │   └── test_vacation_request_routes.py
│   ├── conftest.py
│   ├── test_bonus.py
│   ├── test_proportional.py
│   ├── test_seniority.py
│   ├── test_vacation_calculator.py
│   └── test_vacation_policy.py
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PonchoGopa/vacation-saas-api.git
cd vacation-saas-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn app.main:app --reload
```

### 4. Open the interactive docs

```
http://localhost:8000/docs
```

### 5. Run the tests

```bash
python -m pytest tests/ -v
```

> 84 tests — all passing ✅

---

## API Examples

The recommended setup order is: **Company → Policy → Employee → Requests**

---

### 🏢 Create a Company

```http
POST /companies/
```

```json
{
    "name": "Acme Corp",
    "bonus_percentage": 0.25
}
```

**Response:**
```json
{
    "id": 1,
    "name": "Acme Corp",
    "bonus_percentage": 0.25
}
```

---

### 📋 Create a Vacation Policy

```http
POST /policies/
```

```json
{
    "company_id": 1,
    "name": "Standard Mexico Policy",
    "rules": [
        {"years_required": 1, "vacation_days": 12},
        {"years_required": 2, "vacation_days": 14},
        {"years_required": 3, "vacation_days": 16},
        {"years_required": 4, "vacation_days": 18},
        {"years_required": 5, "vacation_days": 20},
        {"years_required": 6, "vacation_days": 22},
        {"years_required": 11, "vacation_days": 24},
        {"years_required": 16, "vacation_days": 26},
        {"years_required": 21, "vacation_days": 28},
        {"years_required": 26, "vacation_days": 30}
    ]
}
```

---

### 👤 Create an Employee

```http
POST /employees/
```

```json
{
    "name": "Juan Pérez",
    "hire_date": "2022-01-01",
    "daily_salary": 500.00,
    "company_id": 1,
    "vacation_policy_id": 1
}
```

---

### 📊 Get Vacation Balance

```http
GET /employees/1/vacation-balance
```

**Response:**
```json
{
    "employee_id": 1,
    "years_of_service": 3,
    "total_days_entitled": 42,
    "days_used": 0,
    "remaining_balance": 42
}
```

> Total is cumulative: 12 (year 1) + 14 (year 2) + 16 (year 3) = **42 days**

---

### 💰 Get Vacation Bonus (Prima Vacacional)

```http
GET /employees/1/vacation-bonus
```

**Response:**
```json
{
    "employee_id": 1,
    "employee_name": "Juan Pérez",
    "daily_salary": 500.0,
    "bonus_percentage": 0.25,
    "years_completed": 3,
    "total_days_worked": 1095,
    "vacation_days": 42.0,
    "bonus_amount": 5250.0
}
```

---

### 🗓️ Create a Vacation Request

```http
POST /vacation-requests/?employee_id=1&start_date=2026-04-14&end_date=2026-04-18
```

**Response:**
```json
{
    "id": 1,
    "employee_id": 1,
    "start_date": "2026-04-14",
    "end_date": "2026-04-18",
    "days_requested": 5,
    "status": "pending"
}
```

**Business rules enforced:**
- Start date cannot be in the past
- Request must be submitted at least **5 days in advance**
- Cannot overlap with existing pending or approved requests
- Cannot exceed available balance

---

### ✅ Approve / ❌ Reject / 🚫 Cancel a Request

```http
PATCH /vacation-requests/1/approve?actor_id=1
PATCH /vacation-requests/1/reject?actor_id=1
PATCH /vacation-requests/1/cancel?actor_id=1
```

All actions are **audited** — timestamps and actor IDs are recorded automatically.

---

### 📬 List Pending Requests

```http
GET /vacation-requests/pending?skip=0&limit=10
```

**Response:**
```json
{
    "total": 1,
    "skip": 0,
    "limit": 10,
    "data": [...]
}
```