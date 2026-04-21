"""Memory management command group"""

import click
from cortex_cli import CortexCLI


@click.group()
def memory():
    """Manage long-term memory"""
    pass


@memory.command("list")
@click.option("--limit", default=10, help="Number of entries")
@click.pass_context
def memory_list(ctx, limit):
    """List memory entries"""
    cli = CortexCLI()
    cli.memory_list(limit)


@memory.command("add")
@click.option("--category", default="general", help="Memory category")
@click.option("--importance", default=5, help="Importance (1-10)")
@click.argument("title")
@click.argument("content", nargs=-1, required=True)
@click.pass_context
def memory_add(ctx, category, importance, title, content):
    """Add memory entry"""
    cli = CortexCLI()
    cli.memory_add(category, title, " ".join(content), importance)


@memory.command("search")
@click.option("--limit", default=10, help="Number of results")
@click.argument("query", nargs=-1, required=True)
@click.pass_context
def memory_search(ctx, limit, query):
    """Search memories"""
    cli = CortexCLI()
    cli.memory_search(" ".join(query), limit)


@memory.command("promote")
@click.argument("memory_id", type=int)
@click.pass_context
def memory_promote(ctx, memory_id):
    """Promote memory to long-term storage"""
    cli = CortexCLI()
    cli.memory_promote(memory_id)


@memory.command("delete")
@click.argument("memory_id", type=int)
@click.pass_context
def memory_delete(ctx, memory_id):
    """Delete memory entry"""
    cli = CortexCLI()
    cli.memory_delete(memory_id)
