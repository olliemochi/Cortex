# Cortex Setup Guide

**Organization**: AetherAssembly  
**License**: MIT  
**Support**: support@aetherassembly.org  
**GitHub**: https://github.com/aetherassembly/Cortex  

---

## Quick Start (Recommended)

For a complete automated setup on any Linux distribution:

```bash
bash install.sh --dev
```

This script will:
- Detect your Linux distribution (Ubuntu, Fedora, Arch, etc.)
- Install system dependencies (Python, PostgreSQL, Node.js)
- Create a Python virtual environment
- Install all backend and frontend dependencies
- Create helper scripts for development

**For more options**: `bash install.sh --help`

---

### Table of Contents

1. [Quick Start](#quick-start-recommended)
2. [Installation Options](#installation-options)
3. [Architecture Overview](#architecture-overview)
4. [Frontend Setup](#frontend-setup)
5. [Backend Setup](#backend-setup)
6. [API Endpoints](#api-endpoints)
7. [Component Structure](#component-structure)
8. [Running the Project](#running-the-project)
9. [Troubleshooting](#troubleshooting)
10. [Development Workflow](#development-workflow)

---

## Installation Options

### Full Installation (All Components)
```bash
bash install.sh
```

### Development Mode (Includes Dev Dependencies)
```bash
bash install.sh --dev
```

### Backend Only
```bash
bash install.sh --backend-only
```

### Frontend Only
```bash
bash install.sh --frontend-only
```

### Skip System Dependencies
```bash
bash install.sh --python-only
```

### Manual Python Setup
```bash
bash setup-venv.sh          # Root directory
cd backend && bash setup-venv.sh  # Backend only
```

---

## Architecture Overview

Cortex is a full-stack application with:

- **Frontend**: Svelte-based UI for chat, memory management, dreaming, tools, and agent status
- **Backend**: Python FastAPI server providing memory management, dreaming cycles, Discord integration, and tool execution
- **Database**: PostgreSQL for storing memory entries, chat history, and dreams
- **Real-time Communication**: WebSocket support for streaming responses and live updates

### Technology Stack

- **Frontend**: Svelte, TypeScript, Vite, Tailwind CSS, SvelteKit
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL
- **API**: REST + WebSocket
- **Container**: Docker + Docker Compose

---

## Frontend Setup

### Prerequisites

- Node.js 16+ or using `nvm`
- `pnpm` (preferred) or `npm`

### Installation Steps

1. **Navigate to frontend directory**:
   ```bash
   cd cortex/frontend
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Configure environment variables**:
   Create `.env.local` in the frontend root:
   ```env
   VITE_API_URL=http://localhost:8000/api
   VITE_WS_URL=ws://localhost:8000/ws
   VITE_ENV=development
   ```

4. **Start development server**:
   ```bash
   pnpm dev
   ```
   The frontend will be available at `http://localhost:5173`

### Build for Production

```bash
pnpm build
pnpm preview
```

---

## Backend Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12+
- Virtual environment (`venv` or `poetry`)

### Installation Steps

1. **Navigate to backend directory**:
   ```bash
   cd cortex/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create `.env` in the backend root:
   ```env
   # Local development
   DATABASE_URL=postgresql://cortex:cortex@localhost:5432/cortex_dev
   # Production example (adjust as needed):
   # DATABASE_URL=postgresql://cortex:STRONG_PASSWORD@db.aetherassembly.org:5432/cortex_prod
   
   # API
   API_HOST=0.0.0.0
   API_PORT=8000
   API_WORKERS=4
   
   # Security
   SECRET_KEY=your-secret-key-here
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   # Production: CORS_ORIGINS=https://cortex.aetherassembly.org,https://api.aetherassembly.org
   
   # Discord Integration (optional)
   DISCORD_TOKEN=your-discord-bot-token
   DISCORD_GUILD_ID=your-guild-id
   
   # Email (optional)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_FROM=support@aetherassembly.org
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=your-app-password
   
   # Logging
   LOG_LEVEL=DEBUG
   ```

5. **Initialize database**:
   ```bash
   alembic upgrade head
   ```

6. **Start development server**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1
```

---

## API Endpoints

### Base URL
- Development: `http://localhost:8000/api`
- Production: `https://api.aetherassembly.org/api`

### Chat Endpoints

- **POST /chat/message**: Send a message to the agent
  ```json
  {
    "message": "Hello Cortex",
    "context": {},
    "stream": false
  }
  ```

- **GET /chat/history**: Get chat history
  - Query params: `?chat_id=&limit=50`

- **GET /chat/context**: Get current agent state

- **POST /chat/memory-update**: Save message to memory
  ```json
  {
    "message_id": "uuid",
    "chat_id": "uuid"
  }
  ```

### Memory Endpoints

- **GET /memory/**: List all memory entries
- **POST /memory/add**: Add new memory
  ```json
  {
    "category": "knowledge",
    "title": "Entry title",
    "content": "Entry content",
    "importance": 5
  }
  ```

- **GET /memory/search**: Search memories
  - Query param: `?query=search_term`

- **POST /memory/promote/{id}**: Promote to long-term storage
- **DELETE /memory/{id}**: Delete memory entry

### Dreaming Endpoints

- **GET /dreaming/status**: Get dreaming status
- **POST /dreaming/run**: Start a dream cycle
- **POST /dreaming/cancel**: Cancel current dream
- **GET /dreaming/history**: Get dream history
  - Query param: `?limit=10`

### Tools Endpoints

- **GET /tools/**: List all tools/skills
- **GET /tools/{tool_name}**: Get tool information
- **POST /tools/{tool_name}/execute**: Execute a tool
  ```json
  {
    "args": {}
  }
  ```

- **GET /tools/{tool_name}/status**: Get tool status

### Discord Endpoints (Admin only)

- **GET /discord/status**: Get Discord bot status
- **POST /discord/test-connection**: Test Discord connection
- **GET /discord/activity**: Get Discord activity log

---

## Running with Helper Scripts

After installation, use the provided scripts:

```bash
# Activate environment
source activate-cortex.sh
# or
source .venv/bin/activate

# Run full development setup
bash run-dev.sh

# Run backend only
bash run-dev.sh --backend-only

# Run frontend only
bash run-dev.sh --frontend-only
```

Default ports:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## Component Structure

### Frontend Component Hierarchy

```
src/
├── lib/
│   ├── api/
│   │   ├── cortex.ts (Main API client)
│   │   ├── memory.ts (Memory API)
│   │   └── tools.ts (Tools API)
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatWindow.svelte
│   │   │   └── ChatInput.svelte
│   │   ├── memory/
│   │   │   └── MemoryTab.svelte
│   │   ├── dreaming/
│   │   │   └── DreamingTab.svelte
│   │   ├── tools/
│   │   │   └── ToolsTab.svelte
│   │   ├── agent/
│   │   │   └── AgentStatusTab.svelte
│   │   └── layout/
│   │       ├── Sidebar.svelte
│   │       ├── Header.svelte
│   │       └── MainLayout.svelte
│   └── stores/
│       ├── chat.ts
│       └── cortex.ts
├── routes/
│   ├── +page.svelte
│   ├── +layout.svelte
│   └── [route]/
└── app.css
```

### Key Components

#### ChatWindow
- Displays conversation history
- Supports markdown rendering
- Shows tool execution results
- Displays loading states

#### MemoryTab
- Lists memory entries by category
- Search functionality
- Promote to long-term storage
- Delete entries

#### ToolsTab
- Lists available tools/skills
- Shows tool status
- Execute tools with parameters
- Displays execution results

#### AgentStatusTab
- Shows agent readiness
- Memory entry count
- Last dream timestamp
- Discord connection status
- Available tools list

---

## Running the Project

### Option 1: Docker Compose (Recommended)

```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Manual Setup

**Terminal 1 - Backend**:
```bash
cd cortex/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd cortex/frontend
pnpm dev
```

**Terminal 3 - Database**:
```bash
# If using local PostgreSQL
sudo service postgresql start
# Or with Docker:
docker run -d --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:14
```

---

## Troubleshooting

### Frontend Issues

**Problem**: CORS errors when calling API
- **Solution**: Check `CORS_ORIGINS` in backend `.env` includes frontend URL

**Problem**: Module not found errors
- **Solution**: Verify `$lib` alias in `svelte.config.js` and `tsconfig.json`

**Problem**: Styles not applying
- **Solution**: Ensure Tailwind CSS is properly configured in `tailwind.config.js`

### Backend Issues

**Problem**: Database connection error
- **Solution**: 
  - Check `DATABASE_URL` is correct
  - Verify PostgreSQL is running
  - Run migrations: `alembic upgrade head`

**Problem**: Port already in use
- **Solution**: Change `API_PORT` in `.env` or kill process: `lsof -i :8000`

**Problem**: Import errors
- **Solution**: Install requirements: `pip install -r requirements.txt`

---

## Development Workflow

### Adding a New Component

1. Create component file in `src/lib/components/{feature}/`
2. Import in parent component or route
3. Add styles (Tailwind classes or `<style>` block)
4. Test in development with `pnpm dev`

### Adding a New API Endpoint

1. Create route handler in `backend/app/routes/`
2. Add to router in `backend/app/main.py`
3. Update TypeScript types in frontend
4. Add API client method in `frontend/src/lib/api/cortex.ts`
5. Test with REST client or curl

### Database Schema Changes

1. Update SQLAlchemy models in `backend/app/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review migration in `backend/alembic/versions/`
4. Apply migration: `alembic upgrade head`

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/cortex-feature

# Make changes and commit
git add .
git commit -m "feat: add cortex feature"

# Push and create PR
git push origin feature/cortex-feature
```

---

## System Installation (Desktop Application)

For production-like environment without development mode, install as a desktop application:

```bash
cd /path/to/cortex
sudo make install-app
# Or manually:
sudo bash install-app.sh
```

This installs:
- Application to `/opt/cortex` (read-only)
- User data to `~/.local/share/cortex/` (writable)
- Launcher to `/usr/local/bin/cortex-launcher`
- Desktop entry to application menu
- **Shell completions (auto-installed)**:
  - Bash: `/etc/bash_completion.d/cortex`
  - Zsh: `/usr/share/zsh/site-functions/_cortex`
  - Fish: `/usr/share/fish/vendor_completions.d/cortex.fish`

### Launching

```bash
# Command line
cortex-launcher

# Application menu (search for "Cortex")

# Make target
make launch
```

### Uninstalling

```bash
sudo cortex-uninstall
# This also removes all shell completions
```

---

## Shell Completions

### CLI Commands Available

After installation, use tab completion in your shell:

```bash
cortex chat send "Hello"                    # Send message to agent
cortex memory list --limit 20               # List memory entries
cortex memory add --category learning       # Add memory entry
cortex memory search "database"             # Search memories
cortex dream status                         # Get dream status
cortex dream run --focus "consolidation"    # Start dream cycle
cortex tools list                           # List available tools
cortex tools execute web_search query="AI"  # Execute a tool
cortex status                               # Show system status
cortex version                              # Show version info
cortex info                                 # Show information
```

### Using Completions

```bash
# View main commands
cortex [TAB]

# View subcommands
cortex memory [TAB]
cortex dream [TAB]

# View options
cortex memory add --[TAB]
cortex dream run --[TAB]
```

### Completion Locations

- **Bash**: `/etc/bash_completion.d/cortex`
- **Zsh**: `/usr/share/zsh/site-functions/_cortex`
- **Fish**: `/usr/share/fish/vendor_completions.d/cortex.fish`

If completions aren't active after installation, restart your shell:

```bash
exec bash    # or zsh, fish
```

---

## Additional Resources

- [Svelte Documentation](https://svelte.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
