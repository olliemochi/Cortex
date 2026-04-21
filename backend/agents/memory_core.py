# Source: openclaw/src/memory-host-sdk/ (adapted)
# CORTEX MODIFICATION: Memory management core for Cortex

import asyncio
import logging
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)


class MemoryCore:
    """
    Manages long-term memory stored in MEMORY.md
    Handles reading, writing, searching, and promoting/demoting memory entries.
    """
    
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
        self.entries = []
        log.info(f'MemoryCore initialized with path: {memory_path}')
    
    async def initialize(self):
        """Load memory from file on startup"""
        await self._load_memory()
    
    async def _load_memory(self):
        """Load MEMORY.md from disk"""
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, 'r') as f:
                    content = f.read()
                self.entries = self._parse_memory_entries(content)
                log.info(f'Loaded {len(self.entries)} memory entries')
            else:
                log.warning(f'Memory file not found: {self.memory_path}')
                self.entries = []
        except Exception as e:
            log.error(f'Error loading memory: {e}')
            self.entries = []
    
    async def add_entry(self, category: str, title: str, content: str, importance: int = 5) -> bool:
        """Add a new memory entry"""
        try:
            entry = {
                'category': category,
                'title': title,
                'content': content,
                'importance': importance,
                'date': datetime.now().isoformat(),
                'status': 'grounded'
            }
            self.entries.append(entry)
            await self._save_memory()
            return True
        except Exception as e:
            log.error(f'Error adding memory entry: {e}')
            return False
    
    async def promote_entry(self, entry_id: int) -> bool:
        """Promote entry from short-term to long-term memory"""
        try:
            if 0 <= entry_id < len(self.entries):
                self.entries[entry_id]['status'] = 'promoted'
                await self._save_memory()
                return True
            return False
        except Exception as e:
            log.error(f'Error promoting memory entry: {e}')
            return False
    
    async def delete_entry(self, entry_id: int) -> bool:
        """Delete a memory entry"""
        try:
            if 0 <= entry_id < len(self.entries):
                self.entries.pop(entry_id)
                await self._save_memory()
                return True
            return False
        except Exception as e:
            log.error(f'Error deleting memory entry: {e}')
            return False
    
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """Search memory entries by keyword"""
        results = []
        query_lower = query.lower()
        for entry in self.entries:
            if (query_lower in entry['title'].lower() or 
                query_lower in entry['content'].lower() or
                query_lower in entry['category'].lower()):
                results.append(entry)
        return results
    
    async def get_all(self) -> List[Dict[str, Any]]:
        """Get all memory entries"""
        return self.entries
    
    async def _save_memory(self):
        """Save memory entries to file"""
        try:
            with open(self.memory_path, 'w') as f:
                f.write('# Cortex Memory\n\n')
                for i, entry in enumerate(self.entries):
                    f.write(f"## [{entry['category']}] - {entry['title']}\n")
                    f.write(f"- **Date**: {entry['date']}\n")
                    f.write(f"- **Status**: {entry['status']}\n")
                    f.write(f"- **Importance**: {entry['importance']}\n")
                    f.write(f"- **Content**: {entry['content']}\n\n")
            log.debug(f'Saved {len(self.entries)} memory entries to disk')
        except Exception as e:
            log.error(f'Error saving memory: {e}')
    
    def _parse_memory_entries(self, content: str) -> List[Dict[str, Any]]:
        """Parse MEMORY.md file into entry objects"""
        entries = []
        current_entry = None
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Look for section headers (## [CATEGORY] - Title)
            if line.startswith('## ['):
                # Save previous entry if exists
                if current_entry:
                    entries.append(current_entry)
                
                # Parse new entry header
                try:
                    # Format: ## [category] - title
                    bracket_end = line.find(']')
                    if bracket_end > 3:
                        category = line[4:bracket_end]  # Extract from [...]
                        title = line[bracket_end+4:].strip()  # Skip "] - "
                        
                        current_entry = {
                            'category': category,
                            'title': title,
                            'date': '',
                            'status': 'grounded',
                            'importance': 5,
                            'content': ''
                        }
                except Exception as e:
                    log.debug(f'Error parsing entry header: {e}')
            
            # Parse entry metadata
            elif current_entry and line.startswith('- **'):
                try:
                    # Format: - **Key**: Value
                    key_end = line.find('**:', 4)
                    if key_end > 0:
                        key = line[4:key_end].lower().replace(' ', '_')
                        value = line[key_end+3:].strip()
                        
                        if key == 'date':
                            current_entry['date'] = value
                        elif key == 'status':
                            current_entry['status'] = value
                        elif key == 'importance':
                            try:
                                current_entry['importance'] = int(value)
                            except ValueError:
                                pass
                        elif key == 'content':
                            current_entry['content'] = value
                except Exception as e:
                    log.debug(f'Error parsing entry metadata: {e}')
            
            # Append content lines to current entry
            elif current_entry and line.strip() and not line.startswith('#'):
                if current_entry['content']:
                    current_entry['content'] += f'\n{line}'
                else:
                    current_entry['content'] = line
        
        # Save last entry
        if current_entry:
            entries.append(current_entry)
        
        return entries
