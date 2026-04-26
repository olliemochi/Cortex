# Cortex Quick Start Guide

## Project Status

**Status**: In Development | **Last Updated**: April 2026

Core chat, memory, and dreaming systems are implemented. Discord and Tailscale integrations are partial stubs. Not yet suitable for production deployment without further review.

---

## Quick Start

### 5-Minute Setup

#### Option 1: Docker Compose (Easiest)

```bash
# 1. Clone and enter the project
git clone https://github.com/olliemochi/Cortex
cd Cortex

# 2. Copy and configure environment
cp .env.example .env

# 3. Start all services
docker-compose up -d

# 4. Access application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Option 2: Manual Setup

**Backend**:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**:

```bash
cd frontend
npm install
npm run dev
```

---

## Using Cortex

### Web Interface

1. **Open** http://localhost:5173
2. **Chat tab**: Talk to Cortex agent
3. **Memory tab**: View and manage memories
4. **Tools tab**: See available tools
5. **Dreaming tab**: Control memory consolidation
6. **Status tab**: Check system health

### CLI Tool

```bash
# Make it executable
chmod +x cli/cortex_cli.py

# Or run directly
python cli/cortex_cli.py --help

# Examples
python cli/cortex_cli.py chat send "Hello Cortex"
python cli/cortex_cli.py memory list
python cli/cortex_cli.py memory search "important"
python cli/cortex_cli.py dream status
python cli/cortex_cli.py tools list
python cli/cortex_cli.py status
```

### Discord Bot

> **Note:** Discord integration is a partial stub. Endpoints exist but full bot functionality requires additional implementation.

1. **Create Discord bot**:
   - Go to Discord Developer Portal
   - Create application, add Bot, copy token

2. **Start bot**:

   ```bash
   curl -X POST http://localhost:8000/api/cortex/discord/config \
     -H "Content-Type: application/json" \
     -d '{"token": "YOUR_BOT_TOKEN"}'
   ```

### Tailscale Integration

> **Note:** Tailscale integration is a partial stub. Endpoints exist but full device management is not yet verified.

---

## Key Features

### 1. Chat & Conversation

- Talk to Cortex AI agent
- Streaming responses
- Message history
- Context awareness

### 2. Memory Management

- Automatic memory from chats
- Categorized storage
- Search across memories
- Importance scoring
- Long-term promotion

### 3. Dreaming Cycles

- Memory consolidation
- Pattern recognition
- Insight generation
- Connection building
- Scheduled or manual

### 4. Tool Execution

- Execute external tools
- Web search
- Code execution
- Custom tools
- Status monitoring

### 5. CLI Interface

- Terminal commands
- Full feature access
- Automation support
- JSON output

---

## API Examples

### Send Message

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What can you do?",
    "context": {}
  }'
```

### Add Memory

```bash
curl -X POST http://localhost:8000/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{
    "category": "knowledge",
    "title": "Important fact",
    "content": "This is something to remember",
    "importance": 8
  }'
```

### Search Memory

```bash
curl "http://localhost:8000/api/memory/search?query=important&limit=10"
```

### Get Status

```bash
curl http://localhost:8000/api/chat/context
```

### Start Dream

```bash
curl -X POST http://localhost:8000/api/dreaming/run
```

### List Tools

```bash
curl http://localhost:8000/api/tools/
```

---

## Troubleshooting

### Ports Already in Use

```bash
lsof -i :5173  # Frontend
lsof -i :8000  # Backend
kill -9 <PID>
```

### Database Connection Error

```bash
docker ps | grep postgres
docker logs cortex-postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### Services Won't Start

```bash
docker-compose logs -f

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### API Not Responding

```bash
curl http://localhost:8000/health
docker-compose logs backend
```

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
# Database
DATABASE_URL=postgresql://cortex:cortex@localhost:5432/cortex_db

# Security
SECRET_KEY=your-secret-key-here

# Discord (optional)
DISCORD_TOKEN=your_token_here

# Tailscale (optional)
TAILSCALE_API_KEY=your_key_here
TAILSCALE_TAILNET=example.com
```

### Frontend Configuration

In `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

---

## Development

### Adding New Features

1. **Backend endpoint**:
   - Create route in `backend/routers/`
   - Register it in `backend/main.py`
   - Test with `/docs`

2. **Frontend component**:
   - Create `.svelte` file in `frontend/src/`
   - Add API client method in `frontend/src/lib/apis/`
   - Import and use in the relevant route

3. **Database table**:
   - Add model in `backend/models/`
   - Create migration: `cd backend && alembic revision --autogenerate -m "description"`
   - Apply: `alembic upgrade head`

### Running Tests

```bash
# Backend tests
cd backend
pytest test -v

# Frontend tests
cd frontend
npm test
```

### Viewing API Documentation

- Interactive: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Project Structure

```bash
Cortex/
├── frontend/          # SvelteKit UI
├── backend/           # FastAPI application
│   ├── agents/        # CortexAgent, MemoryCore, DreamingEngine, ToolExecutor
│   ├── app/
│   │   └── integrations/  # Discord, Tailscale (partial stubs)
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API route handlers
│   └── main.py
├── cli/               # Python CLI client
├── skills/            # Skill definitions
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── docs/
```

---

## Help & Support

- **Setup detail**: See `docs/SETUP_GUIDE.md`
- **API reference**: See `docs/API_DOCUMENTATION.md`
- **Deployment**: See `docs/DEPLOYMENT_GUIDE.md`
- **Logs**: `docker-compose logs -f`
