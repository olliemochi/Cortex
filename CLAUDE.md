# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cortex is a full-stack AI agent platform built on top of Open-WebUI, extended with a memory system, dreaming cycles, tool execution, and multi-channel integrations (web UI, Discord, CLI). Python 3.10+ backend (FastAPI), SvelteKit 5 frontend.

## Commands

### Development

```bash
make dev              # Start both frontend and backend dev servers
make install-dev      # Install all dependencies including dev tools
make build            # Build production bundle
```

### Backend (manual)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload  # port 8000
```

### Frontend (manual)

```bash
cd frontend
npm install
npm run dev       # port 5173
npm run build
npm run lint
npm run check     # Svelte type checking
```

### Docker

```bash
make docker-build
make docker-up    # docker-compose up -d
make docker-down
```

### Code Quality

```bash
make lint         # eslint + pylint
make format       # prettier + ruff
```

### Testing

```bash
cd backend && pytest backend/test -v
cd frontend && npm test
```

### Database Migrations

```bash
cd backend && alembic upgrade head
alembic revision --autogenerate -m "description"
```

## Architecture

The system has four layers:

**Frontend** (SvelteKit, port 5173) — web UI, real-time via WebSocket  
**Backend API** (FastAPI, port 8000) — REST + WebSocket, auth, routing  
**Agent & Memory layer** — CortexAgent orchestrator, MemoryCore, DreamingEngine, ToolExecutor  
**Infrastructure** — PostgreSQL (data), Redis (optional cache), Ollama (local LLMs), external APIs

### Key Data Flows

1. **Chat**: User message → REST API → `CortexAgent` → model inference → streamed response → saved to DB
2. **Memory consolidation**: Dreaming timer → `DreamingEngine` (5-phase cycle) → pattern analysis → promotes memories, writes insights to `DREAMS.md`
3. **Discord**: Discord gateway → Bot handler → same `CortexAgent` path as web UI
4. **Tool execution**: User command → `ToolExecutor` registry → execute → return results

### Backend Structure (`backend/`)

- `main.py` — FastAPI app entry point, router registration
- `config.py` / `cortex_env.py` — configuration and environment
- `routers/` — API endpoints; Cortex-specific ones are `cortex_chat.py`, `cortex_tools.py`, `memory.py`, `dreaming.py`, `discord.py`; the rest are inherited from Open-WebUI
- `agents/cortex.py` — main message orchestrator
- `agents/memory_core.py` — semantic search, categorization, importance scoring
- `agents/dreaming_engine_real.py` — 5-phase background memory consolidation
- `models/` — SQLAlchemy ORM models (25+ tables: users, chats, memories, files, functions, etc.)

### Frontend Structure (`frontend/`)

- `src/lib/` — shared components and utilities
- `src/routes/` — SvelteKit page routes
- Real-time communication via WebSocket; REST calls to `VITE_API_URL`

### CLI (`cli/`)

Click-based client with command groups: `chat`, `memory`, `dreaming`, `tools`, `system`. Shell completions provided for Bash, Zsh, and Fish.

## Environment Configuration

Copy `.env.example` to `.env` at the repo root and configure:

- Database URL (PostgreSQL default in Docker, SQLite for local dev)
- Redis URL (optional)
- `OLLAMA_BASE_URL` for local LLM (default `http://localhost:11434`)
- API keys for OpenAI, Anthropic, Google if used
- `DISCORD_BOT_TOKEN` for Discord integration

Frontend env vars go in `frontend/.env` (`VITE_API_URL`, `VITE_WS_URL`).

## Change Log

All changes made by Claude Code are recorded in [`CHANGES.md`](./CHANGES.md).

## Open-WebUI Base

Cortex extends Open-WebUI — many routers, models, and UI components are inherited from it. Cortex-specific additions are prefixed with `cortex_` or live in `agents/`. When exploring API routes, distinguish between inherited Open-WebUI routes and Cortex-specific ones.
