# Cortex CLI Structure

## Organization

The CLI is organized into modular command groups for better maintainability:

### Commands Module (`commands/`)

- **chat.py** - Send messages to Cortex agent
- **memory.py** - Manage long-term memory (list, add, search, promote, delete)
- **dreaming.py** - Manage dreaming cycles (status, run, cancel, history)
- **tools.py** - Execute tools and skills (list, info, execute)
- **system.py** - System commands (status, version, info)

### Completions Module (`completions/`)

Shell completion scripts for improved CLI experience:

- **cortex_completion.bash** - Bash completion
- **cortex_completion.zsh** - Zsh completion
- **cortex_completion.fish** - Fish shell completion

## Installation

### System Installation (Auto-install Completions)

When you install Cortex using the system installer, shell completions are automatically installed:

```bash
sudo bash install-app.sh
```

This installs completions to:
- **Bash**: `/etc/bash_completion.d/cortex`
- **Zsh**: `/usr/share/zsh/site-functions/_cortex`
- **Fish**: `/usr/share/fish/vendor_completions.d/cortex.fish`

After installation, restart your shell or open a new terminal window for completions to be active.

### Manual Installation

If you prefer to manually install completions:

#### Bash Completion

```bash
sudo cp completions/cortex_completion.bash /etc/bash_completion.d/cortex
```

Or add to `~/.bashrc`:
```bash
source /path/to/cortex/cli/completions/cortex_completion.bash
```

#### Zsh Completion

```bash
mkdir -p ~/.zsh/completions
cp completions/cortex_completion.zsh ~/.zsh/completions/_cortex
```

Or system-wide:
```bash
sudo cp completions/cortex_completion.zsh /usr/share/zsh/site-functions/_cortex
```

#### Fish Completion

```bash
mkdir -p ~/.config/fish/completions
cp completions/cortex_completion.fish ~/.config/fish/completions/cortex.fish
```

Or system-wide:
```bash
sudo cp completions/cortex_completion.fish /usr/share/fish/vendor_completions.d/cortex.fish
```

## Usage Examples

```bash
# Chat with agent
cortex chat send "Hello, what is your name?"

# Manage memory
cortex memory list --limit 20
cortex memory add --category "learning" --importance 8 "Python Tips" "Use list comprehensions"
cortex memory search "database" --limit 10
cortex memory promote 5

# Dreaming cycles
cortex dream status
cortex dream run --focus "memory consolidation"
cortex dream history --limit 5

# Tools
cortex tools list
cortex tools info web_search
cortex tools execute web_search query="AI news"

# System
cortex status
cortex version
cortex info
```

## Integration with cortex_cli.py

The command modules wrap the main `CortexCLI` class from `cortex_cli.py`, providing a clean Click-based interface while maintaining backward compatibility with the core CLI logic.

### Extending the CLI

To add new commands:

1. Create a new module in `commands/` (e.g., `learning.py`)
2. Define command groups and commands using Click decorators
3. Import and export in `commands/__init__.py`
4. Add corresponding completion rules in the appropriate completion script

### Adding New Options

For any new command options, update the relevant completion script to include them for better shell integration.
