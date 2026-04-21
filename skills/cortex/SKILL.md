# Cortex Master Skill

This is the master skill definition for the Cortex agent system.

## Overview

Cortex is a unified AI agent that coordinates:
- Chat interface interactions
- Memory management and consolidation
- Tool execution with approval gates
- Multi-channel communication (web UI, Discord, CLI)
- Model selection and switching

## Available Tools

### Memory Management
- `memory_list` — List all memories
- `memory_add` — Add a new memory entry
- `memory_promote` — Promote a memory to long-term storage
- `memory_delete` — Remove a memory entry
- `memory_search` — Search memory by keyword

### Dreaming
- `dreaming_start` — Begin a dreaming cycle
- `dreaming_status` — Check current dreaming phase
- `dreaming_cancel` — Cancel active dreaming

### Model Operations
- `model_list` — List available models
- `model_switch` — Switch to a different model
- `model_status` — Get current model info

### Tool Execution
- `tool_list` — List available tools
- `tool_execute` — Execute a tool with arguments
- `tool_status` — Get tool execution status

### Web Search
- `search` — Perform a web search
- `search_with_summary` — Search and summarize results

## Slash Commands

Users can trigger these commands in chat:

- `/help` — Show available commands and help
- `/memory [action] [args]` — Memory management
- `/dreaming [action]` — Dreaming control
- `/tools` — List available tools
- `/status` — Show system status
- `/search [query]` — Web search
- `/run [tool] [args]` — Execute a tool

## Configuration

Environment variables:
- `CORTEX_DEFAULT_MODEL` — Default model to use
- `OLLAMA_BASE_URL` — Ollama server URL
- `MEMORY_PATH` — Path to MEMORY.md
- `DREAMS_PATH` — Path to DREAMS.md
- `DREAMING_ENABLED` — Enable/disable dreaming
- `DREAMING_SCHEDULE` — Cron schedule for auto-dreaming

## Limits & Guards

- Memory entries: max 50,000 characters per entry
- Dreaming duration: max 5 minutes per cycle
- Tool execution: requires user confirmation
- API rate limiting: 100 requests per minute per user

## Examples

### Chat Example
```
User: /search cortex ai framework
Agent: [Performs web search and returns top results]

User: What should I remember?
Agent: Let me save this to your memory...

User: /dreaming status
Agent: Last dream cycle: 2 hours ago. Next scheduled: in 4 hours.
```

### CLI Example
```bash
cortex chat "What is Cortex?"
cortex memory list
cortex dreaming run
cortex tools list
```

## Architecture

Cortex uses a modular architecture:
- **Frontend**: SvelteKit UI with slash command support
- **Backend**: Python FastAPI with OpenClaw agent gateway
- **Agents**: Multi-level agent spawning for complex tasks
- **Memory**: File-based MEMORY.md + DREAMS.md
- **Discord**: Separate channel integration for async chat
- **CLI**: Python CLI client using REST API

See [ARCHITECTURE.md](../../ARCHITECTURE.md) for details.
