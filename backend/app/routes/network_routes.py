# Source: NEW - Tailscale Integration Endpoints
# CORTEX MODIFICATION: REST API endpoints for Tailscale network management
"""REST API endpoints for Tailscale network management."""

import logging

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/network", tags=["network"])


class DevicePairingRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Request model for device pairing."""

    device_ip: str


class AuthKeyRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Request model for auth key generation."""

    reusable: bool = True
    expiry_hours: int = 24


@router.get("/tailscale/status")
async def get_tailscale_status():
    """Get Tailscale network status"""
    try:
        from app.integrations.tailscale import (  # pylint: disable=import-outside-toplevel,import-error
            get_tailscale_status as _get_tailscale_status,
        )

        status = await _get_tailscale_status()
        return {"status": "ok", "data": status}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error getting Tailscale status: %s", e)
        return {
            "status": "error",
            "error": str(e),
            "data": {"connected": False},
        }


@router.post("/tailscale/connect")
async def connect_tailscale():
    """Connect to Tailscale network"""
    try:
        from app.integrations.tailscale import (  # pylint: disable=import-outside-toplevel,import-error
            connect_tailscale as _connect_tailscale,
        )

        result = await _connect_tailscale()
        if result.get("success"):
            return {"status": "ok", "data": result}
        return {
            "status": "error",
            "error": result.get("error", "Connection failed"),
        }
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error connecting to Tailscale: %s", e)
        return {"status": "error", "error": str(e)}


@router.post("/tailscale/disconnect")
async def disconnect_tailscale():
    """Disconnect from Tailscale network"""
    try:
        from app.integrations.tailscale import (  # pylint: disable=import-outside-toplevel,import-error
            disconnect_tailscale as _disconnect_tailscale,
        )

        result = await _disconnect_tailscale()
        if result.get("success"):
            return {"status": "ok", "data": result}
        return {"status": "error", "error": "Disconnection failed"}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error disconnecting from Tailscale: %s", e)
        return {"status": "error", "error": str(e)}


@router.get("/tailscale/peers")
async def list_tailscale_peers():
    """List Tailscale network peers"""
    try:
        from app.integrations.tailscale import (  # pylint: disable=import-outside-toplevel,import-error
            TailscaleClient,
        )

        client = TailscaleClient()
        peers = await client.list_devices()
        return {"status": "ok", "data": peers}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error listing peers: %s", e)
        return {"status": "error", "error": str(e), "data": []}


@router.post("/tailscale/pair")
async def pair_device(request: DevicePairingRequest):
    """Pair with Tailscale device"""
    try:
        from app.integrations.tailscale import (  # pylint: disable=import-outside-toplevel,import-error
            pair_tailscale_device,
        )

        result = await pair_tailscale_device(request.device_ip)
        if result.get("success"):
            return {"status": "ok", "data": result}
        return {"status": "error", "error": result.get("error")}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error pairing device: %s", e)
        return {"status": "error", "error": str(e)}


@router.get("/tailscale/auth-key")
async def generate_tailscale_auth_key(
    reusable: bool = True, expiry_hours: int = 24
):
    """Generate Tailscale authentication key"""
    try:
        from app.integrations.tailscale import (  # pylint: disable=import-outside-toplevel,import-error
            TailscaleClient,
        )

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
        return {"status": "error", "error": "Failed to generate auth key"}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error generating auth key: %s", e)
        return {"status": "error", "error": str(e)}
