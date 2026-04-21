# Source: NEW - Frontend Dockerfile
# CORTEX MODIFICATION: Docker container for Cortex frontend UI

# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source
COPY . .

# Build
RUN npm run build

# Runtime stage
FROM node:18-alpine

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built assets from builder
COPY --from=builder /app/.svelte-kit/build ./build
COPY --from=builder /app/package.json ./package.json

# Expose port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:5173 || exit 1

# Start application
CMD ["serve", "-s", "build", "-l", "5173"]
