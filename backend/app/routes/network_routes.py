# Source: NEW - Tailscale Integration Endpoints
# CORTEX MODIFICATION: REST API endpoints for Tailscale network management

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/network", tags=["network"])


class DevicePairingRequest(BaseModel):
    device_ip: str


class AuthKeyRequest(BaseModel):
    reusable: bool = True
    expiry_hours: int = 24


@router.get("/tailscale/status")
async def get_tailscale_status():
    """Get Tailscale network status"""
    try:
        from app.integrations.tailscale import get_tailscale_status

        status = await get_tailscale_status()
        return {"status": "ok", "data": status}
    except Exception as e:
        logger.error(f"Error getting Tailscale status: {e}")
        return {
            "status": "error",
            "error": str(e),
            "data": {"connected": False},
        }


@router.post("/tailscale/connect")
async def connect_tailscale():
    """Connect to Tailscale network"""
    try:
        from app.integrations.tailscale import connect_tailscale

        result = await connect_tailscale()
        if result.get("success"):
            return {"status": "ok", "data": result}
        else:
            return {
                "status": "error",
                "error": result.get("error", "Connection failed"),
            }
    except Exception as e:
        logger.error(f"Error connecting to Tailscale: {e}")
        return {"status": "error", "error": str(e)}


@router.post("/tailscale/disconnect")
async def disconnect_tailscale():
    """Disconnect from Tailscale network"""
    try:
        from app.integrations.tailscale import disconnect_tailscale

        result = await disconnect_tailscale()
        if result.get("success"):
            return {"status": "ok", "data": result}
        else:
            return {"status": "error", "error": "Disconnection failed"}
    except Exception as e:
        logger.error(f"Error disconnecting from Tailscale: {e}")
        return {"status": "error", "error": str(e)}


@router.get("/tailscale/peers")
async def list_tailscale_peers():
    """List Tailscale network peers"""
    try:
        from app.integrations.tailscale import TailscaleClient

        client = TailscaleClient()
        peers = await client.list_devices()
        return {"status": "ok", "data": peers}
    except Exception as e:
        logger.error(f"Error listing peers: {e}")
        return {"status": "error", "error": str(e), "data": []}


@router.post("/tailscale/pair")
async def pair_device(request: DevicePairingRequest):
    """Pair with Tailscale device"""
    try:
        from app.integrations.tailscale import pair_tailscale_device

        result = await pair_tailscale_device(request.device_ip)
        if result.get("success"):
            return {"status": "ok", "data": result}
        else:
            return {"status": "error", "error": result.get("error")}
    except Exception as e:
        logger.error(f"Error pairing device: {e}")
        return {"status": "error", "error": str(e)}


@router.get("/tailscale/auth-key")
async def generate_tailscale_auth_key(
    reusable: bool = True, expiry_hours: int = 24
):
    """Generate Tailscale authentication key"""
    try:
        from app.integrations.tailscale import TailscaleClient

        client = TailscaleClient()
        auth_key = client.generate_auth_key(reusable, expiry_hours)

        if auth_key:
            return {
                "status": "ok",
                "data": {
                    "auth_key": auth_key,
                    "reusable": reusable,
                    "expiry_hours": expiry_hours,
                },
            }
        else:
            return {"status": "error", "error": "Failed to generate auth key"}
    except Exception as e:
        logger.error(f"Error generating auth key: {e}")
        return {"status": "error", "error": str(e)}
