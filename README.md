# 📊 Business Analytics API

A backend REST API built with **FastAPI** for managing business sales data and providing analytics.

The project demonstrates practical backend development concepts including REST APIs, CRUD operations, authentication, authorization, database management, SQLAlchemy, password hashing, JWT-based authentication, and analytics using aggregated sales data.

---

## 🚀 Tech Stack & Core Concepts

* **Framework:** Python · FastAPI · Pydantic · Uvicorn
* **Database:** SQLite · SQLAlchemy (ORM)
* **Security:** JWT (PyJWT) · OAuth2 Password Bearer · Argon2 Hashing
* **Analytics:** SQL Aggregations · SQLAlchemy

---

##  ✨ Key Features

The Business Analytics API allows authenticated users to manage their sales records and retrieve business insights from their data.

### Key Features

-  JWT authentication with OAuth2
-  Role-based authorization (`user` / `admin`)
-  Sales CRUD with user ownership
-  Revenue, product, category, and summary analytics
-  SQLAlchemy + SQLite
-  Argon2 password hashing
-  Router / Service layer architecture
-  Interactive Swagger/OpenAPI documentation

--- 

## 📁 Project Structure

```text
business-analytics-api/
│
├── app/
│   ├── main.py
│   │
│   ├── config.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── sale.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── sale.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── sales.py
│   │   └── analytics.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── users_service.py
│   │   └── analytics_service.py
|   |   └── sales_service.py
│   │
│   └── dependencies/
│       └── auth_dependencies.py
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md

```
---

## 🛠️ How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/KaziShoubo/business-analytics-api.git
cd business-analytics-api
```

### 2. Create a Virtual Environment
Create a Python virtual environment:
```bash
python -m venv venv
```

Activate it on **Windows**:
```bash
venv\Scripts\activate
```

Activate it on **macOS / Linux**:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root. The actual `.env` file is intentionally excluded from GitHub for security reasons. You can use `.env.example` as a template.

Add your JWT secret key inside the file:
```text
SECRET_KEY=your-secret-key-here
```

### 5. Start the FastAPI Server
Run the application with Uvicorn:
```bash
uvicorn app.main:app --reload
```
The API will be available at: `http://127.0.0.1:8000`

---

## 📖 API Documentation

FastAPI automatically provides interactive API documentation once the server is running:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

*Note: Swagger UI can be used directly to register users, authenticate with JWT, create and manage sales, and test the analytics endpoints.*

---

## 📑 API Endpoints

### Authentication

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | Authenticate user and receive JWT |

### Users

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/users/` | Register a new user |
| `POST` | `/api/v1/users/admin` | Create an admin user |
| `GET` | `/api/v1/users/` | Retrieve users (**admin only**) |

### Sales

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/sales/` | Create a sale |
| `GET` | `/api/v1/sales/` | Retrieve user's sales |
| `GET` | `/api/v1/sales/{sale_id}` | Retrieve a specific sale |
| `PUT` | `/api/v1/sales/{sale_id}` | Update a sale |
| `DELETE` | `/api/v1/sales/{sale_id}` | Delete a sale |

### Analytics

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/analytics/revenue` | Calculate total revenue |
| `GET` | `/api/v1/analytics/products` | Analyze product performance |
| `GET` | `/api/v1/analytics/categories` | Analyze category performance |
| `GET` | `/api/v1/analytics/summary` | Return overall business summary |

---

## 🔄 Basic Usage Flow

A typical workflow for interacting with the application:
1. **Register a user** using `POST /api/v1/users/`
2. **Log in** using `POST /api/v1/auth/login`
3. **Copy** the returned JWT access token.
4. Click **Authorize** in Swagger UI.
5. Enter the **Bearer token**.
6. **Create sales** using `POST /api/v1/sales/`
7. **Retrieve and manage** sales records.
8. Use the **analytics endpoints** to analyze revenue, products, categories, and overall business performance.

---

## 🏗️ Architecture

The project follows a layered architecture to keep the application easy to maintain, test, and extend:

```text
Client
  ↓
FastAPI Router
  ↓
Service Layer
  ↓
SQLAlchemy
  ↓
SQLite Database
```

### Component Responsibilities
* **Routers:** Handle HTTP requests and responses.
* **Services:** Contain core business logic.
* **Schemas:** Validate API input and output payloads (Pydantic).
* **Models:** Define structural database tables.
* **Dependencies:** Handle authentication, authorization, and shared resource injection.
* **Database:** Manage SQLAlchemy sessions and SQLite file lifecycles.

---

## 🔒 Authentication & Security

The project implements several backend security practices:
* **JWT-Based Authentication:** Uses secure OAuth2 password bearer flow tokens.
* **Password Hashing:** Passwords are securely hashed using **Argon2** before database storage.
* **Role-Based Authorization (RBAC):**
  * `user`: Can manage their own sales records and access their own analytics.
  * `admin`: Has additional administrative permissions, including user management.
* **User-Specific Resource Ownership:** Sales records are tightly associated with the authenticated creator, preventing cross-user data tampering or unauthorized access.
* **Configuration Safety:** Critical application values use environment variables; the `.env` file is intentionally excluded from version control tracking.

---

## 🗄️ Database Configuration

The project utilizes **SQLite** coupled with **SQLAlchemy**. 
* The SQLite database file (`business_analytics.db`) initializes automatically when the application boots up.
* No separate external database server installation is required.

---

## 🚀 Future Improvements
* [ ] Full automated unit and integration test coverage.
* [ ] Pagination and filtering configurations for sales records.
* [ ] Date-range parameter controls for custom analytics window parsing.
* [ ] Native PostgreSQL engine configuration switch support.
* [ ] Production Docker deployment files (`Dockerfile` & `docker-compose.yml`).
* [ ] Alembic database migrations pipeline setup.
* [ ] GitHub Actions CI/CD automated validation workflow.
* [ ] Advanced frontend interactive business dashboards.

---

## 👤 Author

**Kazi Shoubo**  
*Master of Science — Information Systems Management*  
Technical University of Berlin  