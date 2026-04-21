#!/usr/bin/env python3
# Source: NEW - Cortex CLI Tool
# CORTEX MODIFICATION: Command-line interface for Cortex agent

import click
import json
import sys
from typing import Optional
from datetime import datetime
import requests
from tabulate import tabulate
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
import time

console = Console()


class CortexCLI:
    """Cortex CLI client"""

    def __init__(self, api_url: str = "http://localhost:8000/api"):
        self.api_url = api_url
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs):
        """Make API request"""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            console.print(
                f"[red]Error: Cannot connect to Cortex API at {self.api_url}[/red]"
            )
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            console.print(f"[red]API Error: {e}[/red]")
            sys.exit(1)

    def chat(self, message: str):
        """Send message to agent"""
        console.print("[yellow]Sending message...[/yellow]")
        result = self._request(
            "POST", "chat/message", json={"message": message, "stream": False}
        )

        if result.get("status") == "ok":
            data = result.get("data", {})
            console.print(
                Panel(
                    data.get("content", "No response"),
                    title="[bold]Cortex Response[/bold]",
                    border_style="green",
                )
            )
            if data.get("tokens"):
                tokens = data.get("tokens", {})
                console.print(
                    f"[dim]Tokens used - Input: {tokens.get('input')}, Output: {tokens.get('output')}[/dim]"
                )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def memory_list(self, limit: int = 10):
        """List memory entries"""
        result = self._request("GET", "memory/", params={"limit": limit})

        if result.get("status") == "ok":
            data = result.get("data", [])
            if not data:
                console.print("[yellow]No memories found[/yellow]")
                return

            table_data = []
            for mem in data:
                table_data.append(
                    [
                        mem.get("id"),
                        mem.get("category"),
                        mem.get("title"),
                        mem.get("importance"),
                        mem.get("status"),
                    ]
                )

            console.print(
                tabulate(
                    table_data,
                    headers=["ID", "Category", "Title", "Importance", "Status"],
                    tablefmt="grid",
                )
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def memory_add(self, category: str, title: str, content: str, importance: int = 5):
        """Add memory entry"""
        result = self._request(
            "POST",
            "memory/add",
            json={
                "category": category,
                "title": title,
                "content": content,
                "importance": importance,
            },
        )

        if result.get("status") == "ok":
            data = result.get("data", {})
            console.print(f"[green]✓ Memory added (ID: {data.get('id')})[/green]")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def memory_search(self, query: str, limit: int = 10):
        """Search memories"""
        result = self._request(
            "GET", "memory/search", params={"query": query, "limit": limit}
        )

        if result.get("status") == "ok":
            data = result.get("data", [])
            if not data:
                console.print("[yellow]No memories found[/yellow]")
                return

            for mem in data:
                console.print(
                    Panel(
                        mem.get("content"),
                        title=f"[bold]{mem.get('title')}[/bold]",
                        subtitle=f"Category: {mem.get('category')} | Importance: {mem.get('importance')}",
                    )
                )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def memory_promote(self, memory_id: int):
        """Promote memory to long-term storage"""
        result = self._request("POST", f"memory/promote/{memory_id}")

        if result.get("status") == "ok":
            console.print("[green]✓ Memory promoted to long-term storage[/green]")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def memory_delete(self, memory_id: int):
        """Delete memory entry"""
        result = self._request("DELETE", f"memory/{memory_id}")

        if result.get("status") == "ok":
            console.print("[green]✓ Memory deleted[/green]")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def dreaming_status(self):
        """Get dreaming status"""
        result = self._request("GET", "dreaming/status")

        if result.get("status") == "ok":
            data = result.get("data", {})
            console.print(
                Panel(
                    f"""Is Dreaming: {'Yes' if data.get('is_dreaming') else 'No'}
Last Dream: {data.get('last_dream', 'Never')}
Dream Frequency: {data.get('dream_frequency')}
Next Dream: {data.get('next_dream', 'Unknown')}
Auto Dreaming: {'Enabled' if data.get('auto_dreaming') else 'Disabled'}""",
                    title="[bold]Dreaming Status[/bold]",
                    border_style="cyan",
                )
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def dreaming_run(self, focus: Optional[str] = None):
        """Start dream cycle"""
        console.print("[yellow]Starting dream cycle...[/yellow]")
        payload = {}
        if focus:
            payload["focus"] = focus

        result = self._request("POST", "dreaming/run", json=payload)

        if result.get("status") == "ok":
            data = result.get("data", {})
            console.print(
                f"[green]✓ Dream started (ID: {data.get('dream_id')})[/green]"
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def dreaming_cancel(self):
        """Cancel dream cycle"""
        result = self._request("POST", "dreaming/cancel")

        if result.get("status") == "ok":
            console.print("[green]✓ Dream cancelled[/green]")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def dreaming_history(self, limit: int = 10):
        """Get dream history"""
        result = self._request("GET", "dreaming/history", params={"limit": limit})

        if result.get("status") == "ok":
            data = result.get("data", [])
            if not data:
                console.print("[yellow]No dream history[/yellow]")
                return

            table_data = []
            for dream in data:
                table_data.append(
                    [
                        dream.get("timestamp"),
                        dream.get("duration_seconds"),
                        dream.get("new_connections", 0),
                        dream.get("memories_processed", 0),
                    ]
                )

            console.print(
                tabulate(
                    table_data,
                    headers=["Timestamp", "Duration (s)", "Connections", "Memories"],
                    tablefmt="grid",
                )
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def tools_list(self):
        """List available tools"""
        result = self._request("GET", "tools/")

        if result.get("status") == "ok":
            data = result.get("data", [])
            if not data:
                console.print("[yellow]No tools available[/yellow]")
                return

            table_data = []
            for tool in data:
                table_data.append(
                    [
                        tool.get("name"),
                        tool.get("description"),
                        tool.get("status"),
                        tool.get("category", "unknown"),
                    ]
                )

            console.print(
                tabulate(
                    table_data,
                    headers=["Name", "Description", "Status", "Category"],
                    tablefmt="grid",
                )
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def tools_info(self, tool_name: str):
        """Get tool information"""
        result = self._request("GET", f"tools/{tool_name}")

        if result.get("status") == "ok":
            data = result.get("data", {})
            console.print(
                Panel(
                    json.dumps(data, indent=2),
                    title=f"[bold]{tool_name}[/bold]",
                    border_style="blue",
                )
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def tools_execute(self, tool_name: str, params: dict):
        """Execute tool"""
        console.print(f"[yellow]Executing {tool_name}...[/yellow]")
        result = self._request("POST", f"tools/{tool_name}/execute", json=params)

        if result.get("status") == "ok":
            data = result.get("data", {})
            console.print(
                Panel(
                    json.dumps(data.get("result"), indent=2),
                    title=f"[bold]{tool_name} Result[/bold]",
                    border_style="green",
                )
            )
            console.print(
                f"[dim]Execution time: {data.get('execution_time_ms')}ms[/dim]"
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")

    def status(self):
        """Get system status"""
        result = self._request("GET", "chat/context")

        if result.get("status") == "ok":
            data = result.get("data", {})
            console.print(
                Panel(
                    f"""Agent: {'✓ Ready' if data.get('agent_ready') else '✗ Offline'}
Memory Entries: {data.get('memory_entries', 0)}
Last Dream: {data.get('last_dream', 'Never')}
Dreaming Enabled: {'Yes' if data.get('dreaming_enabled') else 'No'}
Discord Status: {data.get('discord_status', 'unknown')}
Available Tools: {', '.join(data.get('available_tools', []))}""",
                    title="[bold]System Status[/bold]",
                    border_style="green",
                )
            )
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")


# Click CLI groups
@click.group()
@click.option(
    "--api-url",
    default="http://localhost:8000/api",
    envvar="CORTEX_API_URL",
    help="Cortex API URL",
)
@click.pass_context
def cortex(ctx, api_url):
    """Cortex CLI - Command-line interface for Cortex AI agent"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = CortexCLI(api_url)


@cortex.group()
def chat():
    """Chat with Cortex agent"""
    pass


@chat.command("send")
@click.argument("message", nargs=-1, required=True)
@click.pass_context
def chat_send(ctx, message):
    """Send message to agent"""
    ctx.obj["cli"].chat(" ".join(message))


@cortex.group()
def memory():
    """Manage long-term memory"""
    pass


@memory.command("list")
@click.option("--limit", default=10, help="Number of entries")
@click.pass_context
def memory_list(ctx, limit):
    """List memory entries"""
    ctx.obj["cli"].memory_list(limit)


@memory.command("add")
@click.option("--category", default="general", help="Memory category")
@click.option("--importance", default=5, help="Importance (1-10)")
@click.argument("title")
@click.argument("content", nargs=-1, required=True)
@click.pass_context
def memory_add(ctx, category, importance, title, content):
    """Add memory entry"""
    ctx.obj["cli"].memory_add(category, title, " ".join(content), importance)


@memory.command("search")
@click.option("--limit", default=10, help="Number of results")
@click.argument("query", nargs=-1, required=True)
@click.pass_context
def memory_search(ctx, limit, query):
    """Search memories"""
    ctx.obj["cli"].memory_search(" ".join(query), limit)


@memory.command("promote")
@click.argument("memory_id", type=int)
@click.pass_context
def memory_promote(ctx, memory_id):
    """Promote memory to long-term storage"""
    ctx.obj["cli"].memory_promote(memory_id)


@memory.command("delete")
@click.argument("memory_id", type=int)
@click.pass_context
def memory_delete(ctx, memory_id):
    """Delete memory entry"""
    ctx.obj["cli"].memory_delete(memory_id)


@cortex.group()
def dream():
    """Manage dreaming cycles"""
    pass


@dream.command("status")
@click.pass_context
def dream_status(ctx):
    """Get dreaming status"""
    ctx.obj["cli"].dreaming_status()


@dream.command("run")
@click.option("--focus", default=None, help="Dream focus topic")
@click.pass_context
def dream_run(ctx, focus):
    """Start dream cycle"""
    ctx.obj["cli"].dreaming_run(focus)


@dream.command("cancel")
@click.pass_context
def dream_cancel(ctx):
    """Cancel dream cycle"""
    ctx.obj["cli"].dreaming_cancel()


@dream.command("history")
@click.option("--limit", default=10, help="Number of entries")
@click.pass_context
def dream_history(ctx, limit):
    """Get dream history"""
    ctx.obj["cli"].dreaming_history(limit)


@cortex.group()
def tools():
    """Manage tools and skills"""
    pass


@tools.command("list")
@click.pass_context
def tools_list(ctx):
    """List available tools"""
    ctx.obj["cli"].tools_list()


@tools.command("info")
@click.argument("tool_name")
@click.pass_context
def tools_info(ctx, tool_name):
    """Get tool information"""
    ctx.obj["cli"].tools_info(tool_name)


@tools.command("execute")
@click.argument("tool_name")
@click.argument("params", nargs=-1)
@click.pass_context
def tools_execute(ctx, tool_name, params):
    """Execute a tool"""
    # Parse params as key=value pairs
    param_dict = {}
    for param in params:
        if "=" in param:
            key, value = param.split("=", 1)
            param_dict[key] = value
    ctx.obj["cli"].tools_execute(tool_name, param_dict)


@cortex.command()
@click.pass_context
def status(ctx):
    """Get system status"""
    ctx.obj["cli"].status()


@cortex.command()
def version():
    """Show version"""
    console.print("[bold]Cortex[/bold] v1.0.0")


@cortex.command()
def info():
    """Show information"""
    console.print(
        Panel(
            """Cortex is an advanced AI agent with:
  • Long-term memory management
  • Dreaming cycles for memory consolidation
  • Tool/skill execution framework
  • Discord integration
  • Command-line interface

Use [bold]cortex --help[/bold] for available commands.""",
            title="[bold]Cortex[/bold]",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    cortex(obj={})
