"""Cortex Memory Model - Extended memory system with categories and importance scoring"""

import time
import uuid
from typing import Optional
from enum import Enum

from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Text, Integer, BigInteger, Float, Index
from pydantic import BaseModel, ConfigDict

from open_webui.internal.db import Base, get_db, get_db_context


# Memory Categories
class MemoryCategory(str, Enum):
    KNOWLEDGE = "knowledge"
    EVENTS = "events"
    PREFERENCES = "preferences"
    SKILLS = "skills"
    RELATIONSHIPS = "relationships"
    GOALS = "goals"
    INSIGHTS = "insights"


# Memory Status (lifecycle)
class MemoryStatus(str, Enum):
    TRANSIENT = "transient"  # Short-term, may be forgotten
    GROUNDED = "grounded"    # Regular memory
    PROMOTED = "promoted"    # Important, long-term storage
    ARCHIVED = "archived"    # Old but kept for reference


#####################
# Database Models
#####################


class CortexMemory(Base):
    """Extended memory model with categories, importance, and metadata"""
    __tablename__ = "cortex_memory"

    id = Column(String, primary_key=True, unique=True)
    user_id = Column(String, nullable=False, index=True)
    category = Column(String, default="knowledge")
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    importance = Column(Integer, default=5)  # 1-10 scale
    status = Column(String, default="grounded")
    source = Column(String, nullable=True)  # Where this memory came from (chat, tool, etc)
    tags = Column(Text, nullable=True)  # Comma-separated tags for grouping
    embedding_vector = Column(Text, nullable=True)  # For semantic search
    related_memories = Column(Text, nullable=True)  # JSON list of related memory IDs
    accessed_count = Column(Integer, default=0)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    last_accessed = Column(BigInteger, nullable=True)

    __table_args__ = (
        Index("idx_user_category", "user_id", "category"),
        Index("idx_user_importance", "user_id", "importance"),
        Index("idx_user_status", "user_id", "status"),
    )


class CortexDream(Base):
    """Dreams record - consolidation sessions and insights"""
    __tablename__ = "cortex_dream"

    id = Column(String, primary_key=True, unique=True)
    user_id = Column(String, nullable=False, index=True)
    dream_duration_seconds = Column(Integer)
    phase = Column(String)  # light_sleep, deep_sleep, REM, etc
    memories_reviewed = Column(Integer, default=0)
    memories_consolidated = Column(Integer, default=0)
    insights_generated = Column(Text)  # JSON list of insights
    new_connections = Column(Integer, default=0)  # Memory connections made
    status = Column(String, default="complete")
    created_at = Column(BigInteger)


#####################
# Pydantic Models
#####################


class CortexMemoryCreate(BaseModel):
    """Create a new memory"""
    category: str = "knowledge"
    title: str
    content: str
    importance: int = 5
    source: Optional[str] = None
    tags: Optional[str] = None


class CortexMemoryUpdate(BaseModel):
    """Update a memory"""
    title: Optional[str] = None
    content: Optional[str] = None
    importance: Optional[int] = None
    status: Optional[str] = None
    category: Optional[str] = None


class CortexMemoryResponse(BaseModel):
    """Memory response model"""
    id: str
    user_id: str
    category: str
    title: str
    content: str
    importance: int
    status: str
    source: Optional[str]
    tags: Optional[str]
    created_at: int
    updated_at: int
    last_accessed: Optional[int]
    accessed_count: int

    model_config = ConfigDict(from_attributes=True)


class CortexDreamResponse(BaseModel):
    """Dream response model"""
    id: str
    user_id: str
    dream_duration_seconds: int
    memories_reviewed: int
    memories_consolidated: int
    new_connections: int
    status: str
    created_at: int
    insights_generated: Optional[str]

    model_config = ConfigDict(from_attributes=True)


#####################
# Database Operations
#####################


