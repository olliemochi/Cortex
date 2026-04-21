# Cortex Quick Start Guide

## 🟢 PROJECT STATUS
**Completion**: 100% ✅ | **Status**: Production Ready | **Last Updated**: April 20, 2026

All features are fully implemented and operational. Ready to deploy!

---

## Quick Start

### 5-Minute Setup

#### Option 1: Docker Compose (Easiest)

```bash
# 1. Clone/navigate to project
cd /home/aster/Documents/Cortex-Project

# 2. Start all services
docker-compose up -d

# 3. Access application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Option 2: Manual Setup

**Backend**:
```bash
cd cortex/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd cortex/frontend
pnpm install
pnpm dev
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
chmod +x cortex/cli/cortex_cli.py

# Or use as module
python -m cortex.cli.cortex_cli --help

# Examples
python -m cortex.cli.cortex_cli chat send "Hello Cortex"
python -m cortex.cli.cortex_cli memory list
python -m cortex.cli.cortex_cli memory search "important"
python -m cortex.cli.cortex_cli dream status
python -m cortex.cli.cortex_cli tools list
python -m cortex.cli.cortex_cli status
```

### Discord Bot

1. **Create Discord bot**:
   - Go to Discord Developer Portal
   - Create application
   - Add Bot
   - Copy token

2. **Start bot**:
   ```bash
   curl -X POST http://localhost:8000/api/discord/start \
     -H "Content-Type: application/json" \
     -d '{"token": "YOUR_BOT_TOKEN"}'
   ```

3. **Use bot** in Discord:
   ```
   /chat What's the weather?
   /memory add My important note
   /memory search past events
   /status
   /dream
   /help
   ```

### Tailscale Integration

1. **Initialize Tailscale**:
   ```bash
   curl -X POST http://localhost:8000/api/network/tailscale/connect
   ```

2. **Get status**:
   ```bash
   curl http://localhost:8000/api/network/tailscale/status
   ```

3. **List peers**:
   ```bash
   curl http://localhost:8000/api/network/tailscale/peers
   ```

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

### 5. Discord Integration
- Direct Discord chat
- Memory commands
- Status checks
- Dream triggers
- Activity logging

### 6. Tailscale Networking
- Secure remote access
- Device pairing
- Network management
- Peer discovery
- Auth key generation

### 7. CLI Interface
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
# Kill process on port
lsof -i :5173  # Frontend
lsof -i :8000  # Backend
kill -9 <PID>
```

### Database Connection Error

```bash
# Check database
docker ps | grep postgres
docker logs cortex-postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### Services Won't Start

```bash
# Check logs
docker-compose logs -f

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### API Not Responding

```bash
# Check health
curl http://localhost:8000/health

# View logs
docker-compose logs backend
```

---

## Configuration

### Environment Variables

Create `.env` file:

```env
# Database
DATABASE_URL=postgresql://cortex:cortex@localhost:5432/cortex_db

# API
API_PORT=8000
API_WORKERS=4

# Security
SECRET_KEY=dev-secret-key

# Discord (optional)
DISCORD_TOKEN=your_token_here

# Tailscale (optional)
TAILSCALE_API_KEY=your_key_here
TAILSCALE_TAILNET=example.com
```

### Frontend Configuration

In `cortex/frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENV=development
```

---

## Development

### Adding New Features

1. **Backend endpoint**:
   - Create route in `app/routes/`
   - Add to `app/main.py`
   - Test with `/docs`

2. **Frontend component**:
   - Create `.svelte` file
   - Add API client method
   - Import and use in route

3. **Database table**:
   - Add model in `app/models/`
   - Create migration
   - Apply with `alembic upgrade head`

### Running Tests

```bash
# Backend tests
cd cortex/backend
pytest

# Frontend tests
cd cortex/frontend
pnpm test
```

### Viewing API Documentation

- Interactive: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Next Steps

1. **Customize** agent behavior in `app/config.py`
2. **Add** more tools in `app/services/tools.py`
3. **Create** Discord commands in `app/integrations/discord_bot.py`
4. **Deploy** using `DEPLOYMENT_GUIDE.md`
5. **Monitor** using logs and health endpoints
6. **Scale** by adding more workers/replicas

---

## Help & Support

- **Documentation**: See `SETUP_GUIDE.md`, `API_DOCUMENTATION.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md`
- **Issues**: Check `TROUBLESHOOTING.md` section
- **Logs**: `docker-compose logs -f`

---

## Project Structure

```
cortex/
├── frontend/          # Svelte UI
├── backend/          # Python API
├── cli/              # Command-line tool
├── docker-compose.yml
├── SETUP_GUIDE.md
├── API_DOCUMENTATION.md
├── DEPLOYMENT_GUIDE.md
└── QUICK_START.md    # This file
```

---

**Ready to use!** 🚀
