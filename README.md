# Cortex - AI Agent Platform

> A full-stack AI agent platform built on Open-WebUI, extended with memory management, dreaming cycles, tool execution, and multi-channel integrations.

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-In%20Development-yellow.svg)

## Project Status

Active development. Core chat, memory, and dreaming systems are implemented. Some integrations (Discord, Tailscale) exist as stubs or are partially wired. Docker image builds are in the process of being stabilised. Not yet suitable for production deployment without further review and configuration.

## Features

### AI Agent

- Chat interface with persistent conversation history
- Context-aware responses via connected LLM backends (Ollama / OpenAI-compatible)
- Streaming responses
- Multi-model support

### Memory System

- Memory storage and retrieval backed by PostgreSQL
- Categorised memories with importance scoring
- Semantic search across stored memories
- Memory promotion to long-term storage
- Built on `backend/agents/memory_core.py` and `backend/routers/memories.py`

### Dreaming Cycles

- Background memory consolidation cycles
- Pattern recognition and insight generation from stored memories
- Configurable scheduling
- Implemented in `backend/agents/dreaming_engine_real.py`

### Tool Execution

- Tool registry and executor (`backend/agents/tool_executor.py`)
- Built-in tools accessible through the chat interface
- Custom tool addition supported

### Discord Integration

- Discord bot stub present (`backend/app/integrations/discord_bot.py`, `backend/app/routes/discord_routes.py`)
- **Status:** partial — wiring exists but full bot functionality requires configuration and testing

### Tailscale Networking

- Tailscale integration stub present (`backend/app/integrations/tailscale.py`, `backend/app/routes/network_routes.py`)
- **Status:** partial — endpoints exist, full device management not verified

### CLI

- Python CLI client in `cli/` directory
- Covers chat, memory, dreaming, and tool commands

### Web Interface

- SvelteKit frontend (Svelte 5, TypeScript, Tailwind CSS 4)
- Real-time WebSocket chat
- Memory manager, notes, channels, workspace views
- Local frontend build verified working

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Or: Node.js 18–22, Python 3.10–3.12, PostgreSQL 12+

### Docker Compose

```bash
git clone https://github.com/olliemochi/Cortex
cd Cortex
cp .env.example .env   # fill in secrets
docker compose up -d
```

Frontend: http://localhost:5173  
Backend API: http://localhost:8000  
API Docs: http://localhost:8000/docs

### Manual Development

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

See [QUICK_START.md](QUICK_START.md) for more detail.

---

## Documentation

- [QUICK_START.md](QUICK_START.md) — setup in a few steps
- [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) — detailed configuration
- [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) — API reference
- [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) — deployment notes

---

## Stack

**Frontend**
- SvelteKit + Svelte 5, TypeScript, Vite, Tailwind CSS 4

**Backend**
- Python 3.10+, FastAPI, SQLAlchemy, PostgreSQL, Redis

**Infrastructure**
- Docker & Docker Compose

---

## Project Structure

```bash
Cortex/
├── frontend/          # SvelteKit UI
│   └── src/
│       ├── lib/
│       │   ├── apis/
│       │   ├── components/
│       │   └── stores/
│       └── routes/
├── backend/           # FastAPI application
│   ├── agents/        # Cortex agent, memory core, dreaming engine, tool executor
│   ├── app/
│   │   ├── integrations/  # Discord, Tailscale (partial)
│   │   └── routes/
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API route handlers
│   └── main.py
├── cli/               # Python CLI client
├── skills/            # Skill definitions for tool integrations
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── docs/
```

---

## API Reference

### Chat

- `POST /api/chat/message` — send message
- `POST /api/chat/stream` — stream response
- `GET /api/chat/history` — conversation history

### Memory

- `GET /api/memory/` — list memories
- `POST /api/memory/add` — add memory
- `GET /api/memory/search` — search memories
- `POST /api/memory/promote/{id}` — promote to long-term
- `DELETE /api/memory/{id}` — delete memory

### Dreaming

- `GET /api/dreaming/status` — current status
- `POST /api/dreaming/run` — start a cycle
- `POST /api/dreaming/cancel` — cancel active cycle
- `GET /api/dreaming/history` — cycle history

### Tools

- `GET /api/tools/` — list tools
- `POST /api/tools/{name}/execute` — execute tool

See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for full details.

---

## Development

### Running Tests

```bash
cd backend
pytest test -v
```

### Linting

```bash
cd backend
flake8 . --max-line-length=127
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT — see [LICENSE](LICENSE).

Cortex builds on [Open-WebUI](https://github.com/open-webui/open-webui) (MIT). Full attribution in LICENSE.

---

**Cortex** — AI Agent Platform by [AetherAssembly](https://aetherassembly.org)  
Repository: [github.com/olliemochi/Cortex](https://github.com/olliemochi/Cortex)
