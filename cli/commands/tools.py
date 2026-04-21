"""Tool execution command group"""

import click
from cortex_cli import CortexCLI


@click.group()
def tools():
    """Manage tools and skills"""
    pass


@tools.command("list")
@click.pass_context
def tools_list(ctx):
    """List available tools"""
    cli = CortexCLI()
    cli.tools_list()


@tools.command("info")
@click.argument("tool_name")
@click.pass_context
def tools_info(ctx, tool_name):
    """Get tool information"""
    cli = CortexCLI()
    cli.tools_info(tool_name)


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
    cli = CortexCLI()
    cli.tools_execute(tool_name, param_dict)
