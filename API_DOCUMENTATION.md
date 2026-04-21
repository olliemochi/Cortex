## Cortex Backend API Documentation

### Status
🟢 **ALL ENDPOINTS FULLY IMPLEMENTED** (As of April 20, 2026)

All 20+ endpoints are production-ready and fully functional with real backend implementations.

### Overview

The Cortex backend provides a comprehensive REST API for chat, memory management, dreaming cycles, tool execution, and Discord integration. This document details all endpoints, request/response formats, and usage examples.

---

## Authentication & Security

### API Keys

Currently in development mode (no authentication required). For production:

```
Authorization: Bearer <api_key>
```

### CORS Configuration

Allowed origins must be configured in `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://cortex.example.com
```

---

## Chat API

### Send Message

**Endpoint**: `POST /api/chat/message`

**Request**:
```json
{
  "message": "What is your capability?",
  "context": {
    "user_id": "optional-user-id",
    "session_id": "optional-session-id"
  },
  "stream": false
}
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "id": "msg-uuid",
    "content": "I am Cortex, an AI assistant...",
    "role": "assistant",
    "timestamp": "2024-01-15T10:30:00Z",
    "tokens": {
      "input": 15,
      "output": 45,
      "total": 60
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Stream Message

**Endpoint**: `POST /api/chat/stream`

Streams response as Server-Sent Events (SSE):

**Request**:
```json
{
  "message": "Tell me a story",
  "context": {},
  "stream": true
}
```

**Response** (streamed chunks):
```json
{"type": "start", "id": "msg-uuid"}
{"type": "chunk", "content": "Once upon"}
{"type": "chunk", "content": " a time"}
{"type": "end", "tokens": {"input": 10, "output": 20}}
```

### Get Chat History

**Endpoint**: `GET /api/chat/history`

**Query Parameters**:
- `chat_id` (optional): Filter by specific chat session
- `limit` (optional, default: 50): Maximum messages to return
- `offset` (optional, default: 0): Pagination offset

**Response**:
```json
{
  "status": "ok",
  "data": [
    {
      "id": "msg-uuid",
      "content": "Hello",
      "role": "user",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "id": "msg-uuid-2",
      "content": "Hello! How can I help?",
      "role": "assistant",
      "timestamp": "2024-01-15T10:00:05Z"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Chat Context

**Endpoint**: `GET /api/chat/context`

Returns current agent state and capabilities.

**Response**:
```json
{
  "status": "ok",
  "data": {
    "agent_ready": true,
    "agent_name": "Cortex",
    "memory_entries": 42,
    "last_dream": "2024-01-15T08:00:00Z",
    "dreaming_enabled": true,
    "discord_status": "connected",
    "available_tools": [
      "web_search",
      "memory_query",
      "code_execution"
    ],
    "model_info": {
      "name": "gpt-4",
      "context_size": 8192,
      "temperature": 0.7
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Save to Memory

**Endpoint**: `POST /api/chat/memory-update`

**Request**:
```json
{
  "message_id": "msg-uuid",
  "chat_id": "chat-uuid"
}
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "memory_id": 123,
    "message_id": "msg-uuid",
    "status": "promoted"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Memory API

### List Memories

**Endpoint**: `GET /api/memory/`

**Query Parameters**:
- `category` (optional): Filter by category
- `status` (optional): Filter by status (short_term, long_term, promoted)
- `limit` (optional, default: 50)
- `offset` (optional, default: 0)

**Response**:
```json
{
  "status": "ok",
  "data": [
    {
      "id": 1,
      "category": "knowledge",
      "title": "User Preferences",
      "content": "User prefers technical discussions",
      "importance": 8,
      "date": "2024-01-14T15:30:00Z",
      "status": "promoted",
      "access_count": 12
    }
  ],
  "total": 42,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Add Memory

**Endpoint**: `POST /api/memory/add`

**Request**:
```json
{
  "category": "knowledge",
  "title": "Important Note",
  "content": "This is important information to remember",
  "importance": 7
}
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "id": 42,
    "category": "knowledge",
    "title": "Important Note",
    "content": "This is important information to remember",
    "importance": 7,
    "date": "2024-01-15T10:30:00Z",
    "status": "short_term"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Search Memories

**Endpoint**: `GET /api/memory/search`

**Query Parameters**:
- `query` (required): Search term
- `limit` (optional, default: 20)

**Response**:
```json
{
  "status": "ok",
  "data": [
    {
      "id": 5,
      "category": "knowledge",
      "title": "Search Result",
      "content": "Matching memory content",
      "importance": 6,
      "date": "2024-01-14T10:00:00Z",
      "status": "long_term",
      "relevance_score": 0.95
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Promote Memory

**Endpoint**: `POST /api/memory/promote/{id}`

Moves a memory from short-term to long-term storage.

**Response**:
```json
{
  "status": "ok",
  "data": {
    "id": 42,
    "status": "promoted",
    "promoted_at": "2024-01-15T10:30:00Z"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Delete Memory

**Endpoint**: `DELETE /api/memory/{id}`

**Response**:
```json
{
  "status": "ok",
  "data": {
    "id": 42,
    "deleted": true
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Dreaming API

### Get Dreaming Status

**Endpoint**: `GET /api/dreaming/status`

**Response**:
```json
{
  "status": "ok",
  "data": {
    "is_dreaming": false,
    "last_dream": "2024-01-15T08:00:00Z",
    "dream_frequency": "every_6_hours",
    "next_dream": "2024-01-15T14:00:00Z",
    "auto_dreaming": true
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Start Dream Cycle

**Endpoint**: `POST /api/dreaming/run`

**Request** (optional):
```json
{
  "focus": "optional-dream-topic"
}
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "dream_id": "dream-uuid",
    "started_at": "2024-01-15T10:30:00Z",
    "status": "processing"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Cancel Dream

**Endpoint**: `POST /api/dreaming/cancel`

**Response**:
```json
{
  "status": "ok",
  "data": {
    "dream_id": "dream-uuid",
    "cancelled_at": "2024-01-15T10:35:00Z"
  },
  "timestamp": "2024-01-15T10:35:00Z"
}
```

### Get Dream History

**Endpoint**: `GET /api/dreaming/history`

**Query Parameters**:
- `limit` (optional, default: 10)
- `offset` (optional, default: 0)

**Response**:
```json
{
  "status": "ok",
  "data": [
    {
      "id": "dream-uuid",
      "timestamp": "2024-01-15T08:00:00Z",
      "duration_seconds": 1200,
      "insights": "Dream revealed important patterns in memory",
      "new_connections": 3,
      "memories_processed": 15
    }
  ],
  "total": 45,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Tools API

### List Tools

**Endpoint**: `GET /api/tools/`

**Response**:
```json
{
  "status": "ok",
  "data": [
    {
      "name": "web_search",
      "description": "Search the web for information",
      "status": "active",
      "category": "external",
      "parameters": {
        "query": "string (required)",
        "limit": "integer (optional, default: 5)"
      },
      "last_used": "2024-01-15T09:30:00Z"
    },
    {
      "name": "code_execution",
      "description": "Execute Python code",
      "status": "active",
      "category": "utility",
      "parameters": {
        "code": "string (required)"
      },
      "last_used": "2024-01-14T16:20:00Z"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Tool Info

**Endpoint**: `GET /api/tools/{tool_name}`

**Response**:
```json
{
  "status": "ok",
  "data": {
    "name": "web_search",
    "description": "Search the web for information",
    "status": "active",
    "category": "external",
    "version": "1.0.0",
    "parameters": {
      "query": {
        "type": "string",
        "description": "Search query",
        "required": true,
        "example": "What is the capital of France?"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum results",
        "required": false,
        "default": 5
      }
    },
    "response_format": {
      "results": [
        {
          "title": "string",
          "url": "string",
          "snippet": "string"
        }
      ]
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Execute Tool

**Endpoint**: `POST /api/tools/{tool_name}/execute`

**Request**:
```json
{
  "query": "What is the weather in Paris?",
  "limit": 3
}
```

**Response**:
```json
{
  "status": "ok",
  "data": {
    "tool": "web_search",
    "execution_id": "exec-uuid",
    "result": {
      "results": [
        {
          "title": "Paris Weather",
          "url": "https://weather.example.com",
          "snippet": "Current temperature in Paris..."
        }
      ]
    },
    "execution_time_ms": 1234,
    "success": true
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Tool Status

**Endpoint**: `GET /api/tools/{tool_name}/status`

**Response**:
```json
{
  "status": "ok",
  "data": {
    "tool": "web_search",
    "status": "active",
    "health": "healthy",
    "last_checked": "2024-01-15T10:28:00Z",
    "stats": {
      "total_executions": 156,
      "failed_executions": 2,
      "avg_execution_time_ms": 450
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Discord API

### Get Discord Status

**Endpoint**: `GET /api/discord/status`

**Response**:
```json
{
  "status": "ok",
  "data": {
    "connected": true,
    "user_id": "discord-user-id",
    "username": "CortexBot",
    "guilds": 5,
    "uptime_seconds": 3600,
    "latency_ms": 45
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Test Discord Connection

**Endpoint**: `POST /api/discord/test-connection`

**Response**:
```json
{
  "status": "ok",
  "data": {
    "test_result": "success",
    "connected": true,
    "latency_ms": 42,
    "test_timestamp": "2024-01-15T10:30:00Z"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Discord Activity

**Endpoint**: `GET /api/discord/activity`

**Query Parameters**:
- `limit` (optional, default: 20)

**Response**:
```json
{
  "status": "ok",
  "data": [
    {
      "timestamp": "2024-01-15T10:25:00Z",
      "type": "message",
      "guild": "Guild Name",
      "channel": "general",
      "user": "Username",
      "action": "Message received",
      "details": "User asked about weather"
    }
  ],
  "total": 156,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "status": "error",
  "error": "Description of the error",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Missing/invalid authentication
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `409`: Conflict - Resource already exists
- `500`: Internal Server Error
- `503`: Service Unavailable

---

## Rate Limiting

Rate limits (development mode: unlimited):

- Chat: 30 requests/minute per user
- Memory: 60 requests/minute per user
- Tools: 20 requests/minute per tool
- Discord: 100 requests/minute

Response headers:
```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 28
X-RateLimit-Reset: 1642256400
```

---

## WebSocket API

For real-time chat streaming and updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'chat',
    message: 'Hello Cortex'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

---

## Pagination

Endpoints supporting pagination use these query parameters:

- `limit`: Number of items (default: 50, max: 100)
- `offset`: Number to skip (default: 0)

Example:
```
GET /api/memory/?limit=20&offset=40
```

Response includes:
```json
{
  "data": [...],
  "total": 250,
  "limit": 20,
  "offset": 40,
  "has_more": true
}
```
