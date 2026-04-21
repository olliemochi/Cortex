#!/usr/bin/env fish

# Fish Completion for Cortex CLI
# Installation:
#   cp cortex_completion.fish ~/.config/fish/completions/cortex.fish

# Main commands
complete -c cortex -f -n "__fish_use_subcommand_from_list" -a "chat" -d "Send messages to Cortex agent"
complete -c cortex -f -n "__fish_use_subcommand_from_list" -a "memory" -d "Manage long-term memory"
complete -c cortex -f -n "__fish_use_subcommand_from_list" -a "dream" -d "Manage dreaming cycles"
complete -c cortex -f -n "__fish_use_subcommand_from_list" -a "tools" -d "Manage tools and skills"
complete -c cortex -f -n "__fish_use_subcommand_from_list" -a "status" -d "Get system status"
complete -c cortex -f -n "__fish_use_subcommand_from_list" -a "version" -d "Show version"
complete -c cortex -f -n "__fish_use_subcommand_from_list" -a "info" -d "Show information"

# Chat subcommands
complete -c cortex -f -n "__fish_seen_subcommand_from chat" -a "send" -d "Send message to agent"

# Memory subcommands
complete -c cortex -f -n "__fish_seen_subcommand_from memory" -a "list" -d "List memory entries"
complete -c cortex -f -n "__fish_seen_subcommand_from memory" -a "add" -d "Add memory entry"
complete -c cortex -f -n "__fish_seen_subcommand_from memory" -a "search" -d "Search memories"
complete -c cortex -f -n "__fish_seen_subcommand_from memory" -a "promote" -d "Promote memory to long-term"
complete -c cortex -f -n "__fish_seen_subcommand_from memory" -a "delete" -d "Delete memory entry"

# Memory options
complete -c cortex -n "__fish_seen_subcommand_from memory" -l category -d "Memory category" -r
complete -c cortex -n "__fish_seen_subcommand_from memory" -l importance -d "Importance level 1-10" -r
complete -c cortex -n "__fish_seen_subcommand_from memory" -l limit -d "Number of entries" -r

# Dream subcommands
complete -c cortex -f -n "__fish_seen_subcommand_from dream" -a "status" -d "Get dreaming status"
complete -c cortex -f -n "__fish_seen_subcommand_from dream" -a "run" -d "Start dream cycle"
complete -c cortex -f -n "__fish_seen_subcommand_from dream" -a "cancel" -d "Cancel dream cycle"
complete -c cortex -f -n "__fish_seen_subcommand_from dream" -a "history" -d "Get dream history"

# Dream options
complete -c cortex -n "__fish_seen_subcommand_from dream" -l focus -d "Dream focus topic" -r
complete -c cortex -n "__fish_seen_subcommand_from dream" -l limit -d "Number of entries" -r

# Tools subcommands
complete -c cortex -f -n "__fish_seen_subcommand_from tools" -a "list" -d "List available tools"
complete -c cortex -f -n "__fish_seen_subcommand_from tools" -a "info" -d "Get tool information"
complete -c cortex -f -n "__fish_seen_subcommand_from tools" -a "execute" -d "Execute a tool"

# Tools options
complete -c cortex -n "__fish_seen_subcommand_from tools" -l limit -d "Number of results" -r
