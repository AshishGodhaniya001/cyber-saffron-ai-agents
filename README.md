# Cyber Saffron AI Agents

An open-source FastAPI multi-agent system that discovers business leads,
scores them with Gemini AI, manages prioritized tasks, and automates sales
outreach.

## Suggested GitHub repository

Repository name:

`cyber-saffron-ai-agents`

GitHub description:

`FastAPI multi-agent lead generation and sales automation system powered by Gemini AI, PostgreSQL, Redis, and Docker.`

Suggested topics:

`ai-agents`, `fastapi`, `gemini-ai`, `lead-generation`, `sales-automation`,
`python`, `postgresql`, `redis`, `docker`, `open-source`

## My role

**Project Maintainer and AI Agent Developer**

My responsibilities include:

- Finding and fixing application bugs.
- Improving agent orchestration and task processing.
- Maintaining the Lead Generation and Sales agents.
- Improving database reliability and duplicate prevention.
- Protecting API keys and other private configuration.
- Organizing the repository and removing unused files.
- Maintaining Docker and local development configuration.
- Testing application startup, API health, and Python syntax.
- Writing project documentation and progress reports.
- Reviewing and implementing future system improvements.

## How it works

The main workflow is:

`Discover leads → Save leads → Score with Gemini → Qualify leads → Create sales tasks → Send outreach email`

The system includes:

- **Master CTO Agent:** Coordinates and dispatches queued work.
- **LeadGen Agent:** Discovers, stores, scores, and qualifies leads.
- **Sales Agent:** Contacts qualified leads through the Resend email API.
- **Scheduler:** Runs lead discovery and orchestration automatically.
- **FastAPI:** Provides API endpoints and interactive documentation.
- **PostgreSQL:** Stores leads, tasks, and KPI events.
- **Redis:** Available for future durable task-queue improvements.

## Run with Docker

1. Copy `.env.example` to `.env`.
2. Add real API credentials only to `.env`.
3. Start the application:

```powershell
docker compose up --build
```

Open:

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Stop the application:

```powershell
docker compose down
```

## API endpoints

- `GET /health`
- `POST /discover_leads`
- `POST /orchestrate`

## Security

The public `.env.example` contains placeholders only. Real credentials belong
in the ignored `.env` file. The `.dockerignore` file also prevents private
configuration from being copied into Docker images.

## Project status

This project is an active development prototype. The core AI-agent pipeline is
implemented, while real lead-source integrations, automated tests,
authentication, durable queues, monitoring, and production deployment remain
future work.
