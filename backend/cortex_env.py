# Source: NEW - Cortex-specific environment configuration
# CORTEX MODIFICATION: New file for Cortex-specific environment variables

import os
import logging
from typing import Optional
from pathlib import Path

log = logging.getLogger(__name__)

# =====================================================
# CORTEX - CORE CONFIGURATION
# =====================================================

# Whether to bind to Tailscale interface only (not 0.0.0.0)
TAILSCALE_ONLY = os.getenv('TAILSCALE_ONLY', 'false').lower() == 'true'

# Tailscale hostname for DNS naming
TAILSCALE_HOSTNAME = os.getenv('TAILSCALE_HOSTNAME', 'cortex')

# =====================================================
# CORTEX - MODEL CONFIGURATION
# =====================================================

# Default model for Cortex agent
CORTEX_DEFAULT_MODEL = os.getenv('CORTEX_DEFAULT_MODEL', 'cortex:latest')

# Custom model path (for fine-tuned models)
CORTEX_CUSTOM_MODEL_PATH = os.getenv('CORTEX_CUSTOM_MODEL_PATH', '')

# =====================================================
# CORTEX - MEMORY CONFIGURATION
# =====================================================

# Path to MEMORY.md file
MEMORY_PATH = os.getenv('MEMORY_PATH', './memory/MEMORY.md')

# Path to DREAMS.md file
DREAMS_PATH = os.getenv('DREAMS_PATH', './memory/DREAMS.md')

# Enable dreaming system
DREAMING_ENABLED = os.getenv('DREAMING_ENABLED', 'false').lower() == 'true'

# Cron schedule for automatic dreaming (e.g., "0 3 * * *" = 3 AM daily)
DREAMING_SCHEDULE = os.getenv('DREAMING_SCHEDULE', '0 3 * * *')

# =====================================================
# CORTEX - DISCORD BOT CONFIGURATION
# =====================================================

# Enable Discord bot integration
DISCORD_BOT_ENABLED = os.getenv('DISCORD_BOT_ENABLED', 'false').lower() == 'true'

# Discord bot token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')

# Comma-separated list of Discord channel IDs where bot can respond
DISCORD_ALLOWED_CHANNELS = [
    ch.strip() for ch in os.getenv('DISCORD_ALLOWED_CHANNELS', '').split(',') if ch.strip()
]

# Comma-separated list of Discord user IDs allowed to interact with bot
DISCORD_ALLOWED_USERS = [
    u.strip() for u in os.getenv('DISCORD_ALLOWED_USERS', '').split(',') if u.strip()
]

# =====================================================
# CORTEX - LOGGING CONFIGURATION
# =====================================================

LOG_FILE = os.getenv('LOG_FILE', './logs/cortex.log')
CORTEX_LOG_LEVEL = os.getenv('CORTEX_LOG_LEVEL', 'INFO')

# Ensure logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

log.info(f'Cortex Configuration Loaded')
log.debug(f'  TAILSCALE_ONLY: {TAILSCALE_ONLY}')
log.debug(f'  CORTEX_DEFAULT_MODEL: {CORTEX_DEFAULT_MODEL}')
log.debug(f'  MEMORY_PATH: {MEMORY_PATH}')
log.debug(f'  DREAMS_PATH: {DREAMS_PATH}')
log.debug(f'  DREAMING_ENABLED: {DREAMING_ENABLED}')
log.debug(f'  DISCORD_BOT_ENABLED: {DISCORD_BOT_ENABLED}')
