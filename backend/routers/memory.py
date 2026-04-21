# Source: NEW - Cortex Memory Router
# CORTEX MODIFICATION: REST API endpoints for memory management with full database backing

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
import logging

from open_webui.utils.auth import get_verified_user
from models.cortex_memory import (
    cortex_memories,
    CortexMemoryCreate,
    CortexMemoryUpdate,
    CortexMemoryResponse,
    MemoryCategory,
    MemoryStatus,
)

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/cortex/memory",
    tags=["cortex-memory"],
    dependencies=[Depends(get_verified_user)],
)


@router.get("/", response_model=dict)
async def list_memories(
    user=Depends(get_verified_user),
    category: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """List all memories with optional filtering"""
    try:
        memories, total = cortex_memories.list_memories(
            user_id=user.id,
            category=category,
            status=status_filter,
            limit=limit,
            offset=offset,
        )
        return {
            "status": "ok",
            "data": memories,
            "count": len(memories),
            "total": total,
            "offset": offset,
        }
    except Exception as e:
        log.error(f"Error listing memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add", response_model=dict)
async def add_memory(
    entry: CortexMemoryCreate, user=Depends(get_verified_user)
):
    """Add a new memory entry"""
    try:
        memory = cortex_memories.add_memory(
            user_id=user.id,
            category=entry.category,
            title=entry.title,
            content=entry.content,
            importance=entry.importance,
            source=entry.source,
            tags=entry.tags,
        )
        if memory:
            return {"status": "ok", "data": memory}
        else:
            raise HTTPException(status_code=500, detail="Failed to create memory")
    except Exception as e:
        log.error(f"Error adding memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{memory_id}", response_model=dict)
async def get_memory(memory_id: str, user=Depends(get_verified_user)):
    """Get a specific memory"""
    try:
        memory = cortex_memories.get_memory(memory_id=memory_id, user_id=user.id)
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "ok", "data": memory}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{memory_id}", response_model=dict)
async def update_memory(
    memory_id: str,
    update_data: CortexMemoryUpdate,
    user=Depends(get_verified_user),
):
    """Update a memory"""
    try:
        memory = cortex_memories.update_memory(
            memory_id=memory_id, user_id=user.id, update_data=update_data
        )
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "ok", "data": memory}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error updating memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/promote/{memory_id}", response_model=dict)
async def promote_memory(memory_id: str, user=Depends(get_verified_user)):
    """Promote memory to long-term storage"""
    try:
        memory = cortex_memories.promote_memory(memory_id=memory_id, user_id=user.id)
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "ok", "data": memory}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error promoting memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{memory_id}')
async def delete_memory(memory_id: str, user=Depends(get_verified_user)):
    """Delete a memory entry"""
    try:
        success = cortex_memories.delete_memory(memory_id=memory_id, user_id=user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "ok", "data": {"deleted": memory_id}}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error deleting memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/search')
async def search_memories(query: str = Query(...), category: Optional[str] = Query(None), limit: int = Query(50, ge=1, le=200), user=Depends(get_verified_user)):
    """Search memory entries"""
    try:
        results = cortex_memories.search_memories(
            user_id=user.id, query=query, category=category, limit=limit
        )
        return {'status': 'ok', 'query': query, 'data': results, 'count': len(results)}
    except Exception as e:
        log.error(f'Error searching memories: {e}')
        raise HTTPException(status_code=500, detail=str(e))
