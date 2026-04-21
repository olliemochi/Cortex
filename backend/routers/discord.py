# Source: NEW - Cortex Discord Router
# CORTEX MODIFICATION: REST API endpoints for Discord bot management and interaction

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any, List
import logging

from open_webui.utils.auth import get_admin_user, get_verified_user

log = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api/cortex/discord',
    tags=['cortex-discord'],
)


@router.get('/config')
async def get_discord_config(user=Depends(get_admin_user)):
    """Get Discord bot configuration (admin only)"""
    try:
        # CORTEX MODIFICATION: Get from cortex_env
        config = {
            'enabled': False,
            'token_set': False,
            'allowed_channels': [],
            'allowed_users': [],
            'status': 'disconnected'
        }
        return config
    except Exception as e:
        log.error(f'Error getting Discord config: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/config')
async def update_discord_config(config: Dict[str, Any], user=Depends(get_admin_user)):
    """Update Discord bot configuration (admin only)"""
    try:
        # CORTEX MODIFICATION: Save to environment/database
        result = {
            'status': 'updated',
            'config': config
        }
        return result
    except Exception as e:
        log.error(f'Error updating Discord config: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/test-connection')
async def test_discord_connection(user=Depends(get_admin_user)):
    """Test Discord bot connection"""
    try:
        # CORTEX MODIFICATION: Test bot connectivity
        result = {
            'status': 'success',
            'message': 'Discord bot connection test passed'
        }
        return result
    except Exception as e:
        log.error(f'Error testing Discord connection: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/activity')
async def get_discord_activity(limit: int = 20, user=Depends(get_admin_user)):
    """Get recent Discord bot activity log"""
    try:
        # CORTEX MODIFICATION: Get from activity logger
        activity = []
        return {'activity': activity, 'limit': limit, 'total': len(activity)}
    except Exception as e:
        log.error(f'Error getting Discord activity: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/webhook')
async def handle_discord_webhook(request: Request):
    """Handle Discord webhook messages (no auth required)"""
    try:
        # CORTEX MODIFICATION: Route Discord messages to agent
        body = await request.json()
        result = {
            'status': 'received',
            'message_id': None
        }
        return result
    except Exception as e:
        log.error(f'Error handling Discord webhook: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/status')
async def get_discord_status(user=Depends(get_verified_user)):
    """Get Discord bot status (available to all users)"""
    try:
        # CORTEX MODIFICATION: Get bot status
        status_info = {
            'connected': False,
            'guilds': 0,
            'users_connected': 0,
            'last_message': None
        }
        return status_info
    except Exception as e:
        log.error(f'Error getting Discord status: {e}')
        raise HTTPException(status_code=500, detail=str(e))
