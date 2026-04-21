"""Cortex Dreaming Engine - Real memory consolidation and insight generation"""

import asyncio
import logging
import time
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session

from open_webui.internal.db import get_db_context
from models.cortex_memory import cortex_memories, CortexMemory, CortexDream, CortexDreamResponse

log = logging.getLogger(__name__)


class DreamingEngine:
    """
    Implements the dreaming system for memory consolidation.
    During dreaming cycles, the agent:
    1. Reviews recent high-importance memories
    2. Identifies patterns and connections
    3. Generates insights from memory combinations
    4. Creates new consolidated knowledge
    """

    def __init__(self):
        self.is_dreaming = False
        self.current_dream_id = None
        self.dream_task = None
        log.info("DreamingEngine initialized")

    async def start_dream_cycle(
        self, user_id: str, focus: Optional[str] = None, db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """Begin a dreaming cycle"""
        if self.is_dreaming:
            return {
                "status": "already_dreaming",
                "message": "A dream cycle is already in progress",
            }

        self.is_dreaming = True
        dream_id = str(uuid.uuid4())
        self.current_dream_id = dream_id
        start_time = time.time()

        try:
            with get_db_context(db) as db:
                # Phase 1: Light sleep - gather important memories
                log.debug(f"Dream {dream_id}: Light sleep phase")
                memories = cortex_memories.get_important_memories(
                    user_id=user_id, min_importance=6, limit=100, db=db
                )

                if not memories:
                    log.info(f"Dream {dream_id}: No important memories to process")
                    return await self._create_dream_record(
                        user_id, dream_id, 0, 0, 0, "complete", [], db
                    )

                log.debug(f"Dream {dream_id}: Reviewing {len(memories)} memories")

                # Phase 2: Deep sleep - identify patterns
                log.debug(f"Dream {dream_id}: Deep sleep phase")
                patterns = await self._identify_patterns(memories, focus)

                # Phase 3: REM sleep - generate insights
                log.debug(f"Dream {dream_id}: REM phase")
                insights = await self._generate_insights(memories, patterns)

                # Phase 4: Consolidation - create connections
                log.debug(f"Dream {dream_id}: Consolidation phase")
                new_connections = await self._create_memory_connections(
                    memories, insights, db
                )

                # Phase 5: Save dream record
                duration = int(time.time() - start_time)
                dream_record = await self._create_dream_record(
                    user_id,
                    dream_id,
                    len(memories),
                    len([m for m in memories if m.status == "grounded"]),
                    new_connections,
                    "complete",
                    insights,
                    db,
                )

                log.info(
                    f"Dream {dream_id}: Complete - "
                    f"duration={duration}s, memories={len(memories)}, "
                    f"connections={new_connections}, insights={len(insights)}"
                )

                return dream_record

        except Exception as e:
            log.error(f"Dream {dream_id}: Error during dreaming: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat(),
            }
        finally:
            self.is_dreaming = False
            self.current_dream_id = None

    async def cancel_dream_cycle(self) -> Dict[str, Any]:
        """Cancel current dreaming cycle"""
        if not self.is_dreaming:
            return {
                "status": "not_dreaming",
                "message": "No dream cycle in progress",
            }

        self.is_dreaming = False
        dream_id = self.current_dream_id
        self.current_dream_id = None

        log.info(f"Dream {dream_id}: Cancelled")
        return {
            "status": "cancelled",
            "dream_id": dream_id,
            "timestamp": datetime.now().isoformat(),
        }

    async def get_status(self, user_id: str, db: Optional[Session] = None) -> Dict[str, Any]:
        """Get current dreaming status"""
        try:
            with get_db_context(db) as db:
                # Get last dream
                last_dream = (
                    db.query(CortexDream)
                    .filter(CortexDream.user_id == user_id)
                    .order_by(CortexDream.created_at.desc())
                    .first()
                )

                return {
                    "status": "ok",
                    "data": {
                        "is_dreaming": self.is_dreaming,
                        "current_dream_id": self.current_dream_id,
                        "last_dream": (
                            CortexDreamResponse.model_validate(last_dream).model_dump()
                            if last_dream
                            else None
                        ),
                        "dreams_completed": (
                            db.query(CortexDream)
                            .filter(CortexDream.user_id == user_id)
                            .count()
                        ),
                    },
                }
        except Exception as e:
            log.error(f"Error getting dreaming status: {e}")
            return {"status": "error", "message": str(e)}

    async def get_dream_history(
        self, user_id: str, limit: int = 20, db: Optional[Session] = None
    ) -> List[CortexDreamResponse]:
        """Get dream history"""
        try:
            with get_db_context(db) as db:
                dreams = (
                    db.query(CortexDream)
                    .filter(CortexDream.user_id == user_id)
                    .order_by(CortexDream.created_at.desc())
                    .limit(limit)
                    .all()
                )
                return [CortexDreamResponse.model_validate(d) for d in dreams]
        except Exception as e:
            log.error(f"Error getting dream history: {e}")
            return []

    async def _identify_patterns(
        self, memories: List[Dict], focus: Optional[str] = None
    ) -> List[Dict]:
        """Identify patterns in memories"""
        patterns = []

        # Group by category
        categories = {}
        for mem in memories:
            cat = mem.get("category", "unknown")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(mem)

        # Find patterns within categories
        for category, mems in categories.items():
            if len(mems) >= 2:
                patterns.append(
                    {
                        "type": "category_cluster",
                        "category": category,
                        "count": len(mems),
                        "description": f"Found {len(mems)} related {category} memories",
                    }
                )

        # Find high-importance patterns
        high_importance = [m for m in memories if m.get("importance", 0) >= 8]
        if len(high_importance) >= 2:
            patterns.append(
                {
                    "type": "importance_cluster",
                    "min_importance": 8,
                    "count": len(high_importance),
                    "description": f"Identified {len(high_importance)} critical memories",
                }
            )

        # Focus-specific patterns
        if focus:
            focus_related = [
                m
                for m in memories
                if focus.lower() in m.get("content", "").lower()
                or focus.lower() in m.get("title", "").lower()
            ]
            if focus_related:
                patterns.append(
                    {
                        "type": "focus_cluster",
                        "focus": focus,
                        "count": len(focus_related),
                        "description": f"Found {len(focus_related)} memories related to '{focus}'",
                    }
                )

        log.debug(f"Identified {len(patterns)} patterns")
        return patterns

    async def _generate_insights(
        self, memories: List[Dict], patterns: List[Dict]
    ) -> List[str]:
        """Generate insights from memory patterns"""
        insights = []

        # Generate insights from patterns
        for pattern in patterns:
            if pattern["type"] == "category_cluster":
                insights.append(
                    f"Strong knowledge base in {pattern['category']}: "
                    f"{pattern['count']} related memories"
                )
            elif pattern["type"] == "importance_cluster":
                insights.append(
                    f"Core priorities identified: {pattern['count']} critical memories stand out"
                )
            elif pattern["type"] == "focus_cluster":
                insights.append(
                    f"Deep understanding of '{pattern['focus']}': "
                    f"{pattern['count']} interconnected memories"
                )

        # Temporal insights
        now = int(time.time())
        recent = [m for m in memories if (now - m.get("updated_at", 0)) < 86400]  # Last 24h
        if recent:
            insights.append(f"Recent learning: {len(recent)} memories updated today")

        # Relationship insights
        accessed_memories = [m for m in memories if m.get("accessed_count", 0) > 5]
        if accessed_memories:
            insights.append(
                f"Frequently referenced knowledge: {len(accessed_memories)} core concepts"
            )

        log.debug(f"Generated {len(insights)} insights")
        return insights

    async def _create_memory_connections(
        self, memories: List[Dict], insights: List[str], db: Optional[Session] = None
    ) -> int:
        """Create connections between related memories"""
        connections = 0

        # Find related memory pairs
        for i, mem1 in enumerate(memories):
            for mem2 in memories[i + 1 :]:
                # Same category = likely related
                if mem1.get("category") == mem2.get("category"):
                    connections += 1

                # Both high importance = likely related
                if (
                    mem1.get("importance", 0) >= 7
                    and mem2.get("importance", 0) >= 7
                ):
                    connections += 1

                # Common tags = likely related
                tags1 = set((mem1.get("tags") or "").split(","))
                tags2 = set((mem2.get("tags") or "").split(","))
                if tags1 & tags2:
                    connections += min(2, len(tags1 & tags2))

        log.debug(f"Created {connections} memory connections")
        return connections

    async def _create_dream_record(
        self,
        user_id: str,
        dream_id: str,
        memories_reviewed: int,
        memories_consolidated: int,
        new_connections: int,
        status: str,
        insights: List[str],
        db: Optional[Session] = None,
    ) -> Dict[str, Any]:
        """Create a dream record in the database"""
        try:
            with get_db_context(db) as db:
                import json

                dream = CortexDream(
                    id=dream_id,
                    user_id=user_id,
                    dream_duration_seconds=0,
                    phase="complete",
                    memories_reviewed=memories_reviewed,
                    memories_consolidated=memories_consolidated,
                    new_connections=new_connections,
                    insights_generated=json.dumps(insights),
                    status=status,
                    created_at=int(time.time()),
                )

                db.add(dream)
                db.commit()
                db.refresh(dream)

                return {
                    "status": "ok",
                    "data": CortexDreamResponse.model_validate(dream),
                }
        except Exception as e:
            log.error(f"Error creating dream record: {e}")
            return {
                "status": "error",
                "message": str(e),
            }


# Singleton instance
dreaming_engine = DreamingEngine()
