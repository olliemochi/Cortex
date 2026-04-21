#!/bin/bash

# Bash Completion for Cortex CLI
# Installation:
#   sudo cp cortex_completion.bash /etc/bash_completion.d/cortex
#   OR
#   source cortex_completion.bash

_cortex_completion() {
    local cur prev words cword
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    local commands="chat memory dream tools status version info"
    
    # Chat subcommands
    local chat_commands="send"
    
    # Memory subcommands
    local memory_commands="list add search promote delete"
    
    # Dream subcommands
    local dream_commands="status run cancel history"
    
    # Tools subcommands
    local tools_commands="list info execute"
    
    # Options for various commands
    local memory_options="--category --importance --limit"
    local dream_options="--focus --limit"
    local tools_options="--limit"
    
    # Completion logic
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
    elif [[ ${COMP_CWORD} -eq 2 ]]; then
        case "${COMP_WORDS[1]}" in
            chat)
                COMPREPLY=($(compgen -W "${chat_commands}" -- ${cur}))
                ;;
            memory)
                COMPREPLY=($(compgen -W "${memory_commands}" -- ${cur}))
                ;;
            dream)
                COMPREPLY=($(compgen -W "${dream_commands}" -- ${cur}))
                ;;
            tools)
                COMPREPLY=($(compgen -W "${tools_commands}" -- ${cur}))
                ;;
        esac
    elif [[ ${COMP_CWORD} -ge 2 ]]; then
        case "${COMP_WORDS[1]}" in
            memory)
                COMPREPLY=($(compgen -W "${memory_options}" -- ${cur}))
                ;;
            dream)
                COMPREPLY=($(compgen -W "${dream_options}" -- ${cur}))
                ;;
            tools)
                COMPREPLY=($(compgen -W "${tools_options}" -- ${cur}))
                ;;
        esac
    fi
    
    return 0
}

complete -o bashdefault -o default -o nospace -F _cortex_completion cortex
