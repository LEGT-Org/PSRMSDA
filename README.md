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
| Package Manager | uv |
| AI Integration | Groq LLM API |
| API Client | Python AsyncGroq |

## Project Structure

```text
PSRMSDA/
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── Backend source code
├── frontend/
│   └── Frontend source code
├── README.md
└── .gitignore
```

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

This command installs the dependencies defined in `pyproject.toml` and uses `uv.lock` when available.

Configure the required backend environment variables, including the database connection settings and Groq API credentials, according to the project's configuration.

### 3. Database Setup

1. Start your MySQL server.
2. Create the required project database.
3. Configure the database connection settings in the backend environment file.
4. Run the database initialization or migration process used by the project.

### 4. Frontend Setup

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

Navigate to the backend directory:

```bash
cd backend
```

Start the FastAPI development server using uv:

```bash
uv run uvicorn app.main:app --reload
```

Replace `<MODULE_NAME>` with the actual Python module containing the FastAPI application.

### Frontend

Navigate to the frontend directory:

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

**Course:** SIA301 – System Integration and Architecture

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
