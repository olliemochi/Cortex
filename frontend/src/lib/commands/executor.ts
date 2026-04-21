// Source: NEW - Cortex Command Executor
// CORTEX MODIFICATION: Execute parsed slash commands and route to appropriate handlers

import { getCommand } from './registry';
import { parseCommand, validateCommand } from './parser';
import type { ParsedCommand } from './parser';
import * as cortexAPI from '../api/cortex';

export interface CommandResult {
	success: boolean;
	message: string;
	data?: any;
	error?: string;
}

/**
 * Execute a command based on user input
 */
export async function executeCommand(input: string): Promise<CommandResult> {
	// Parse the command
	const parsed = parseCommand(input);

	// Check if it's actually a command
	if (!parsed.isCommand) {
		return {
			success: false,
			message: 'Not a command',
			error: parsed.error || 'Message does not start with /'
		};
	}

	// Validate the command
	const validation = validateCommand(parsed);
	if (!validation.valid) {
		return {
			success: false,
			message: 'Invalid command',
			error: validation.error
		};
	}

	// Get the command definition
	const command = getCommand(parsed.command || '');
	if (!command) {
		return {
			success: false,
			message: 'Command not found',
			error: `Unknown command: ${parsed.command}`
		};
	}

	try {
		// Route to appropriate handler based on command
		switch (command.name) {
			case 'memory':
				return await handleMemoryCommand(parsed.args);
			case 'search':
				return await handleSearchCommand(parsed.args);
			case 'dream':
				return await handleDreamCommand(parsed.args);
			case 'tools':
				return await handleToolsCommand(parsed.args);
			case 'status':
				return await handleStatusCommand(parsed.args);
			case 'help':
				return await handleHelpCommand(parsed.args);
			case 'clear':
				return await handleClearCommand(parsed.args);
			case 'reset':
				return await handleResetCommand(parsed.args);
			default:
				// Use the handler from command definition if available
				if (command.handler) {
					const result = await command.handler(parsed.args);
					return {
						success: true,
						message: 'Command executed',
						data: result
					};
				}
				return {
					success: false,
					message: 'Command not implemented',
					error: `No handler for command: ${command.name}`
				};
		}
	} catch (error) {
		return {
			success: false,
			message: 'Command execution failed',
			error: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}

/**
 * Handle /memory command
 */
async function handleMemoryCommand(args: Record<string, any>): Promise<CommandResult> {
	const action = args.action || 'list';
	const query = args.query || '';

	try {
		switch (action) {
			case 'list': {
				const response = await cortexAPI.memoryClient.list();
				return {
					success: response.status === 'ok',
					message: `Retrieved ${response.data?.length || 0} memory entries`,
					data: response.data
				};
			}

			case 'search': {
				if (!query) {
					return {
						success: false,
						message: 'Search query required',
						error: 'Please provide a search query'
					};
				}
				const response = await cortexAPI.memoryClient.search(query);
				return {
					success: response.status === 'ok',
					message: `Found ${response.data?.length || 0} matching entries`,
					data: response.data
				};
			}

			case 'promote': {
				const entryId = parseInt(query);
				if (isNaN(entryId)) {
					return {
						success: false,
						message: 'Invalid entry ID',
						error: 'Entry ID must be a number'
					};
				}
				const response = await cortexAPI.memoryClient.promote(entryId);
				return {
					success: response.status === 'ok',
					message: `Promoted entry ${entryId} to long-term memory`,
					data: response.data
				};
			}

			case 'delete': {
				const entryId = parseInt(query);
				if (isNaN(entryId)) {
					return {
						success: false,
						message: 'Invalid entry ID',
						error: 'Entry ID must be a number'
					};
				}
				const response = await cortexAPI.memoryClient.delete(entryId);
				return {
					success: response.status === 'ok',
					message: `Deleted entry ${entryId}`,
					data: response.data
				};
			}

			default:
				return {
					success: false,
					message: 'Unknown action',
					error: `Memory action '${action}' not recognized`
				};
		}
	} catch (error) {
		return {
			success: false,
			message: 'Memory command failed',
			error: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}

/**
 * Handle /search command
 */
async function handleSearchCommand(args: Record<string, any>): Promise<CommandResult> {
	const query = args.query;

	if (!query) {
		return {
			success: false,
			message: 'Search query required',
			error: 'Please provide a search query'
		};
	}

	try {
		const response = await cortexAPI.memoryClient.search(query);
		return {
			success: response.status === 'ok',
			message: `Found ${response.data?.length || 0} results for "${query}"`,
			data: response.data
		};
	} catch (error) {
		return {
			success: false,
			message: 'Search failed',
			error: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}

/**
 * Handle /dream command
 */
async function handleDreamCommand(args: Record<string, any>): Promise<CommandResult> {
	const action = args.action || 'status';

	try {
		switch (action) {
			case 'status': {
				const response = await cortexAPI.dreamingClient.status();
				return {
					success: response.status === 'ok',
					message: 'Dreaming status retrieved',
					data: response.data
				};
			}

			case 'run': {
				const response = await cortexAPI.dreamingClient.run();
				return {
					success: response.status === 'ok',
					message: 'Dream cycle started',
					data: response.data
				};
			}

			case 'cancel': {
				const response = await cortexAPI.dreamingClient.cancel();
				return {
					success: response.status === 'ok',
					message: 'Dream cycle cancelled',
					data: response.data
				};
			}

			case 'history': {
				const response = await cortexAPI.dreamingClient.history();
				return {
					success: response.status === 'ok',
					message: `Retrieved ${response.data?.length || 0} dream records`,
					data: response.data
				};
			}

			default:
				return {
					success: false,
					message: 'Unknown action',
					error: `Dream action '${action}' not recognized`
				};
		}
	} catch (error) {
		return {
			success: false,
			message: 'Dream command failed',
			error: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}

/**
 * Handle /tools command
 */
async function handleToolsCommand(args: Record<string, any>): Promise<CommandResult> {
	const action = args.action || 'list';
	const toolName = args.tool_name || '';

	try {
		switch (action) {
			case 'list': {
				const response = await cortexAPI.toolsClient.list();
				return {
					success: response.status === 'ok',
					message: `Found ${response.data?.length || 0} available tools`,
					data: response.data
				};
			}

			case 'info': {
				if (!toolName) {
					return {
						success: false,
						message: 'Tool name required',
						error: 'Please specify a tool name'
					};
				}
				const response = await cortexAPI.toolsClient.info(toolName);
				return {
					success: response.status === 'ok',
					message: `Tool information retrieved`,
					data: response.data
				};
			}

			default:
				return {
					success: false,
					message: 'Unknown action',
					error: `Tools action '${action}' not recognized`
				};
		}
	} catch (error) {
		return {
			success: false,
			message: 'Tools command failed',
			error: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}

/**
 * Handle /status command
 */
async function handleStatusCommand(args: Record<string, any>): Promise<CommandResult> {
	try {
		const response = await cortexAPI.chatClient.context();
		return {
			success: response.status === 'ok',
			message: 'System status retrieved',
			data: response.data
		};
	} catch (error) {
		return {
			success: false,
			message: 'Status command failed',
			error: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}

/**
 * Handle /help command
 */
async function handleHelpCommand(args: Record<string, any>): Promise<CommandResult> {
	const commandName = args.command;

	try {
		if (commandName) {
			const command = getCommand(commandName);
			if (!command) {
				return {
					success: false,
					message: 'Command not found',
					error: `Unknown command: ${commandName}`
				};
			}
			return {
				success: true,
				message: `Help for /${command.name}`,
				data: command
			};
		} else {
			// List all commands
			const allCommands = await import('./registry').then((m) => m.getAllCommands());
			return {
				success: true,
				message: `Available commands (${allCommands.length} total)`,
				data: allCommands.map((c) => ({
					name: c.name,
					description: c.description,
					aliases: c.aliases,
					category: c.category
				}))
			};
		}
	} catch (error) {
		return {
			success: false,
			message: 'Help command failed',
			error: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}

/**
 * Handle /clear command
 */
async function handleClearCommand(args: Record<string, any>): Promise<CommandResult> {
	return {
		success: true,
		message: 'Chat history cleared',
		data: { action: 'clear_chat' }
	};
}

/**
 * Handle /reset command
 */
async function handleResetCommand(args: Record<string, any>): Promise<CommandResult> {
	return {
		success: true,
		message: 'Agent state reset',
		data: { action: 'reset_agent' }
	};
}
