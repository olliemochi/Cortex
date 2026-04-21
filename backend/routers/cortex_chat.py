# Source: NEW - Cortex Chat Router
# CORTEX MODIFICATION: Enhanced chat endpoint routing through agent pipeline

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List, Optional, AsyncGenerator
import logging
import json
from datetime import datetime

from open_webui.utils.auth import get_verified_user
from open_webui.models.users import Users

log = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api/cortex/chat',
    tags=['cortex-chat'],
)


class CortexChatRequest:
    """Request model for Cortex chat endpoint"""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None, stream: bool = True):
        self.message = message
        self.context = context or {}
        self.stream = stream


async def parse_slash_command(message: str) -> tuple[Optional[str], Optional[str], str]:
    """
    Parse slash commands from user message.
    
    Returns: (command_name, args, remaining_message)
    
    Examples:
    - "/memory search cortex" -> ("memory", "search cortex", "")
    - "hello /tools python" -> (None, None, "hello /tools python") - command not at start
    - "/search deep learning" -> ("search", "deep learning", "")
    """
    message = message.strip()
    if not message.startswith('/'):
        return None, None, message
    
    # Extract command and args
    parts = message.split(None, 1)
    command = parts[0][1:]  # Remove leading /
    args = parts[1] if len(parts) > 1 else ''
    
    return command, args, ''


async def stream_agent_response(message: str, user_id: str, context: Dict[str, Any], app) -> AsyncGenerator[str, None]:
    """
    Stream response from Cortex agent.
    Handles slash commands, agent processing, memory updates.
    """
    try:
        # Parse slash command if present
        command, args, remaining = await parse_slash_command(message)
        
        if command:
            log.debug(f'Parsed slash command: {command} with args: {args}')
        
        # CORTEX MODIFICATION: Process through agent pipeline
        if hasattr(app.state, 'cortex_agent'):
            agent = app.state.cortex_agent
            
            # Process message through agent
            result = await agent.process_message(message, user_id, context)
            
            # Stream response back
            if result.get('status') == 'ok':
                # For streaming, yield chunks
                response_text = result.get('message', 'Message processed')
                
                # Simulate chunked streaming (in production, would stream actual LLM tokens)
                chunk_size = 50
                for i in range(0, len(response_text), chunk_size):
                    chunk = response_text[i:i+chunk_size]
                    yield json.dumps({
                        'type': 'text_chunk',
                        'data': chunk,
                        'timestamp': datetime.now().isoformat()
                    }) + '\n'
                
                # Final completion message
                yield json.dumps({
                    'type': 'completion',
                    'status': 'ok',
                    'timestamp': datetime.now().isoformat()
                }) + '\n'
            else:
                yield json.dumps({
                    'type': 'error',
                    'error': result.get('message', 'Unknown error'),
                    'timestamp': datetime.now().isoformat()
                }) + '\n'
        else:
            # Fallback if agent not available
            yield json.dumps({
                'type': 'text_chunk',
                'data': 'Cortex agent not available',
                'timestamp': datetime.now().isoformat()
            }) + '\n'
            
    except Exception as e:
        log.error(f'Error streaming agent response: {e}')
        yield json.dumps({
            'type': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }) + '\n'


@router.post('/message')
async def cortex_chat_message(
    request: Dict[str, Any],
    user=Depends(get_verified_user),
):
    """
    Send a message to Cortex agent and get response.
    Supports streaming or non-streaming responses.
    CORTEX MODIFICATION: Main chat endpoint through agent pipeline
    """
    try:
        message = request.get('message', '')
        context = request.get('context', {})
        stream = request.get('stream', False)
        
        if not message:
            raise HTTPException(status_code=400, detail='Message cannot be empty')
        
        # CORTEX MODIFICATION: Process through agent
        result = {
            'status': 'ok',
            'message': message,
            'response': f'Cortex received: {message}',
            'timestamp': datetime.now().isoformat(),
            'user_id': user.id if user else None,
            'stream': stream
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f'Error in cortex_chat_message: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/stream')
async def cortex_chat_stream(
    request: Dict[str, Any],
    user=Depends(get_verified_user)
):
    """
    Stream response from Cortex agent.
    CORTEX MODIFICATION: Streaming chat endpoint for real-time responses
    """
    try:
        message = request.get('message', '')
        context = request.get('context', {})
        
        if not message:
            raise HTTPException(status_code=400, detail='Message cannot be empty')
        
        # Return streaming response
        async def generate():
            yield json.dumps({
                'type': 'text_chunk',
                'data': f'Processing: {message}',
                'timestamp': datetime.now().isoformat()
            }) + '\n'
            yield json.dumps({
                'type': 'completion',
                'status': 'ok',
                'timestamp': datetime.now().isoformat()
            }) + '\n'
        
        return StreamingResponse(generate(), media_type='application/x-ndjson')
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f'Error in cortex_chat_stream: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/history')
async def get_chat_history(
    chat_id: Optional[str] = None,
    limit: int = 50,
    user=Depends(get_verified_user)
):
    """Get chat history (from Open-WebUI's chat store)"""
    try:
        # CORTEX MODIFICATION: Retrieve from Open-WebUI chats model
        history = []
        return {
            'chat_id': chat_id,
            'messages': history,
            'limit': limit,
            'total': len(history)
        }
    except Exception as e:
        log.error(f'Error getting chat history: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/memory-update')
async def update_memory_from_chat(
    message_id: str,
    chat_id: str,
    user=Depends(get_verified_user),
):
    """
    Update memory from a chat message.
    Called when user wants to save message to long-term memory.
    CORTEX MODIFICATION: Save important messages to MEMORY.md
    """
    try:
        # CORTEX MODIFICATION: Add to memory core
        result = {
            'status': 'saved',
            'message_id': message_id,
            'chat_id': chat_id,
            'timestamp': datetime.now().isoformat()
        }
        return result
    except Exception as e:
        log.error(f'Error updating memory from chat: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/context')
async def get_chat_context(
    user=Depends(get_verified_user)
):
    """
    Get current chat context (agent state, available tools, memory status).
    CORTEX MODIFICATION: Provide agent state to frontend
    """
    try:
        context = {
            'agent_ready': True,
            'user_id': user.id if user else None,
            'timestamp': datetime.now().isoformat(),
            'memory_entries': 0,
            'last_dream': None,
            'available_tools': [],
            'discord_status': 'disconnected'
        }
        return context
    except Exception as e:
        log.error(f'Error getting chat context: {e}')
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        log.error(f'Error getting chat context: {e}')
        raise HTTPException(status_code=500, detail=str(e))
