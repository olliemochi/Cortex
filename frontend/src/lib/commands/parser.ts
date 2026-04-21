// Source: NEW - Cortex Command Parser
// CORTEX MODIFICATION: Parse and validate slash commands from user input

import { getCommand } from './registry';

export interface ParsedCommand {
	isCommand: boolean;
	command?: string;
	args: Record<string, any>;
	rawArgs: string[];
	remainingText: string;
	error?: string;
}

/**
 * Parse a user message to detect slash commands
 *
 * Examples:
 * - "/memory search cortex" -> { isCommand: true, command: "memory", args: { action: "search", query: "cortex" } }
 * - "hello /world" -> { isCommand: false, remainingText: "hello /world" }
 * - "/unknown" -> { isCommand: false, error: "Unknown command: unknown" }
 */
export function parseCommand(message: string): ParsedCommand {
	const trimmed = message.trim();

	// Check if message starts with slash
	if (!trimmed.startsWith('/')) {
		return {
			isCommand: false,
			args: {},
			rawArgs: [],
			remainingText: message
		};
	}

	// Extract command and rest
	const parts = trimmed.slice(1).split(/\s+/);
	if (parts.length === 0 || !parts[0]) {
		return {
			isCommand: false,
			args: {},
			rawArgs: [],
			remainingText: message,
			error: 'Invalid command format'
		};
	}

	const commandName = parts[0].toLowerCase();
	const restArgs = parts.slice(1);

	// Look up command
	const command = getCommand(commandName);
	if (!command) {
		return {
			isCommand: false,
			args: {},
			rawArgs: restArgs,
			remainingText: message,
			error: `Unknown command: ${commandName}`
		};
	}

	// Parse arguments based on command definition
	const args = parseArguments(command, restArgs);

	return {
		isCommand: true,
		command: command.name,
		args,
		rawArgs: restArgs,
		remainingText: ''
	};
}

/**
 * Parse command arguments according to command definition
 */
function parseArguments(command: any, rawArgs: string[]): Record<string, any> {
	const args: Record<string, any> = {};

	if (!command.args || command.args.length === 0) {
		return args;
	}

	// Simple positional parsing
	command.args.forEach((argDef: any, index: number) => {
		if (argDef.type === 'enum') {
			// Enum argument - must match one of the values
			if (index < rawArgs.length && argDef.enum?.includes(rawArgs[index])) {
				args[argDef.name] = rawArgs[index];
			}
		} else if (argDef.type === 'number') {
			// Number argument
			if (index < rawArgs.length) {
				const num = parseFloat(rawArgs[index]);
				if (!isNaN(num)) {
					args[argDef.name] = num;
				}
			}
		} else if (argDef.type === 'boolean') {
			// Boolean argument
			if (index < rawArgs.length) {
				args[argDef.name] = ['true', 'yes', '1'].includes(rawArgs[index].toLowerCase());
			}
		} else {
			// String argument - consume rest of args
			if (index < rawArgs.length) {
				args[argDef.name] = rawArgs.slice(index).join(' ');
			}
		}
	});

	return args;
}

/**
 * Validate a parsed command has all required arguments
 */
export function validateCommand(parsed: ParsedCommand): { valid: boolean; error?: string } {
	if (!parsed.isCommand) {
		return { valid: false, error: 'Not a command' };
	}

	if (parsed.error) {
		return { valid: false, error: parsed.error };
	}

	const command = getCommand(parsed.command || '');
	if (!command) {
		return { valid: false, error: 'Command not found' };
	}

	// Check required arguments
	for (const argDef of command.args) {
		if (argDef.required && !(argDef.name in parsed.args)) {
			return {
				valid: false,
				error: `Missing required argument: ${argDef.name}`
			};
		}
	}

	return { valid: true };
}

/**
 * Extract autocomplete suggestions from partial input
 */
export function getAutocompleteSuggestions(
	input: string
): { commands: any[]; position: number; partialText: string } {
	// Check if we're in a command context
	if (!input.startsWith('/')) {
		return { commands: [], position: -1, partialText: '' };
	}

	// Find the last word (potential command name)
	const parts = input.slice(1).split(/\s+/);
	const currentPart = parts[parts.length - 1];

	// If this is the first part, suggest commands
	if (parts.length === 1) {
		const suggestions = getCommandSuggestions(currentPart);
		return {
			commands: suggestions,
			position: 0,
			partialText: currentPart
		};
	}

	// If we have a command, suggest its arguments
	const commandName = parts[0].toLowerCase();
	const command = getCommand(commandName);
	if (!command || command.args.length === 0) {
		return { commands: [], position: -1, partialText: '' };
	}

	// Suggest enum values for enum arguments
	const argIndex = parts.length - 2; // -1 for command, -1 for 0-indexing
	if (argIndex < command.args.length) {
		const argDef = command.args[argIndex];
		if (argDef.type === 'enum' && argDef.enum) {
			const suggestions = argDef.enum.filter((e) =>
				e.toLowerCase().startsWith(currentPart.toLowerCase())
			);
			return {
				commands: suggestions.map((s) => ({ name: s, description: argDef.description })),
				position: argIndex,
				partialText: currentPart
			};
		}
	}

	return { commands: [], position: -1, partialText: '' };
}

/**
 * Format a command help text
 */
export function getCommandHelp(commandName: string): string {
	const command = getCommand(commandName);
	if (!command) {
		return `Command not found: ${commandName}`;
	}

	let help = `**/${command.name}** - ${command.description}\n\n`;

	if (command.aliases.length > 0) {
		help += `**Aliases**: ${command.aliases.map((a) => `/${a}`).join(', ')}\n\n`;
	}

	if (command.args.length > 0) {
		help += `**Arguments**:\n`;
		command.args.forEach((arg) => {
			const required = arg.required ? '(required)' : '(optional)';
			help += `  - **${arg.name}** ${required}: ${arg.description}`;
			if (arg.type === 'enum' && arg.enum) {
				help += ` [${arg.enum.join(', ')}]`;
			}
			help += '\n';
		});
	}

	return help;
}

// Re-export for convenience
export { getCommandSuggestions } from './registry';