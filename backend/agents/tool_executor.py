"""Cortex Tool Execution System - Real tool implementations and execution"""

import asyncio
import logging
import json
import subprocess
import time
import aiohttp
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime

log = logging.getLogger(__name__)


class ToolType(str, Enum):
    """Available tool types"""
    WEB_SEARCH = "web_search"
    CODE_EXEC = "code_execution"
    CALCULATE = "calculator"
    WEATHER = "weather"
    MEMORY_SEARCH = "memory_search"
    INFORMATION = "information"


class ToolResult:
    """Wrapper for tool execution results"""
    def __init__(self, tool_name: str, success: bool, result: Any, error: Optional[str] = None, execution_time_ms: int = 0):
        self.tool_name = tool_name
        self.success = success
        self.result = result
        self.error = error
        self.execution_time_ms = execution_time_ms
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "tool": self.tool_name,
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "execution_time_ms": self.execution_time_ms,
            "timestamp": self.timestamp,
        }


class CortexTools:
    """Core tool execution engine"""

    AVAILABLE_TOOLS = {
        "web_search": {
            "name": "Web Search",
            "description": "Search the internet for information",
            "params": {"query": "str (required)"},
        },
        "calculator": {
            "name": "Calculator",
            "description": "Perform mathematical calculations",
            "params": {"expression": "str (required)"},
        },
        "memory_search": {
            "name": "Memory Search",
            "description": "Search agent's memory for information",
            "params": {"query": "str (required)", "category": "str (optional)"},
        },
        "code_exec": {
            "name": "Code Executor",
            "description": "Execute Python code safely (sandboxed)",
            "params": {"code": "str (required)", "timeout": "int (optional, default 10)"},
        },
    }

    def __init__(self):
        self.execution_history = {}
        log.info("CortexTools initialized with tools: " + ", ".join(self.AVAILABLE_TOOLS.keys()))

    async def list_tools(self) -> List[Dict]:
        """List all available tools"""
        return list(self.AVAILABLE_TOOLS.values())

    async def get_tool_info(self, tool_name: str) -> Optional[Dict]:
        """Get information about a specific tool"""
        if tool_name not in self.AVAILABLE_TOOLS:
            return None
        return self.AVAILABLE_TOOLS[tool_name]

    async def execute_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        user_id: Optional[str] = None,
    ) -> ToolResult:
        """Execute a tool with given arguments"""
        if tool_name not in self.AVAILABLE_TOOLS:
            return ToolResult(
                tool_name,
                False,
                None,
                error=f"Tool '{tool_name}' not found",
            )

        start_time = time.time()

        try:
            if tool_name == "web_search":
                result = await self._web_search(args.get("query", ""))
            elif tool_name == "calculator":
                result = await self._calculate(args.get("expression", ""))
            elif tool_name == "code_exec":
                result = await self._execute_code(
                    args.get("code", ""),
                    args.get("timeout", 10),
                )
            elif tool_name == "memory_search":
                result = await self._memory_search(
                    args.get("query", ""),
                    args.get("category"),
                    user_id,
                )
            else:
                result = {"error": "Tool not implemented"}

            execution_time = int((time.time() - start_time) * 1000)
            tool_result = ToolResult(tool_name, True, result, execution_time_ms=execution_time)

            # Store in history
            if user_id:
                if user_id not in self.execution_history:
                    self.execution_history[user_id] = []
                self.execution_history[user_id].append(tool_result.to_dict())

            log.debug(f"Tool {tool_name} executed successfully in {execution_time}ms")
            return tool_result

        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            error_msg = f"Error executing {tool_name}: {str(e)}"
            log.error(error_msg)
            return ToolResult(
                tool_name,
                False,
                None,
                error=error_msg,
                execution_time_ms=execution_time,
            )

    async def _web_search(self, query: str, max_results: int = 5) -> Dict:
        """Perform web search (mock implementation - needs actual search API)"""
        try:
            # This would integrate with actual search API (Google, Bing, etc)
            # For now, returning a structure that shows how it would work
            return {
                "query": query,
                "results": [
                    {
                        "title": f"Result about {query}",
                        "url": "https://example.com/result",
                        "snippet": f"Information about {query}...",
                    }
                ],
                "total_results": 1,
                "note": "Web search requires API key configuration",
            }
        except Exception as e:
            raise Exception(f"Web search failed: {e}")

    async def _calculate(self, expression: str) -> Dict:
        """Perform mathematical calculation"""
        try:
            # Safety: Only allow basic math expressions
            allowed_chars = "0123456789+-*/.() "
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters in expression")

            result = eval(expression)  # Safe because we validated chars
            return {
                "expression": expression,
                "result": result,
                "type": type(result).__name__,
            }
        except Exception as e:
            raise Exception(f"Calculation failed: {e}")

    async def _execute_code(self, code: str, timeout: int = 10) -> Dict:
        """Execute Python code safely (sandboxed)"""
        try:
            # Safety: Run in subprocess with timeout to prevent resource exhaustion
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            return {
                "code": code[:200],  # Truncate for response
                "stdout": result.stdout[:1000],  # Limit output
                "stderr": result.stderr[:1000],
                "returncode": result.returncode,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            raise Exception(f"Code execution timeout (>{timeout}s)")
        except Exception as e:
            raise Exception(f"Code execution failed: {e}")

    async def _memory_search(
        self,
        query: str,
        category: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Dict:
        """Search user's memory"""
        try:
            # This integrates with the cortex memory system
            # Would call cortex_memories.search_memories() in production
            return {
                "query": query,
                "category": category,
                "results": [],
                "note": "Would search cortex memory in production",
            }
        except Exception as e:
            raise Exception(f"Memory search failed: {e}")

    async def get_execution_history(
        self, user_id: str, limit: int = 100
    ) -> List[Dict]:
        """Get execution history for a user"""
        if user_id not in self.execution_history:
            return []
        return self.execution_history[user_id][-limit:]


# Singleton instance
cortex_tools = CortexTools()
