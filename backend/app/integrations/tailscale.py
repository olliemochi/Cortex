# Source: NEW - Cortex Tailscale Integration
# CORTEX MODIFICATION: Tailscale network integration for secure remote access

import os
import json
import logging
import subprocess
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class TailscaleDevice:
    """Tailscale device information"""

    name: str
    ip: str
    device_id: str
    is_online: bool
    last_seen: Optional[str] = None


@dataclass
class TailscaleStatus:
    """Tailscale network status"""

    self_name: str
    self_ip: str
    is_connected: bool
    tailnet: str
    peers: List[TailscaleDevice]
    auth_key: Optional[str] = None


class TailscaleClient:
    """Tailscale network client"""

    def __init__(self, api_key: Optional[str] = None, tailnet: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAILSCALE_API_KEY")
        self.tailnet = tailnet or os.getenv("TAILSCALE_TAILNET", "example.com")
        self.base_url = "https://api.tailscale.com/api/v2"
        self.control_url = os.getenv("TAILSCALE_CONTROL_URL", "https://controlplane.tailscale.com")
        self._status = None

    async def get_status(self) -> Optional[TailscaleStatus]:
        """Get Tailscale status"""
        try:
            result = await self._run_command(["tailscale", "status", "--json"])
            if result:
                data = json.loads(result)
                self._status = self._parse_status(data)
                return self._status
        except Exception as e:
            logger.error(f"Error getting Tailscale status: {e}")
        return None

    async def connect(self) -> bool:
        """Connect to Tailscale network"""
        try:
            await self._run_command(["tailscale", "up"])
            logger.info("Connected to Tailscale")
            return True
        except Exception as e:
            logger.error(f"Error connecting to Tailscale: {e}")
            return False

    async def disconnect(self) -> bool:
        """Disconnect from Tailscale network"""
        try:
            await self._run_command(["tailscale", "down"])
            logger.info("Disconnected from Tailscale")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from Tailscale: {e}")
            return False

    async def get_peers(self) -> List[Dict[str, Any]]:
        """Get list of Tailscale peers"""
        try:
            status = await self.get_status()
            if status:
                return [
                    {
                        "name": peer.name,
                        "ip": peer.ip,
                        "device_id": peer.device_id,
                        "is_online": peer.is_online,
                        "last_seen": peer.last_seen,
                    }
                    for peer in status.peers
                ]
        except Exception as e:
            logger.error(f"Error getting peers: {e}")
        return []

    async def enable_device_sharing(self, device_name: str) -> bool:
        """Enable device sharing"""
        try:
            await self._run_command(
                ["tailscale", "share", "enable", device_name]
            )
            logger.info(f"Device sharing enabled: {device_name}")
            return True
        except Exception as e:
            logger.error(f"Error enabling device sharing: {e}")
            return False

    async def disable_device_sharing(self, device_name: str) -> bool:
        """Disable device sharing"""
        try:
            await self._run_command(
                ["tailscale", "share", "disable", device_name]
            )
            logger.info(f"Device sharing disabled: {device_name}")
            return True
        except Exception as e:
            logger.error(f"Error disabling device sharing: {e}")
            return False

    async def pair_device(
        self, device_ip: str, timeout: int = 300
    ) -> Optional[str]:
        """Pair with another device on Tailscale network"""
        try:
            # Test connectivity to device
            result = await self._run_command(
                ["tailscale", "ping", device_ip, "-c", "1"],
                timeout=10
            )

            if result:
                logger.info(f"Successfully paired with device: {device_ip}")
                return device_ip
        except Exception as e:
            logger.error(f"Error pairing device: {e}")
        return None

    async def list_devices(self) -> List[Dict[str, Any]]:
        """List all devices in Tailnet"""
        devices = []
        try:
            if self.api_key and self.tailnet:
                # Use API for more detailed information
                import aiohttp

                async with aiohttp.ClientSession() as session:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    url = f"{self.base_url}/tailnet/{self.tailnet}/devices"

                    async with session.get(url, headers=headers) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            devices = data.get("devices", [])
            else:
                # Fallback to CLI
                peers = await self.get_peers()
                devices = peers

        except Exception as e:
            logger.error(f"Error listing devices: {e}")

        return devices

    async def get_device_details(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get details for specific device"""
        try:
            if self.api_key and self.tailnet:
                import aiohttp

                async with aiohttp.ClientSession() as session:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    url = f"{self.base_url}/tailnet/{self.tailnet}/devices/{device_id}"

                    async with session.get(url, headers=headers) as resp:
                        if resp.status == 200:
                            return await resp.json()
        except Exception as e:
            logger.error(f"Error getting device details: {e}")

        return None

    async def authorize_device(self, device_id: str) -> bool:
        """Authorize device in Tailnet"""
        try:
            if self.api_key and self.tailnet:
                import aiohttp

                async with aiohttp.ClientSession() as session:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    url = f"{self.base_url}/tailnet/{self.tailnet}/devices/{device_id}/authorize"

                    async with session.post(url, headers=headers) as resp:
                        if resp.status == 200:
                            logger.info(f"Device authorized: {device_id}")
                            return True
        except Exception as e:
            logger.error(f"Error authorizing device: {e}")

        return False

    async def revoke_device(self, device_id: str) -> bool:
        """Revoke device access"""
        try:
            if self.api_key and self.tailnet:
                import aiohttp

                async with aiohttp.ClientSession() as session:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    url = f"{self.base_url}/tailnet/{self.tailnet}/devices/{device_id}"

                    async with session.delete(url, headers=headers) as resp:
                        if resp.status == 200:
                            logger.info(f"Device revoked: {device_id}")
                            return True
        except Exception as e:
            logger.error(f"Error revoking device: {e}")

        return False

    def generate_auth_key(self, reusable: bool = True, expiry_hours: int = 24) -> Optional[str]:
        """Generate authentication key for device pairing"""
        try:
            if self.api_key and self.tailnet:
                import aiohttp
                import asyncio

                async def _gen_key():
                    async with aiohttp.ClientSession() as session:
                        headers = {"Authorization": f"Bearer {self.api_key}"}
                        url = f"{self.base_url}/tailnet/{self.tailnet}/keys"
                        payload = {
                            "reusable": reusable,
                            "expiry": expiry_hours * 3600,
                            "preauthorized": True,
                        }

                        async with session.post(
                            url, headers=headers, json=payload
                        ) as resp:
                            if resp.status == 200:
                                data = await resp.json()
                                return data.get("key")
                    return None

                return asyncio.run(_gen_key())
        except Exception as e:
            logger.error(f"Error generating auth key: {e}")

        return None

    async def _run_command(
        self, command: List[str], timeout: int = 30
    ) -> Optional[str]:
        """Run shell command"""
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )
                if process.returncode == 0:
                    return stdout.decode().strip()
                else:
                    error = stderr.decode().strip()
                    logger.error(f"Command error: {error}")
            except asyncio.TimeoutError:
                process.kill()
                logger.error(f"Command timeout: {' '.join(command)}")

        except Exception as e:
            logger.error(f"Error running command: {e}")

        return None

    def _parse_status(self, data: Dict[str, Any]) -> Optional[TailscaleStatus]:
        """Parse Tailscale status JSON"""
        try:
            peers = []
            for peer_data in data.get("Peer", {}).values():
                peer = TailscaleDevice(
                    name=peer_data.get("DNSName", "unknown"),
                    ip=peer_data.get("TailscaleIPs", [""])[0],
                    device_id=peer_data.get("ID", ""),
                    is_online=peer_data.get("Online", False),
                    last_seen=peer_data.get("LastSeen"),
                )
                peers.append(peer)

            self_data = data.get("Self", {})
            return TailscaleStatus(
                self_name=self_data.get("DNSName", "unknown"),
                self_ip=self_data.get("TailscaleIPs", [""])[0],
                is_connected=data.get("TUN", False),
                tailnet=self.tailnet,
                peers=peers,
            )
        except Exception as e:
            logger.error(f"Error parsing status: {e}")
            return None


# API endpoints handler
async def get_tailscale_status() -> Dict[str, Any]:
    """Get Tailscale status"""
    client = TailscaleClient()
    status = await client.get_status()

    if status:
        return {
            "connected": status.is_connected,
            "self_name": status.self_name,
            "self_ip": status.self_ip,
            "tailnet": status.tailnet,
            "peers_count": len(status.peers),
            "peers": [
                {
                    "name": p.name,
                    "ip": p.ip,
                    "is_online": p.is_online,
                }
                for p in status.peers
            ],
        }

    return {"connected": False, "error": "Failed to get status"}


async def connect_tailscale() -> Dict[str, Any]:
    """Connect to Tailscale"""
    client = TailscaleClient()
    success = await client.connect()

    if success:
        status = await client.get_status()
        if status:
            return {"success": True, "ip": status.self_ip}

    return {"success": False, "error": "Failed to connect"}


async def disconnect_tailscale() -> Dict[str, Any]:
    """Disconnect from Tailscale"""
    client = TailscaleClient()
    success = await client.disconnect()

    return {"success": success}


async def pair_tailscale_device(device_ip: str) -> Dict[str, Any]:
    """Pair with Tailscale device"""
    client = TailscaleClient()
    result = await client.pair_device(device_ip)

    if result:
        return {"success": True, "device_ip": result}

    return {"success": False, "error": "Failed to pair device"}
