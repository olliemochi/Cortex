"""System information commands"""

import click
from rich.console import Console
from rich.panel import Panel
from cortex_cli import CortexCLI

console = Console()


@click.command()
@click.pass_context
def status(ctx):
    """Get system status"""
    cli = CortexCLI()
    cli.status()


@click.command()
def version():
    """Show version"""
    console.print("[bold]Cortex[/bold] v1.0.0")


@click.command()
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
