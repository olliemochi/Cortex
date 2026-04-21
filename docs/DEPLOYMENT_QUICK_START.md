# Cortex Deployment Quick Start

🟢 **PRODUCTION READY** | Last Updated: April 20, 2026

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for CLI development)
- Node.js 18+ and npm (for frontend development)

## Quick Start with Docker

### 1. Clone and Navigate
```bash
cd /home/aster/Documents/Cortex-Project/cortex
```

### 2. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Build and Run

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### 4. Access Services

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: postgres://cortex@localhost:5432/cortex_db

### 5. Verify Services

```bash
# Check backend health
curl http://localhost:8000/docs

# Check frontend
curl http://localhost:5173

# Check database
docker-compose exec postgres psql -U cortex -d cortex_db -c "SELECT 1"
```

## Development Setup

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### CLI Tool
```bash
cd cli

# Install CLI package
pip install -e .

# Use CLI
python -m cortex_cli --help
```

## Docker Compose Profiles

### Start with Redis Cache
```bash
docker-compose --profile cache up -d
```

### Start with Nginx Proxy
```bash
docker-compose --profile proxy up -d
```

### Start Everything
```bash
docker-compose --profile cache --profile proxy up -d
```

## Common Operations

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Follow last 100 lines
docker-compose logs -f --tail 100
```

### Run Database Migrations
```bash
docker-compose exec backend alembic upgrade head
```

### Access Database Shell
```bash
docker-compose exec postgres psql -U cortex -d cortex_db
```

### Stop Services
```bash
docker-compose down
```

### Clean Up Everything
```bash
docker-compose down -v  # Remove volumes
docker-compose down --rmi all  # Remove images
```

## Troubleshooting

### Ports Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Change port in docker-compose.yml or .env
```

### Database Connection Errors
```bash
# Check database is healthy
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Frontend Build Errors
```bash
# Clear node_modules and rebuild
docker-compose exec frontend rm -rf node_modules
docker-compose rebuild frontend
docker-compose up -d frontend
```

### Backend Import Errors
```bash
# Reinstall dependencies
docker-compose exec backend pip install -r requirements.txt

# Restart backend
docker-compose restart backend
```

## Production Deployment

### Using Docker Swarm
1. Initialize Swarm: `docker swarm init`
2. Create stack: `docker stack deploy -c docker-compose.yml cortex`
3. View services: `docker service ls`

### Using Kubernetes
1. Convert compose to Kubernetes: `kompose convert -f docker-compose.yml`
2. Deploy: `kubectl apply -f *.yaml`
3. View services: `kubectl get services`

### Environment Variables for Production
```env
# Security
SECRET_KEY=<generate-new-secret>
JWT_ALGORITHM=HS256

# Database
DATABASE_URL=postgresql://user:password@host/database

# CORS
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# Discord (optional)
DISCORD_BOT_TOKEN=<your-token>

# Tailscale (optional)
TAILSCALE_API_KEY=<your-api-key>
```

## Monitoring and Maintenance

### Health Checks
```bash
# Backend health
curl -s http://localhost:8000/docs | head -20

# Frontend health
curl -s http://localhost:5173 | head

# Database health
docker-compose exec postgres pg_isready -U cortex
```

### Backup Database
```bash
docker-compose exec postgres pg_dump -U cortex cortex_db > backup.sql
```

### Restore Database
```bash
docker-compose exec -T postgres psql -U cortex cortex_db < backup.sql
```

## Next Steps

1. Review `.env.example` and configure your environment
2. Set Discord bot token if using Discord integration
3. Configure Tailscale API key for network integration
4. Customize frontend branding in `frontend/`
5. Add custom tools in `backend/app/tools/`
6. Set up reverse proxy (Nginx) for production

For more detailed information, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
