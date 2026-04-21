# Source: NEW - Cortex Discord Bot Module
# CORTEX MODIFICATION: Discord bot integration for Cortex agent

import os
import asyncio
from typing import Optional, Dict, List, Any
from datetime import datetime
import logging

import discord
from discord.ext import commands, tasks

logger = logging.getLogger(__name__)


class CortexDiscordBot(commands.Cog):
    """Discord bot integration for Cortex AI agent"""

    def __init__(self, bot: commands.Bot, cortex_api_url: str = "http://localhost:8000/api"):
        self.bot = bot
        self.api_url = cortex_api_url
        self.activity_log: List[Dict[str, Any]] = []
        self.max_log_size = 500
        self.command_prefix = "/"

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when bot connects to Discord"""
        logger.info(f"Cortex bot logged in as {self.bot.user}")
        await self.update_activity()
        self.heartbeat_loop.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handle incoming messages"""
        # Ignore bot's own messages
        if message.author == self.bot.user:
            return

        # Ignore messages without Cortex command prefix
        if not message.content.startswith(self.command_prefix):
            return

        # Log activity
        self._log_activity(
            type="message",
            guild=message.guild.name if message.guild else "DM",
            channel=message.channel.name if hasattr(message.channel, "name") else "DM",
            user=message.author.name,
            action="Message received",
            details=message.content[:100],
        )

        # Process command
        await self.process_cortex_command(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Handle reaction added"""
        if user == self.bot.user:
            return

        self._log_activity(
            type="reaction",
            guild=reaction.message.guild.name if reaction.message.guild else "DM",
            channel=reaction.message.channel.name if hasattr(reaction.message.channel, "name") else "DM",
            user=user.name,
            action="Reaction added",
            details=f"Emoji: {reaction.emoji}",
        )

    @tasks.loop(minutes=5)
    async def heartbeat_loop(self):
        """Periodic heartbeat for health checks"""
        try:
            await self.update_activity()
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")

    async def update_activity(self):
        """Update bot activity status"""
        try:
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="Cortex dreams | /help for commands"
                )
            )
        except Exception as e:
            logger.error(f"Failed to update activity: {e}")

    async def process_cortex_command(self, message: discord.Message):
        """Process Cortex slash command"""
        try:
            # Parse command from message
            parts = message.content.strip().split(maxsplit=1)
            if len(parts) < 1:
                return

            command = parts[0][1:]  # Remove slash prefix
            args = parts[1] if len(parts) > 1 else ""

            # Handle commands
            if command == "chat":
                await self.handle_chat(message, args)
            elif command == "memory":
                await self.handle_memory(message, args)
            elif command == "status":
                await self.handle_status(message)
            elif command == "dream":
                await self.handle_dream(message)
            elif command == "help":
                await self.handle_help(message)
            else:
                await message.reply(f"Unknown command: /{command}. Use `/help` for available commands.")

        except Exception as e:
            logger.error(f"Error processing command: {e}")
            await message.reply(f"Error processing command: {str(e)}")

    async def handle_chat(self, message: discord.Message, query: str):
        """Handle /chat command"""
        if not query:
            await message.reply("Usage: `/chat <message>`")
            return

        try:
            # Show typing indicator
            async with message.channel.typing():
                # Send to Cortex API
                import aiohttp

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.api_url}/chat/message",
                        json={"message": query, "context": {"source": "discord"}},
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            if data.get("status") == "ok":
                                response_text = data.get("data", {}).get("content", "No response")
                                # Split long responses
                                await self.send_long_message(message, response_text)
                            else:
                                await message.reply(f"Error: {data.get('error', 'Unknown error')}")
                        else:
                            await message.reply(f"API error: {resp.status}")
        except Exception as e:
            logger.error(f"Chat error: {e}")
            await message.reply(f"Failed to get response: {str(e)}")

    async def handle_memory(self, message: discord.Message, args: str):
        """Handle /memory command"""
        if not args:
            await message.reply("Usage: `/memory add|search|list [args]`")
            return

        try:
            parts = args.split(maxsplit=1)
            action = parts[0]
            data = parts[1] if len(parts) > 1 else ""

            import aiohttp

            async with aiohttp.ClientSession() as session:
                if action == "add":
                    if not data:
                        await message.reply("Usage: `/memory add <content>`")
                        return

                    async with session.post(
                        f"{self.api_url}/memory/add",
                        json={
                            "category": "discord",
                            "title": f"From {message.author.name}",
                            "content": data,
                            "importance": 5,
                        },
                    ) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            if result.get("status") == "ok":
                                await message.reply("✓ Memory added successfully")
                            else:
                                await message.reply(f"Error: {result.get('error')}")

                elif action == "search":
                    if not data:
                        await message.reply("Usage: `/memory search <query>`")
                        return

                    async with session.get(
                        f"{self.api_url}/memory/search",
                        params={"query": data, "limit": 5},
                    ) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            if result.get("status") == "ok":
                                memories = result.get("data", [])
                                if memories:
                                    response = "Found memories:\n"
                                    for mem in memories:
                                        response += f"- {mem.get('title')}: {mem.get('content')[:50]}...\n"
                                    await self.send_long_message(message, response)
                                else:
                                    await message.reply("No memories found")

                elif action == "list":
                    async with session.get(
                        f"{self.api_url}/memory/",
                        params={"limit": 10},
                    ) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            if result.get("status") == "ok":
                                memories = result.get("data", [])
                                if memories:
                                    response = "Recent memories:\n"
                                    for mem in memories[:5]:
                                        response += f"- [{mem.get('category')}] {mem.get('title')}\n"
                                    await self.send_long_message(message, response)
                                else:
                                    await message.reply("No memories stored")

        except Exception as e:
            logger.error(f"Memory command error: {e}")
            await message.reply(f"Error: {str(e)}")

    async def handle_status(self, message: discord.Message):
        """Handle /status command"""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/chat/context") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "ok":
                            ctx = data.get("data", {})
                            status_text = f"""
**Cortex Agent Status**
Agent: {'✓ Ready' if ctx.get('agent_ready') else '✗ Offline'}
Memory: {ctx.get('memory_entries', 0)} entries
Dreaming: {'Enabled' if ctx.get('dreaming_enabled') else 'Disabled'}
Discord: ✓ Connected
Available Tools: {', '.join(ctx.get('available_tools', []))}
"""
                            await message.reply(status_text)
        except Exception as e:
            logger.error(f"Status error: {e}")
            await message.reply(f"Failed to get status: {str(e)}")

    async def handle_dream(self, message: discord.Message):
        """Handle /dream command"""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_url}/dreaming/run") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "ok":
                            await message.reply("💭 Dream cycle started. Agent is consolidating memories...")
                            self._log_activity(
                                type="dream",
                                guild=message.guild.name if message.guild else "DM",
                                channel=message.channel.name if hasattr(message.channel, "name") else "DM",
                                user=message.author.name,
                                action="Dream cycle initiated",
                                details="Manual trigger",
                            )
                        else:
                            await message.reply(f"Error: {data.get('error')}")
        except Exception as e:
            logger.error(f"Dream error: {e}")
            await message.reply(f"Failed to start dream: {str(e)}")

    async def handle_help(self, message: discord.Message):
        """Handle /help command"""
        help_text = """
**Cortex Discord Bot Commands**

`/chat <message>` - Send a message to Cortex agent
`/memory add <content>` - Save content to memory
`/memory search <query>` - Search memory entries
`/memory list` - Show recent memories
`/status` - Show agent status
`/dream` - Trigger memory consolidation dream
`/help` - Show this help message

**Examples:**
`/chat What is the weather?`
`/memory add Important reminder: meeting at 3pm`
`/memory search past events`
"""
        await message.reply(help_text)

    async def send_long_message(self, message: discord.Message, content: str, max_length: int = 2000):
        """Send message, splitting if needed"""
        if len(content) <= max_length:
            await message.reply(content)
        else:
            # Split into chunks
            chunks = [content[i : i + max_length] for i in range(0, len(content), max_length)]
            for chunk in chunks:
                await message.reply(chunk)

    def _log_activity(
        self,
        type: str,
        guild: str,
        channel: str,
        user: str,
        action: str,
        details: str = "",
    ):
        """Log Discord activity"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": type,
            "guild": guild,
            "channel": channel,
            "user": user,
            "action": action,
            "details": details,
        }
        self.activity_log.append(entry)

        # Trim log if too large
        if len(self.activity_log) > self.max_log_size:
            self.activity_log = self.activity_log[-self.max_log_size :]

        logger.info(f"Discord Activity: {action} - {user} in {channel}")

    def get_activity_log(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get activity log"""
        return self.activity_log[-limit:]

    @commands.command()
    async def ping(self, ctx):
        """Simple ping command for testing"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


async def setup_discord_bot(token: str, cortex_api_url: str = "http://localhost:8000/api"):
    """Initialize and start Discord bot"""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    cog = CortexDiscordBot(bot, cortex_api_url)
    await bot.add_cog(cog)

    logger.info("Discord bot initialized")
    return bot, cog


def get_discord_status(bot: commands.Bot) -> Dict[str, Any]:
    """Get current Discord bot status"""
    if not bot or not bot.user:
        return {"connected": False, "status": "disconnected"}

    return {
        "connected": True,
        "user_id": str(bot.user.id),
        "username": bot.user.name,
        "guilds": len(bot.guilds),
        "uptime_seconds": (datetime.utcnow() - bot.launch_time).total_seconds()
        if hasattr(bot, "launch_time")
        else 0,
        "latency_ms": round(bot.latency * 1000),
    }
