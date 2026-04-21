#compdef cortex

# Zsh Completion for Cortex CLI
# Installation:
#   cp cortex_completion.zsh /usr/share/zsh/site-functions/_cortex
#   OR
#   mkdir -p ~/.zsh/completions
#   cp cortex_completion.zsh ~/.zsh/completions/_cortex

_cortex() {
    local -a main_commands
    main_commands=(
        'chat:Send messages to Cortex agent'
        'memory:Manage long-term memory'
        'dream:Manage dreaming cycles'
        'tools:Manage tools and skills'
        'status:Get system status'
        'version:Show version'
        'info:Show information'
    )
    
    local -a chat_subcommands
    chat_subcommands=(
        'send:Send message to agent'
    )
    
    local -a memory_subcommands
    memory_subcommands=(
        'list:List memory entries'
        'add:Add memory entry'
        'search:Search memories'
        'promote:Promote memory to long-term'
        'delete:Delete memory entry'
    )
    
    local -a dream_subcommands
    dream_subcommands=(
        'status:Get dreaming status'
        'run:Start dream cycle'
        'cancel:Cancel dream cycle'
        'history:Get dream history'
    )
    
    local -a tools_subcommands
    tools_subcommands=(
        'list:List available tools'
        'info:Get tool information'
        'execute:Execute a tool'
    )
    
    local -a memory_options
    memory_options=(
        '--category:Memory category'
        '--importance:Importance level 1-10'
        '--limit:Number of entries'
    )
    
    local -a dream_options
    dream_options=(
        '--focus:Dream focus topic'
        '--limit:Number of entries'
    )
    
    local -a tools_options
    tools_options=(
        '--limit:Number of results'
    )

    _arguments -s -n \
        ':command:->command' \
        '*::options:->options'

    case $state in
        command)
            _describe 'cortex command' main_commands
            ;;
        options)
            case $words[2] in
                chat)
                    _describe 'chat subcommand' chat_subcommands
                    ;;
                memory)
                    case $words[3] in
                        *)
                            _describe 'memory subcommand' memory_subcommands
                            _describe 'memory options' memory_options
                            ;;
                    esac
                    ;;
                dream)
                    case $words[3] in
                        *)
                            _describe 'dream subcommand' dream_subcommands
                            _describe 'dream options' dream_options
                            ;;
                    esac
                    ;;
                tools)
                    case $words[3] in
                        *)
                            _describe 'tools subcommand' tools_subcommands
                            _describe 'tools options' tools_options
                            ;;
                    esac
                    ;;
            esac
            ;;
    esac
}

_cortex