class CortexMemoriesTable:
    """Database operations for Cortex memories"""

    def add_memory(
        self,
        user_id: str,
        category: str,
        title: str,
        content: str,
        importance: int = 5,
        source: Optional[str] = None,
        tags: Optional[str] = None,
        db: Optional[Session] = None,
    ) -> Optional[CortexMemoryResponse]:
        """Add a new memory to the database"""
        with get_db_context(db) as db:
            memory_id = str(uuid.uuid4())
            now = int(time.time())

            memory = CortexMemory(
                id=memory_id,
                user_id=user_id,
                category=category,
                title=title,
                content=content,
                importance=max(1, min(10, importance)),  # Clamp 1-10
                status="grounded",
                source=source,
                tags=tags,
                created_at=now,
                updated_at=now,
            )

            db.add(memory)
            db.commit()
            db.refresh(memory)

            return CortexMemoryResponse.model_validate(memory)

    def list_memories(
        self,
        user_id: str,
        category: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        db: Optional[Session] = None,
    ) -> tuple[list[CortexMemoryResponse], int]:
        """List memories with optional filtering"""
        with get_db_context(db) as db:
            query = db.query(CortexMemory).filter(CortexMemory.user_id == user_id)

            if category:
                query = query.filter(CortexMemory.category == category)
            if status:
                query = query.filter(CortexMemory.status == status)

            total = query.count()
            memories = query.order_by(CortexMemory.updated_at.desc()).limit(limit).offset(offset).all()

            return [CortexMemoryResponse.model_validate(m) for m in memories], total

    def get_memory(
        self, memory_id: str, user_id: str, db: Optional[Session] = None
    ) -> Optional[CortexMemoryResponse]:
        """Get a specific memory"""
        with get_db_context(db) as db:
            memory = db.query(CortexMemory).filter(
                CortexMemory.id == memory_id,
                CortexMemory.user_id == user_id,
            ).first()

            if memory:
                # Update accessed count
                memory.accessed_count += 1
                memory.last_accessed = int(time.time())
                db.commit()
                db.refresh(memory)
                return CortexMemoryResponse.model_validate(memory)
            return None

    def update_memory(
        self,
        memory_id: str,
        user_id: str,
        update_data: CortexMemoryUpdate,
        db: Optional[Session] = None,
    ) -> Optional[CortexMemoryResponse]:
        """Update a memory"""
        with get_db_context(db) as db:
            memory = db.query(CortexMemory).filter(
                CortexMemory.id == memory_id,
                CortexMemory.user_id == user_id,
            ).first()

            if not memory:
                return None

            for key, value in update_data.model_dump(exclude_unset=True).items():
                if key == "importance" and value:
                    value = max(1, min(10, value))  # Clamp 1-10
                if value is not None:
                    setattr(memory, key, value)

            memory.updated_at = int(time.time())
            db.commit()
            db.refresh(memory)
            return CortexMemoryResponse.model_validate(memory)

    def promote_memory(
        self, memory_id: str, user_id: str, db: Optional[Session] = None
    ) -> Optional[CortexMemoryResponse]:
        """Promote memory to long-term storage"""
        return self.update_memory(
            memory_id,
            user_id,
            CortexMemoryUpdate(status="promoted"),
            db,
        )

    def delete_memory(
        self, memory_id: str, user_id: str, db: Optional[Session] = None
    ) -> bool:
        """Delete a memory"""
        with get_db_context(db) as db:
            memory = db.query(CortexMemory).filter(
                CortexMemory.id == memory_id,
                CortexMemory.user_id == user_id,
            ).first()

            if not memory:
                return False

            db.delete(memory)
            db.commit()
            return True

    def search_memories(
        self,
        user_id: str,
        query: str,
        category: Optional[str] = None,
        limit: int = 50,
        db: Optional[Session] = None,
    ) -> list[CortexMemoryResponse]:
        """Search memories by keywords"""
        with get_db_context(db) as db:
            q = db.query(CortexMemory).filter(CortexMemory.user_id == user_id)

            if category:
                q = q.filter(CortexMemory.category == category)

            # Search in title, content, and tags
            query_lower = query.lower()
            results = []
            for memory in q.all():
                if (
                    query_lower in memory.title.lower()
                    or query_lower in memory.content.lower()
                    or (memory.tags and query_lower in memory.tags.lower())
                ):
                    results.append(memory)

            # Sort by importance and recency
            results.sort(
                key=lambda x: (x.importance, x.updated_at), reverse=True
            )

            return [CortexMemoryResponse.model_validate(m) for m in results[:limit]]

    def get_important_memories(
        self,
        user_id: str,
        min_importance: int = 7,
        limit: int = 50,
        db: Optional[Session] = None,
    ) -> list[CortexMemoryResponse]:
        """Get important memories (for dreaming, etc)"""
        with get_db_context(db) as db:
            memories = (
                db.query(CortexMemory)
                .filter(
                    CortexMemory.user_id == user_id,
                    CortexMemory.importance >= min_importance,
                )
                .order_by(CortexMemory.updated_at.desc())
                .limit(limit)
                .all()
            )
            return [CortexMemoryResponse.model_validate(m) for m in memories]


# Singleton instance
cortex_memories = CortexMemoriesTable()
