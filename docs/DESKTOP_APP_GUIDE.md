# Cortex Desktop Application Guide

**Organization**: AetherAssembly  
**License**: MIT  

---

## Overview

Cortex can now be installed as a native Linux desktop application. This guide shows how to install and use it.

---

## Installation

### Option 1: Quick Desktop Install (Recommended)

```bash
cd /path/to/cortex
sudo make install-app
```

This will:
- Copy application files to `/opt/cortex`
- Install launcher to `/usr/local/bin/cortex-launcher`
- Install desktop entry to application menu
- Create application icon
- Update desktop database

### Option 2: Manual Installation

```bash
cd /path/to/cortex
sudo bash install-app.sh
```

### Requirements

- Linux system with desktop environment (GNOME, KDE, XFCE, etc.)
- `sudo` access for system installation
- ~5GB free space in `/opt`

---

## Usage

### Launch from Application Menu

1. Open your application launcher (Activities, Dash, Whisker Menu, etc.)
2. Search for "Cortex"
3. Click to launch

### Launch from Command Line

```bash
cortex-launcher
```

Or via Make:

```bash
make launch
```

### What Happens on Launch

1. **Environment Setup**
   - Creates virtual environment at `~/.local/share/cortex/venv`
   - Installs/updates dependencies automatically
   - Configures local database settings

2. **Backend Startup**
   - Starts FastAPI server on port 8000
   - Waits for server to be ready
   - Logs to `~/.local/share/cortex/logs/backend.log`

3. **Frontend Startup**
   - Starts Vite dev server on port 5173
   - Logs to `~/.local/share/cortex/logs/frontend.log`

4. **Browser Opening**
   - Automatically opens default browser
   - Navigates to `http://localhost:5173`
   - Shows welcome screen

---

## Access Points

Once running:

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:5173 | Web interface |
| API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API Alternative | http://localhost:8000/redoc | ReDoc |

---

## File Locations

After installation:

```
/opt/cortex/                          # Application files
  ├── backend/                        # FastAPI backend
  ├── frontend/                       # SvelteKit frontend
  └── Cortex-Wiki/                    # Documentation

~/.local/share/cortex/                # User data
  ├── venv/                           # Python environment
  ├── data/                           # Application data
  └── logs/                           # Log files
    ├── backend.log
    └── frontend.log

/usr/local/share/applications/
  └── cortex.desktop                  # Desktop entry

/usr/local/share/icons/hicolor/256x256/apps/
  └── cortex.svg                      # Application icon

/usr/local/bin/
  ├── cortex-launcher                 # Launch script
  └── cortex-uninstall                # Uninstall script
```

---

## Uninstallation

### Via Make

```bash
sudo make uninstall-app
```

### Manual Uninstall

```bash
sudo cortex-uninstall
```

This removes:
- `/opt/cortex` - Application files
- `/usr/local/bin/cortex-launcher` - Launcher script
- `/usr/local/bin/cortex-uninstall` - Uninstall script
- `/usr/local/share/applications/cortex.desktop` - Desktop entry
- `/usr/local/share/icons/hicolor/256x256/apps/cortex.svg` - Icon

Note: User data in `~/.local/share/cortex/` is preserved for reinstall.

---

## Troubleshooting

### App Won't Start

**Check logs:**
```bash
tail -f ~/.local/share/cortex/logs/backend.log
tail -f ~/.local/share/cortex/logs/frontend.log
```

**Common issues:**

- **Port in use**: Another service is using ports 8000 or 5173
  ```bash
  lsof -i :8000
  lsof -i :5173
  ```

- **Missing dependencies**: Reinstall:
  ```bash
  sudo rm -rf ~/.local/share/cortex/venv
  cortex-launcher  # Will recreate venv
  ```

- **Permission denied**: App needs write access to home directory
  ```bash
  sudo chown -R $USER ~/.local/share/cortex
  ```

### Browser Doesn't Open

The application will still run. You can manually open:
```
http://localhost:5173
```

### Database Connection Error

Check PostgreSQL is running:
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

---

## Development Mode

To run from source directory instead of system installation:

```bash
cd /path/to/cortex
bash run-dev.sh
```

Or for development with live reloading:

```bash
make dev
```

---

## Configuration

### Environment Variables

Edit `~/.local/share/cortex/data/.env` to customize:

```env
DATABASE_URL=postgresql://cortex:cortex@localhost:5432/cortex_dev
API_PORT=8000
DEBUG=False
LOG_LEVEL=INFO
```

Changes require restarting the application.

### Logs

View application logs:
```bash
# Backend logs
cat ~/.local/share/cortex/logs/backend.log

# Frontend logs
cat ~/.local/share/cortex/logs/frontend.log

# Real-time monitoring
tail -f ~/.local/share/cortex/logs/*.log
```

---

## System Integration

### Add to Startup

To auto-launch Cortex on system startup:

1. **GNOME**: `gnome-tweaks` → Startup Applications → Add
2. **KDE**: System Settings → Startup and Shutdown → Autostart
3. **XFCE**: Applications → Autostart → Add

Command: `/usr/local/bin/cortex-launcher`

### Desktop Shortcut

The `.desktop` file is automatically installed. You can also create a desktop shortcut:

```bash
cp /usr/local/share/applications/cortex.desktop ~/Desktop/
chmod +x ~/Desktop/cortex.desktop
```

---

## Shell Completions

### Automatic Installation

When you install the desktop application, shell completions are **automatically installed** for:

- **Bash** → `/etc/bash_completion.d/cortex`
- **Zsh** → `/usr/share/zsh/site-functions/_cortex`
- **Fish** → `/usr/share/fish/vendor_completions.d/cortex.fish`

### Using CLI Completions

Open a new terminal and try:

```bash
# View all commands
cortex [TAB][TAB]

# View memory commands
cortex memory [TAB][TAB]

# View options
cortex memory add --[TAB][TAB]
```

### Available Commands

```bash
cortex chat send          # Send message to agent
cortex memory list        # List memory entries
cortex memory add         # Add new memory entry
cortex memory search      # Search memories
cortex dream status       # Get dream cycle status
cortex dream run          # Start a dream cycle
cortex tools list         # List available tools
cortex tools execute      # Execute a tool
cortex status             # Show system status
cortex version            # Show version
cortex info               # Show information
```

### Manual Restart Completions (if needed)

If completions aren't working after installation:

```bash
# Bash
source /etc/bash_completion.d/cortex

# Zsh - Restart shell
exec zsh

# Fish - Restart shell
exec fish
```

### Removing Completions

When you uninstall the application, completions are automatically removed:

```bash
sudo cortex-uninstall
```

---

## Support & Feedback

- **Issues**: https://github.com/aetherassembly/Cortex/issues
- **Email**: support@aetherassembly.org
- **Contact**: contact@aetherassembly.org
- **Website**: https://cortex.aetherassembly.org

---

## Advanced Usage

### Run in Background

```bash
nohup cortex-launcher > /tmp/cortex.log 2>&1 &
```

### Systemd Service (Optional)

Create `/etc/systemd/user/cortex.service`:

```ini
[Unit]
Description=Cortex AI Agent Platform
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/cortex-launcher
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

Enable and start:
```bash
systemctl --user enable cortex
systemctl --user start cortex
```

---

**Cortex** - Advanced AI Agent Platform by **AetherAssembly**  
License: MIT | Support: support@aetherassembly.org
