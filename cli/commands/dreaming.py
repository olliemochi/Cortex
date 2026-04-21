"""Dreaming cycle command group"""

import click
from cortex_cli import CortexCLI


@click.group()
def dream():
    """Manage dreaming cycles"""
    pass


@dream.command("status")
@click.pass_context
def dream_status(ctx):
    """Get dreaming status"""
    cli = CortexCLI()
    cli.dreaming_status()


@dream.command("run")
@click.option("--focus", default=None, help="Dream focus topic")
@click.pass_context
def dream_run(ctx, focus):
    """Start dream cycle"""
    cli = CortexCLI()
    cli.dreaming_run(focus)


@dream.command("cancel")
@click.pass_context
def dream_cancel(ctx):
    """Cancel dream cycle"""
    cli = CortexCLI()
    cli.dreaming_cancel()


@dream.command("history")
@click.option("--limit", default=10, help="Number of entries")
@click.pass_context
def dream_history(ctx, limit):
    """Get dream history"""
    cli = CortexCLI()
    cli.dreaming_history(limit)
