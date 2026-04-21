# Cortex Architecture

## Status
🟢 **COMPLETE & PRODUCTION READY** (Last Updated: April 20, 2026)

The architecture below describes the fully implemented system with all components active and operational. The Dreaming Engine has been upgraded to use the complete `dreaming_engine_real.py` implementation with full 5-phase processing.

## Overview

Cortex is a distributed AI agent system that:
1. Provides a unified chat interface (web UI + Discord + CLI)
2. Manages local models via Ollama
3. Maintains long-term memory and dreaming
4. Executes tools with multi-level approval
5. Runs on Tailscale for secure access

## System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  SvelteKit UI (port 3000)   │  Discord Bot  │  CLI Client   │
│  - Chat interface           │  - Messages   │  - Commands   │
│  - Slash commands           │  - Locked DMs │  - Streaming  │
│  - Memory/Dreams tabs       │               │               │
└──────────────────────────────────────────────────────────────┘
                                ↓
                         ┌─────────────┐
                         │ REST API    │
                         │ port 8080   │
                         └─────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                       BACKEND LAYER (FastAPI)               │
├─────────────────────────────────────────────────────────────┤
│  Routers:                                                    │
│  ├─ Chat (message routing)                                  │
│  ├─ Models (Ollama integration)                             │
│  ├─ Memory (MEMORY.md persistence)                          │
│  ├─ Dreaming (memory consolidation)                         │
│  ├─ Tools (skill execution)                                 │
│  ├─ Search (web search)                                     │
│  └─ Discord (bot gateway)                                   │
└──────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                    AGENT LAYER (OpenClaw)                   │
├─────────────────────────────────────────────────────────────┤
│  ├─ Main Cortex Agent (orchestration)                       │
│  ├─ Memory Core (read/write MEMORY.md)                      │
│  ├─ Dreaming Engine (consolidation loop)                    │
│  └─ Sub-Agents (spawned for complex tasks)                  │
└──────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                   RUNTIME LAYER (Services)                  │
├─────────────────────────────────────────────────────────────┤
│  ├─ Ollama (http://localhost:11434)                         │
│  ├─ Memory Store (MEMORY.md + DREAMS.md)                    │
│  ├─ Database (SQLite: users, sessions, auth)                │
│  ├─ Redis Cache (optional: caching & sessions)              │
│  └─ External APIs (search, Discord, etc.)                   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Chat Message Flow
```
User types message → Frontend sends to /api/chat → 
Backend router checks auth → 
Passes to Cortex Agent → 
Agent spawns sub-agent if needed →
Sub-agent calls Ollama →
Response streamed back to frontend →
Message saved to database
```

### Memory Consolidation Flow
```
Dreaming timer triggers (cron) →
Dreaming Engine starts cycle →
Reads MEMORY.md & DREAMS.md →
Agent reviews past interactions →
Consolidates short-term → long-term →
Promotes/demotes entries →
Writes DREAMS.md with insights →
Resets short-term memory
```

### Discord Integration Flow
```
Discord message arrives →
Discord bot gateway checks allowlist →
If allowed: route to Cortex Agent →
Agent processes same as web UI →
Response streamed back to Discord →
Logged in activity audit
```

## File Structure Details

### Frontend (`cortex/frontend/`)
- **SvelteKit config**: `vite.config.ts`, `svelte.config.js`
- **Routes**: 
  - `routes/(app)/` — Main chat interface (from open-webui)
  - `routes/auth/` — Login/register (from open-webui)
- **Components**:
  - `lib/components/chat/` — Chat UI (from open-webui, untouched)
  - `lib/components/dreams/` — Dreams tab
  - `lib/components/memory/` — Memory tab
  - `lib/components/tools/` — Tools tab
  - `lib/components/agent/` — Agent status tab
  - `lib/components/sidebar/` — Modified to add new tabs
- **Commands**: `lib/commands/` — Slash command autocomplete

### Backend (`cortex/backend/`)
- **Entry**: `main.py` — FastAPI app + OpenClaw gateway init
- **Routers** (`routers/`):
  - `chat.py` — Message routing
  - `ollama.py` — Model selection (from open-webui)
  - `memory.py` — Memory CRUD
  - `dreaming.py` — Dreaming endpoints
  - `tools.py` — Tool execution
  - `search.py` — Web search (from open-webui)
  - `discord.py` — Discord bot gateway
  - `auth.py` — User auth (from open-webui, +bot role)
- **Agents** (`agents/`):
  - `cortex.py` — Main agent orchestration
  - `memory_core.py` — Memory management
  - `dreaming_engine.py` — Memory consolidation
- **Models** (`models/`): Database schemas (from open-webui, +bot field)
- **Utils** (`utils/`): Helpers (from open-webui)
- **Data** (`data/`): DB migrations (from open-webui)

### CLI (`cortex/cli/`)
- `cortex.py` — Main CLI entry point
- `commands/` — Subcommand modules
- `completions/` — Shell completion scripts

### Memory (`cortex/memory/`)
- `MEMORY.md` — Long-term memory store
- `DREAMS.md` — Dream cycle diary

## Authentication & Authorization

### Users
- From open-webui auth system
- Roles: `user`, `admin`, `bot`
- JWT tokens with expiry
- Optional: LDAP/SAML via Authlib

### Bot Access
- New `bot` role for Discord & CLI
- Service-to-service auth with API keys
- Per-channel/user allowlists

### Tailscale
- Automatic TLS certificates
- Private IPs on Tailscale mesh
- No public internet exposure
- MagicDNS for hostname resolution

## Performance Considerations

### Caching
- Redis for:
  - Chat history chunks
  - User sessions
  - Model metadata
  - Search results (if enabled)
- Memory: Approximate 100MB per 10K MEMORY.md entries

### Streaming
- WebSocket for frontend (SvelteKit)
- Server-Sent Events (SSE) fallback
- Token streaming from Ollama

### Database
- SQLite by default (single-user)
- PostgreSQL for multi-user deployments
- Indexed columns: user_id, conversation_id, timestamp

### Concurrency
- FastAPI async/await for I/O
- Thread pool for CPU-bound tasks
- Request rate limiting: 100 req/min per user

## Security

### Input Validation
- All user inputs sanitized
- SQL injection protection (SQLAlchemy ORM)
- XSS protection (Svelte auto-escaping)
- CSRF tokens on form submissions

### Secrets
- Environment variables for sensitive data
- No secrets in code or version control
- JWT signing key rotatable

### Discord Bot
- Token stored in env var
- Locked to allowed channels/users
- No permission escalation
- Message audit logging

### Tailscale
- All traffic encrypted
- Zero-trust network
- VPN not required
- Revocable device keys

## Extensibility

### Adding New Tools/Skills
1. Create `.ts` or `.py` file in `skills/cortex/`
2. Define tool interface (name, description, params, execute)
3. Register in `agents/cortex.py`
4. Available immediately to all agents

### Adding New Commands
1. Add to `frontend/src/lib/commands/registry.ts`
2. Implement handler in backend router
3. Autocomplete added automatically

### Adding New Channels (Discord, Slack, etc.)
1. Create `routers/[channel].py`
2. Implement `ChannelAdapter` interface
3. Route to same Cortex Agent
4. Same memory & tools available

## Deployment

### Development
```bash
make dev  # Runs frontend + backend in hot-reload mode
```

### Docker (Recommended)
```bash
docker-compose up -d
# Includes: frontend, backend, Ollama, Redis
```

### Tailscale
```bash
./tailscale.sh
# Binds backend to Tailscale interface only
```

### Production (On your server)
```bash
docker-compose -f docker-compose.yml up -d
# Access via: https://cortex.tailnet-xxx.ts.net/
```

## Monitoring & Debugging

### Logs
- Frontend: Browser console + `npm run dev` output
- Backend: `docker logs cortex_backend` or `./logs/cortex.log`
- Agent runs: Structured JSON logs with session IDs

### Debug Mode
```bash
CORTEX_LOG_LEVEL=debug docker-compose up -d
```

### Health Checks
- Backend: `GET /api/health` → returns uptime, model status, memory size
- Ollama: `GET http://localhost:11434/api/tags` → model list
- Discord: Heartbeat every 30s

## Future Enhancements

- [ ] Plugins/extensions marketplace
- [ ] Multi-agent conversations with turn-taking
- [ ] Vision capabilities (image analysis)
- [ ] Audio/voice input (Whisper + TTS)
- [ ] Fine-tuning interface for custom models
- [ ] Distributed memory (shared cortex nodes)
- [ ] Advanced dreaming (insight derivation, forgetting)
