# PSRMSDA
### Parts and Service Request Management System with Diagnostic Analytics

A web-based information management system developed for **Lightyear Electrical Goods Trading (LEGT)** to improve service request management, equipment fault diagnosis, spare parts management, and inventory monitoring.

PSRMSDA integrates the **Groq LLM API** to provide AI-assisted equipment fault analysis. It processes technician-provided equipment information and fault descriptions to generate diagnostic hypotheses, recommended checks, Standard Operating Procedures (SOPs), and replacement component recommendations.

The system also cross-references recommended components with its internal spare parts inventory to identify possible matches and check stock availability.

## Features

- **Service Request Management** – Create and manage customer repair requests.
- **AI Diagnostic Analysis** – Generate equipment fault analysis using the Groq LLM API.
- **Spare Parts Recommendations** – Receive AI-generated component recommendations.
- **Inventory Management** – Manage spare parts records and stock quantities.
- **Inventory Matching** – Identify possible spare part matches and check availability.
- **Procurement Alerts** – Monitor spare parts requiring replenishment.
- **User Management** – Role-based access control.
- **Report Generation** – Generate system reports.
- **Email Notifications** – Support service-related email notifications.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Vue.js, TypeScript |
| Backend | Python, FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| Database Migration | Alembic |
| Package Manager | uv |
| AI Integration | Groq LLM API |
| API Client | Python AsyncGroq |

## Project Structure

```text
PSRMSDA/
├── backend/
│   ├── app/
│   ├── alembic/
│   │   └── versions/
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   └── Frontend source code
├── README.md
└── .gitignore
```

*Note: The directory structure above illustrates the expected project organization. Adjust it if your actual repository structure differs.*

## Prerequisites

Before running the application, ensure that the following are installed:

- Python
- uv (Python package and project manager)
- Node.js and npm
- MySQL Server
- A Groq API key

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/LEGT-Org/PSRMSDA.git
cd PSRMSDA
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Install the backend dependencies using uv:

```bash
uv sync
```

This command installs the dependencies defined in `pyproject.toml` and uses `uv.lock` to maintain the project's dependency versions.

#### Environment Configuration

Create a `.env` file using the provided `.env.example` as a reference.

Configure the required environment variables, including:

- MySQL database connection settings.
- Groq API key.
- Other environment variables required by the backend.

Use your own credentials and configuration values.

**Important:** Never commit or distribute your actual `.env` file or API credentials.

### 3. Database Setup and Migration

PSRMSDA uses MySQL for data storage and Alembic for database schema migration.

1. Start your MySQL server.
2. Create an empty database for PSRMSDA.
3. Configure the database connection settings in the backend `.env` file.
4. Ensure that the Alembic configuration points to the correct database.
5. Apply the database migrations.

Run the following command from the backend directory:

```bash
uv run alembic upgrade head
```

This applies all available migration revisions and updates the database schema to the latest version.

To check the current migration revision:

```bash
uv run alembic current
```

To view the available migration history:

```bash
uv run alembic history
```

### 4. Initial Administrator Account Setup

To create the initial administrator account, temporarily modify the administrator registration endpoint in:

`backend/app/modules/user/router.py`

**Original implementation:**

```python
@router.post(
    "/admin/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("15/minute")
def register(
    request: Request,
    data: UserCreate,
    service: UserService,
    current_user: AdminUser,
    _: ValidateCSRF
):
    return service.create_user(
        data=data,
        actor_id=current_user.id
    )
```

**Temporary implementation for initial administrator registration:**

```python
@router.post(
    "/admin/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("15/minute")
def register(
    request: Request,
    data: UserCreate,
    service: UserService,
    _: ValidateCSRF
):
    return service.create_user(
        data=data,
        actor_id=1
    )
```

The temporary modification removes the authenticated administrator requirement and uses `actor_id=1` when creating the initial administrator account.

**Create the administrator account through Swagger:**

1. Start the backend server.
2. Open the Swagger documentation:

   http://127.0.0.1:8000/docs

3. Locate the `POST /admin/register` endpoint.
4. Expand the endpoint and select **Try it out**.
5. Enter the required administrator account information according to the `UserCreate` schema.
6. Select **Execute** to create the administrator account.
7. Verify that the account was successfully created.

**Important:** The temporary implementation is intended only for local initial setup. After successfully creating the administrator account:

1. Restore the original implementation containing `current_user: AdminUser`.
2. Restart the backend server.
3. Go to your development database and users table to change user role from user to admin.
4. Log in using the newly created administrator account.

Do not deploy or expose the temporarily modified endpoint to a public network. Also, ensure that user ID `1` exists if the audit logic requires it as the actor.

### 5. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

## Running the Application

### Backend

Open a terminal and navigate to the backend directory:

```bash
cd backend
```

Start the FastAPI development server using uv:

```bash
uv run uvicorn app.main:app --reload
```

The FastAPI application will start using the application instance defined in `app.main`.

### Frontend

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Start the Vue.js development server:

```bash
npm run dev
```

Open the local URL displayed in the terminal to access the application.

## Groq LLM API Integration

PSRMSDA communicates with the Groq LLM API through the Python AsyncGroq client.

The integration follows an asynchronous request-response process:

1. The technician submits equipment information and fault descriptions through the frontend.
2. The FastAPI backend prepares the diagnostic prompts.
3. The backend sends the request to the Groq LLM API.
4. Groq returns a structured JSON diagnostic response.
5. Pydantic validates the returned response.
6. The backend processes the diagnostic information and searches the internal spare parts inventory.
7. The processed results are returned to the frontend.

## Security Notes

- Do not commit `.env` files or expose API keys, passwords, and access tokens.
- Configure your own environment variables before running the application.
- Do not include private customer information in publicly accessible project files.

## Developers

**Project:** Parts and Service Request Management System with Diagnostic Analytics (PSRMSDA)

**Organization:** Lightyear Electrical Goods Trading (LEGT)

**Course:** 

- SE2 – Software Engineering 2
- SIA301 – System Integration and Architecture

**Integration Partner:** Groq LLM API

**Developed by:** 

- Bocar, John Carlo G.
- Camunias, Karl Kobe D.
- Gutierrez, Michael S. Jr.
- Reyes, Vhonlenard G.

**System Integration Grouped:** 

- Alfonso, Cyril John
- Antolin, John Robertson
- Bocar, John Carlo
- Talay, Sean Menard

**Academic Institution:** City College of Calamba
