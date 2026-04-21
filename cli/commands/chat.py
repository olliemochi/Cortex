"""Chat command group"""

import click
from cortex_cli import CortexCLI


@click.group()
def chat():
    """Chat with Cortex agent"""
    pass


@chat.command("send")
@click.argument("message", nargs=-1, required=True)
@click.pass_context
def chat_send(ctx, message):
    """Send message to agent"""
    cli = CortexCLI()
    cli.chat(" ".join(message))
