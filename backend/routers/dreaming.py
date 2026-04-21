# Source: NEW - Cortex Dreaming Router
# CORTEX MODIFICATION: REST API endpoints for dreaming cycle management with real consolidation

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
import logging

from open_webui.utils.auth import get_verified_user
from agents.dreaming_engine_real import dreaming_engine

log = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api/cortex/dreaming',
    tags=['cortex-dreaming'],
    dependencies=[Depends(get_verified_user)]
)


@router.get('/status')
async def get_dreaming_status(user=Depends(get_verified_user)):
    """Get current dreaming status"""
    try:
        result = await dreaming_engine.get_status(user_id=user.id)
        return result
    except Exception as e:
        log.error(f'Error getting dreaming status: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/run')
async def run_dream_cycle(
    focus: Optional[str] = Query(None),
    user=Depends(get_verified_user),
):
    """Manually trigger a dreaming cycle"""
    try:
        result = await dreaming_engine.start_dream_cycle(
            user_id=user.id, focus=focus
        )
        if result.get('status') == 'ok':
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get('message'))
    except HTTPException:
        raise
    except Exception as e:
        log.error(f'Error starting dream cycle: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/cancel')
async def cancel_dream_cycle(user=Depends(get_verified_user)):
    """Cancel current dreaming cycle"""
    try:
        result = await dreaming_engine.cancel_dream_cycle()
        return {'status': 'ok', 'data': result}
    except Exception as e:
        log.error(f'Error cancelling dream cycle: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/history')
async def get_dream_history(
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_verified_user),
):
    """Get dream history"""
    try:
        dreams = await dreaming_engine.get_dream_history(user_id=user.id, limit=limit)
        return {
            'status': 'ok',
            'data': dreams,
            'count': len(dreams),
        }
    except Exception as e:
        log.error(f'Error getting dream history: {e}')
        raise HTTPException(status_code=500, detail=str(e))
