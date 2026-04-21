# Source: NEW - Cortex Tools Router (Agent-based)
# CORTEX MODIFICATION: Agent-based tool/skill execution with real implementations

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List, Optional
import logging

from open_webui.utils.auth import get_verified_user
from agents.tool_executor import cortex_tools

log = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api/cortex/tools',
    tags=['cortex-tools'],
    dependencies=[Depends(get_verified_user)]
)


@router.get('/')
async def list_tools(user=Depends(get_verified_user)):
    """List all available Cortex tools/skills"""
    try:
        tools = await cortex_tools.list_tools()
        return {'status': 'ok', 'data': tools, 'count': len(tools)}
    except Exception as e:
        log.error(f'Error listing tools: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{tool_name}')
async def get_tool_info(tool_name: str, user=Depends(get_verified_user)):
    """Get information about a specific Cortex tool"""
    try:
        tool_info = await cortex_tools.get_tool_info(tool_name)
        if not tool_info:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        return {'status': 'ok', 'data': tool_info}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f'Error getting tool info: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{tool_name}/execute')
async def execute_tool(tool_name: str, args: Dict[str, Any], user=Depends(get_verified_user)):
    """Execute a Cortex tool with specified arguments"""
    try:
        result = await cortex_tools.execute_tool(tool_name, args, user_id=user.id)
        if result.success:
            return {'status': 'ok', 'data': result.to_dict()}
        else:
            raise HTTPException(status_code=400, detail=result.error)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f'Error executing tool: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{tool_name}/status')
async def get_tool_status(tool_name: str, user=Depends(get_verified_user)):
    """Get Cortex tool execution status"""
    try:
        tool_info = await cortex_tools.get_tool_info(tool_name)
        if not tool_info:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        # Get execution history
        history = await cortex_tools.get_execution_history(user_id=user.id, limit=10)
        tool_history = [h for h in history if h['tool'] == tool_name]
        
        return {
            'status': 'ok',
            'data': {
                'tool': tool_name,
                'active': False,
                'last_executions': tool_history[:5],
                'info': tool_info
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f'Error getting tool status: {e}')
        raise HTTPException(status_code=500, detail=str(e))
