## Cortex Deployment Guide

### Status
🟢 **READY FOR DEPLOYMENT** (As of April 20, 2026)

All systems are production-ready. Follow this guide to deploy to your environment.

### Table of Contents
1. [Development Deployment](#development-deployment)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Environment Configuration](#environment-configuration)
6. [SSL/TLS Configuration](#ssltls-configuration)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)

---

## Development Deployment

### Local Docker Compose

1. **Clone and setup**:
   ```bash
   cd /home/aster/Documents/Cortex-Project
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Start services**:
   ```bash
   docker-compose up -d
   ```

4. **View logs**:
   ```bash
   docker-compose logs -f
   ```

5. **Access application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Database: localhost:5432

---

## Production Deployment

### Prerequisites

- Docker & Docker Compose installed
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)
- Minimum 2GB RAM server

### Deployment Steps

1. **Server Setup**:
   ```bash
   # Update system
   sudo apt-get update && sudo apt-get upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/cortex.git
   cd cortex
   ```

3. **Configure Production Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with production values
   nano .env
   ```

4. **Configure SSL**:
   ```bash
   # Copy SSL certificates
   mkdir -p ssl
   cp /path/to/cert.pem ssl/
   cp /path/to/key.pem ssl/
   ```

5. **Start Services**:
   ```bash
   docker-compose up -d
   ```

6. **Verify Deployment**:
   ```bash
   docker-compose ps
   docker-compose logs -f backend
   ```

---

## Docker Deployment

### Build and Push Images

1. **Build images**:
   ```bash
   # Build backend
   docker build -t cortex-backend:latest ./cortex/backend
   
   # Build frontend
   docker build -t cortex-frontend:latest ./cortex/frontend
   ```

2. **Push to registry**:
   ```bash
   # Tag images
   docker tag cortex-backend:latest myregistry/cortex-backend:latest
   docker tag cortex-frontend:latest myregistry/cortex-frontend:latest
   
   # Push
   docker push myregistry/cortex-backend:latest
   docker push myregistry/cortex-frontend:latest
   ```

3. **Use in compose**:
   ```yaml
   services:
     backend:
       image: myregistry/cortex-backend:latest
     frontend:
       image: myregistry/cortex-frontend:latest
   ```

### Docker Compose Profiles

```bash
# Start with cache support
docker-compose --profile cache up -d

# Start with reverse proxy
docker-compose --profile proxy up -d

# Start everything
docker-compose --profile cache --profile proxy up -d
```

---

## Kubernetes Deployment

### Create Manifests

1. **Namespace**:
   ```yaml
   apiVersion: v1
   kind: Namespace
   metadata:
     name: cortex
   ```

2. **ConfigMap**:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: cortex-config
     namespace: cortex
   data:
     API_HOST: "0.0.0.0"
     API_PORT: "8000"
     LOG_LEVEL: "INFO"
     CORS_ORIGINS: "https://cortex.aetherassembly.org"
   ```

3. **Secret**:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: cortex-secret
     namespace: cortex
   type: Opaque
   stringData:
     DATABASE_URL: "postgresql://cortex:password@postgres:5432/cortex_db"
     SECRET_KEY: "$(openssl rand -hex 32)"
     DISCORD_TOKEN: "your-discord-token"
   ```

4. **Deployment**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: cortex-backend
     namespace: cortex
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: cortex-backend
     template:
       metadata:
         labels:
           app: cortex-backend
       spec:
         containers:
         - name: backend
           image: cortex-backend:latest
           ports:
           - containerPort: 8000
           envFrom:
           - configMapRef:
               name: cortex-config
           - secretRef:
               name: cortex-secret
           livenessProbe:
             httpGet:
               path: /docs
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 10
   ```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace cortex

# Apply manifests
kubectl apply -f cortex-namespace.yaml
kubectl apply -f cortex-configmap.yaml
kubectl apply -f cortex-secret.yaml
kubectl apply -f cortex-deployment.yaml
kubectl apply -f cortex-service.yaml
kubectl apply -f cortex-ingress.yaml

# Check status
kubectl get all -n cortex
kubectl logs -n cortex deployment/cortex-backend
```

---

## Environment Configuration

### Development

```env
# Database
DATABASE_URL=postgresql://cortex:cortex@localhost:5432/cortex_dev

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=2

# Security
SECRET_KEY=dev-secret-key-not-secure
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=DEBUG

# Frontend
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENV=development
```

### Production

```env
# Database
DATABASE_URL=postgresql://cortex:$(openssl rand -hex 16)@db.aetherassembly.org:5432/cortex_prod

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Security
SECRET_KEY=GENERATE_WITH_openssl_rand_-hex_32
CORS_ORIGINS=https://cortex.aetherassembly.org,https://api.aetherassembly.org
ALLOWED_HOSTS=cortex.aetherassembly.org,api.aetherassembly.org

# SSL
ENABLE_SSL=true
SSL_CERT_PATH=/etc/ssl/certs/cert.pem
SSL_KEY_PATH=/etc/ssl/private/key.pem

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/cortex/app.log

# Frontend
VITE_API_URL=https://api.aetherassembly.org/api
VITE_WS_URL=wss://api.aetherassembly.org/ws
VITE_ENV=production

# Discord (optional)
DISCORD_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_guild_id

# Tailscale (optional)
TAILSCALE_API_KEY=tskey-xxx
TAILSCALE_TAILNET=aetherassembly.com
```

---

## SSL/TLS Configuration

### Using Let's Encrypt

1. **Install Certbot**:
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Generate Certificate**:
   ```bash
   sudo certbot certonly --standalone -d cortex.aetherassembly.org -d api.aetherassembly.org
   ```

3. **Configure Nginx**:
   ```nginx
   server {
     listen 443 ssl http2;
     server_name cortex.aetherassembly.org;
     
     ssl_certificate /etc/letsencrypt/live/cortex.aetherassembly.org/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/cortex.aetherassembly.org/privkey.pem;
     
     # Security headers
     add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
     add_header X-Content-Type-Options "nosniff" always;
     add_header X-Frame-Options "DENY" always;
   }
   ```

4. **Auto-renewal**:
   ```bash
   sudo certbot renew --dry-run
   ```

---

## Monitoring & Logging

### Docker Logs

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Stream logs
docker-compose logs -f backend

# View specific container
docker logs cortex-backend
```

### Log Files

```bash
# Backend logs
docker exec cortex-backend tail -f /var/log/cortex/app.log

# Database logs
docker logs cortex-postgres
```

### Health Checks

```bash
# Check service health
curl http://localhost:8000/health

# Check database
docker exec cortex-postgres pg_isready -U cortex

# Check frontend
curl http://localhost:5173
```

### Monitoring Stack

```bash
# Start with Prometheus and Grafana
docker-compose --profile monitoring up -d

# Access Grafana
# http://localhost:3000 (admin/admin)
```

---

## Backup & Recovery

### Database Backup

1. **Automated backup**:
   ```bash
   # Create backup script
   cat > backup-db.sh << 'EOF'
   #!/bin/bash
   BACKUP_DIR="/backups/cortex"
   mkdir -p $BACKUP_DIR
   
   docker exec cortex-postgres pg_dump -U cortex cortex_db | \
     gzip > $BACKUP_DIR/cortex_db_$(date +%Y%m%d_%H%M%S).sql.gz
   EOF
   
   chmod +x backup-db.sh
   ```

2. **Schedule with cron**:
   ```bash
   # Daily backup at 2 AM
   0 2 * * * /home/user/backup-db.sh
   ```

3. **Restore from backup**:
   ```bash
   gunzip -c /backups/cortex/cortex_db_20240120_020000.sql.gz | \
     docker exec -i cortex-postgres psql -U cortex cortex_db
   ```

### Container Restart

```bash
# Restart specific service
docker-compose restart backend

# Restart all services
docker-compose restart

# Restart and pull latest images
docker-compose down
docker-compose pull
docker-compose up -d
```

### Disaster Recovery

1. **Backup volumes**:
   ```bash
   docker run --rm -v cortex-postgres:/data -v /backups:/backup \
     alpine tar czf /backup/postgres-data.tar.gz -C /data .
   ```

2. **Restore volumes**:
   ```bash
   docker run --rm -v cortex-postgres:/data -v /backups:/backup \
     alpine tar xzf /backup/postgres-data.tar.gz -C /data
   ```

---

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Error

```bash
# Check database
docker exec cortex-postgres psql -U cortex -c "\l"

# Reset database
docker exec cortex-postgres psql -U cortex -c "DROP DATABASE cortex_db; CREATE DATABASE cortex_db;"
```

### API Not Responding

```bash
# Check container status
docker ps | grep cortex

# Restart service
docker-compose restart backend

# View logs
docker-compose logs -f backend
```

---

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose build --no-cache

# Restart services
docker-compose up -d
```

### Database Migrations

```bash
# Run migrations
docker exec cortex-backend alembic upgrade head

# Create migration
docker exec cortex-backend alembic revision --autogenerate -m "description"
```

### Clean Up

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f
```

---

## Security Best Practices

1. **Change default passwords** in `.env`
2. **Use strong SECRET_KEY** (generate with `openssl rand -hex 32`)
3. **Enable SSL/TLS** in production
4. **Limit CORS origins** to trusted domains
5. **Use environment variables** for secrets (not in code)
6. **Enable authentication** for sensitive endpoints
7. **Regular backups** of database and volumes
8. **Monitor logs** for suspicious activity
9. **Keep dependencies updated**
10. **Use network firewalls** to restrict access

---

## Performance Optimization

1. **Database**:
   - Enable query caching
   - Use connection pooling
   - Index frequently queried columns

2. **API**:
   - Enable compression
   - Use Redis for caching
   - Implement rate limiting

3. **Frontend**:
   - Minify and bundle assets
   - Enable CDN for static files
   - Use service workers

4. **Docker**:
   - Use multi-stage builds
   - Optimize layer caching
   - Use alpine images

---

## Scaling

### Horizontal Scaling

```yaml
services:
  backend:
    deploy:
      replicas: 3
    environment:
      - API_WORKERS=2
```

### Load Balancing

```bash
# Use Nginx as load balancer
docker-compose --profile proxy up -d
```

### Database Replication

```bash
# PostgreSQL replication
# Configure primary and standby replicas
```

---

Created with comprehensive deployment best practices.
