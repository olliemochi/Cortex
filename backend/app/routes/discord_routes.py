# Source: NEW - Discord Integration Endpoints
# CORTEX MODIFICATION: REST API endpoints for Discord bot management

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/discord", tags=["discord"])

# Global Discord bot instance (will be set during app initialization)
discord_bot_instance = None
discord_cog_instance = None


class DiscordConfig(BaseModel):
    token: str
    api_url: Optional[str] = "http://localhost:8000/api"


@router.get("/status")
async def get_discord_status():
    """Get Discord bot status"""
    try:
        if not discord_bot_instance:
            return {
                "status": "ok",
                "data": {
                    "connected": False,
                    "status": "not_initialized",
                    "error": "Discord bot not initialized",
                },
            }

        from app.integrations.discord_bot import get_discord_status

        status = get_discord_status(discord_bot_instance)
        return {"status": "ok", "data": status}
    except Exception as e:
        logger.error(f"Error getting Discord status: {e}")
        return {
            "status": "error",
            "error": str(e),
            "data": {"connected": False},
        }


@router.post("/test-connection")
async def test_discord_connection():
    """Test Discord bot connection"""
    try:
        if not discord_bot_instance:
            raise Exception("Discord bot not initialized")

        # Test by checking if bot is ready
        is_ready = discord_bot_instance.is_ready()
        latency = discord_bot_instance.latency

        return {
            "status": "ok",
            "data": {
                "test_result": "success" if is_ready else "bot_not_ready",
                "connected": is_ready,
                "latency_ms": round(latency * 1000),
            },
        }
    except Exception as e:
        logger.error(f"Error testing Discord connection: {e}")
        return {
            "status": "error",
            "error": str(e),
            "data": {"test_result": "failed"},
        }


@router.post("/start")
async def start_discord_bot(config: DiscordConfig, background_tasks: BackgroundTasks):
    """Start Discord bot"""
    try:
        global discord_bot_instance, discord_cog_instance

        if discord_bot_instance and discord_bot_instance.is_ready():
            return {
                "status": "ok",
                "data": {"message": "Bot already running"},
            }

        from app.integrations.discord_bot import setup_discord_bot

        bot, cog = await setup_discord_bot(config.token, config.api_url)
        discord_bot_instance = bot
        discord_cog_instance = cog

        # Start bot in background
        background_tasks.add_task(bot.start, config.token)

        return {
            "status": "ok",
            "data": {"message": "Discord bot starting"},
        }
    except Exception as e:
        logger.error(f"Error starting Discord bot: {e}")
        return {
            "status": "error",
            "error": str(e),
        }


@router.post("/stop")
async def stop_discord_bot():
    """Stop Discord bot"""
    try:
        global discord_bot_instance

        if not discord_bot_instance:
            return {
                "status": "ok",
                "data": {"message": "Bot not running"},
            }

        await discord_bot_instance.close()
        discord_bot_instance = None

        return {
            "status": "ok",
            "data": {"message": "Discord bot stopped"},
        }
    except Exception as e:
        logger.error(f"Error stopping Discord bot: {e}")
        return {
            "status": "error",
            "error": str(e),
        }


@router.get("/activity")
async def get_discord_activity(limit: int = 20):
    """Get Discord bot activity log"""
    try:
        if not discord_cog_instance:
            return {
                "status": "ok",
                "data": [],
            }

        activity = discord_cog_instance.get_activity_log(limit)
        return {
            "status": "ok",
            "data": activity,
            "total": len(activity),
        }
    except Exception as e:
        logger.error(f"Error getting activity log: {e}")
        return {
            "status": "error",
            "error": str(e),
            "data": [],
        }


def set_discord_instances(bot, cog):
    """Set global Discord bot instances"""
    global discord_bot_instance, discord_cog_instance
    discord_bot_instance = bot
    discord_cog_instance = cog
