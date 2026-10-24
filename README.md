# Sieve — High-Throughput Candidate Ingestion & Workflow Engine

A scalable, asynchronous backend engine built with **FastAPI**, **PostgreSQL**, **Redis / ARQ**, and **Google Gemini** for high-volume candidate document ingestion, structured resume parsing, and multi-stage qualification workflows.

---

## 🏗️ Architecture Overview

The system is built with a domain-driven, modular architecture designed for high-concurrency ingestion and background task orchestration:

```
Sieve Backend
│
├── app/
│   ├── core/                  # Core configurations, async database sessions, security & JWT
│   │   ├── config.py          # Pydantic v2 settings management
│   │   ├── database.py        # Async SQLAlchemy 2.0 engine + session factories
│   │   └── security.py        # Argon2 password hashing & JWT token life-cycle
│   │
│   ├── domains/               # Domain-driven modular services
│   │   ├── campaigns/         # Campaign orchestration, candidate state machines, screening models
│   │   ├── ingestion/         # Chunked pipeline for ZIP, PDF, DOCX, CSV parsing
│   │   ├── chat/              # Conversational agent runtime, Gemini tool-calling, session persistence
│   │   ├── agents/            # Agent presets, system prompts, and capability bindings
│   │   └── users/             # User authentication, profiles, and permission scoping
│   │
│   ├── integrations/          # External third-party integrations
│   │   └── ai/                # Gemini client wrappers, schema enforcement, retry mechanics
│   │
│   └── main.py                # FastAPI application entrypoint, CORS, exception handlers
│
├── alembic/                   # Database versioning & schema migrations
└── tests/                     # Asynchronous Pytest suite with comprehensive domain coverage
```

---

## ⚡ Core Technical Features

### 1. Resilient Async Processing & Distributed Queue
* **ARQ + Redis Worker**: Decouples heavy LLM screening and document extraction from API latency, processing batches concurrently with automatic exponential backoff.
* **State Machine & Batch Tracking**: Atomic job progress tracking in Redis, enabling pausing, resuming, and progress polling across long-running ingestion batches.

### 2. High-Throughput Ingestion Pipeline
* **Multi-Format Document Parsing**: Streams and processes PDF, DOCX, and bulk CSV uploads with zero uncompressed disk bloat.
* **Zip Bomb & Memory Protection**: Configurable strict validation limits (`ZIP_MAX_UNCOMPRESSED_BYTES`, `ZIP_MAX_RATIO`, file count guards) to protect memory and worker resources.

### 3. Structured LLM Extraction & Screening
* **Deterministic Schemas**: Integrates Google Gemini (`gemini-2.0-flash`) using Pydantic structured output models to eliminate hallucinations during profile evaluation.
* **Intelligent Score Breakdown**: Evaluates candidate documents against configurable campaign criteria, generating match scores and unmatched field diagnostics.

### 4. Interactive Agent Chat with Tool Calling
* **Context-Aware Sessions**: Persists conversation history in PostgreSQL with token-aware summarization windows.
* **Backend Tool Calling**: Secure execution of domain tools within the chat context without granting arbitrary frontend execution privileges.

### 5. Multi-Stage Evaluation Funnel & Schema Design
* **Dual-Tier Screening Schema**: The relational database schema is structured for a multi-stage qualification pipeline:
  * `document_screenings`: Stores algorithmic extraction scores, matched qualification fields, and LLM rationale based on resumes.
  * `call_screenings`: Pre-architected schema to persist voice interview sessions, candidate call IDs, transcripts, audio recording references, and post-call evaluation metrics.
* **Candidate State Machine**: Tracks candidate lifecycle across distinct step states (`PENDING`, `IN_PROGRESS`, `COMPLETED`, `PAUSED`, `FAILED`), enabling granular batch control and workflow resumption.

---

## 🛠️ Tech Stack

* **Language & Framework**: Python 3.13, FastAPI (Async ASGI)
* **Database & ORM**: PostgreSQL, SQLAlchemy 2.0 (asyncpg), Alembic
* **Task Queue & Caching**: ARQ, Redis, hiredis
* **AI & Language Models**: Google Gemini (`google-genai`)
* **Storage**: AWS S3 (`boto3` / `aioboto3`)
* **Security & Auth**: JWT (HS256), Argon2 (`pwdlib`)
* **Testing**: Pytest, Pytest-AsyncIO, AsyncMock

---

## 🚀 Getting Started

### Prerequisites
* Python 3.13+
* PostgreSQL 15+
* Redis 7+

### 1. Environment Configuration
Clone the repository and copy the environment template:
```bash
cp env.example .env
```
Fill in your database credentials, Redis URL, AWS S3 keys, and Gemini API key.

### 2. Virtual Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 3. Database Migrations
Apply the latest schema migrations with Alembic:
```bash
alembic upgrade head
```

### 4. Running the Services

**Start the FastAPI Web Server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Start the ARQ Background Worker:**
```bash
python -m arq app.domains.campaigns.worker_entry.WorkerSettings
```

---

## 📖 API Documentation

Once the server is running, interactive API documentation is available at:
* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Running Automated Tests

Run the full async test suite using `pytest`:
```bash
pytest tests/ -v
```
All 32 test suites validate model schema integrity, authentication boundaries, worker state transitions, and file ingestion flows.

---

## 🔮 Future Scope & Extensibility Roadmap

* **AI Voice Screening Dispatcher**: 
  The database schema already includes the `call_screenings` table with fields for call sessions, transcripts, audio recordings, and match evaluation scores. Future releases will connect this stage to a headless voice AI provider (e.g. Retell / Vapi / LiveKit / Twilio) via an ARQ worker dispatch queue to conduct live telephone screenings with candidates who pass document evaluation.
* **ATS Webhook Integrations**: 
  Add bidirectional webhook endpoints for major Applicant Tracking Systems (e.g. Greenhouse, Lever, Workday) to trigger ingestion workflows upon new applicant submissions.
* **Distributed Multi-Tenant Rate Limiting**: 
  Introduce Redis token-bucket rate limiters per organization to ensure equitable resource sharing during simultaneous large-batch campaigns.

