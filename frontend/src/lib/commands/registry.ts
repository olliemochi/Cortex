// Source: NEW - Cortex Command Registry
// CORTEX MODIFICATION: Definition of all available slash commands

export interface CommandArg {
	name: string;
	description: string;
	type: 'string' | 'number' | 'boolean' | 'enum';
	required: boolean;
	enum?: string[];
}

export interface Command {
	name: string;
	description: string;
	aliases: string[];
	category: 'memory' | 'dreaming' | 'tools' | 'status' | 'help' | 'system';
	args: CommandArg[];
	action?: (args: string[]) => Promise<string>;
	handler?: (args: Record<string, any>) => Promise<any>;
}

/**
 * Global command registry
 * Maps command name to command definition
 */
const commands: Map<string, Command> = new Map();

/**
 * Register a command
 */
export function registerCommand(command: Command) {
	commands.set(command.name, command);
	// Also register aliases
	command.aliases.forEach((alias) => {
		commands.set(alias, command);
	});
}

/**
 * Get all registered commands
 */
export function getAllCommands(): Command[] {
	const seen = new Set<string>();
	const result: Command[] = [];
	commands.forEach((cmd, name) => {
		if (seen.has(cmd.name)) return;
		seen.add(cmd.name);
		result.push(cmd);
	});
	return result;
}

/**
 * Get command by name or alias
 */
export function getCommand(nameOrAlias: string): Command | undefined {
	return commands.get(nameOrAlias.toLowerCase());
}

/**
 * Get commands by category
 */
export function getCommandsByCategory(category: Command['category']): Command[] {
	const seen = new Set<string>();
	const result: Command[] = [];
	commands.forEach((cmd) => {
		if (cmd.category === category && !seen.has(cmd.name)) {
			seen.add(cmd.name);
			result.push(cmd);
		}
	});
	return result;
}

/**
 * Get autocomplete suggestions for partial command name
 */
export function getCommandSuggestions(partial: string): Command[] {
	const partialLower = partial.toLowerCase();
	const seen = new Set<string>();
	const result: Command[] = [];

	commands.forEach((cmd) => {
		if (seen.has(cmd.name)) return;
		if (cmd.name.startsWith(partialLower) || cmd.aliases.some((a) => a.startsWith(partialLower))) {
			seen.add(cmd.name);
			result.push(cmd);
		}
	});

	return result.sort((a, b) => a.name.localeCompare(b.name));
}

// ============================================================
// Built-in Commands
// ============================================================

/**
 * Register all built-in Cortex commands
 */
export function registerBuiltInCommands() {
	// /memory command
	registerCommand({
		name: 'memory',
		description: 'Manage your long-term memory',
		aliases: ['mem', 'm'],
		category: 'memory',
		args: [
			{
				name: 'action',
				description: 'Action to perform (list, add, search, promote, delete)',
				type: 'enum',
				required: false,
				enum: ['list', 'add', 'search', 'promote', 'delete']
			},
			{
				name: 'query',
				description: 'Query or additional arguments',
				type: 'string',
				required: false
			}
		],
		handler: async (args) => ({
			status: 'ok',
			action: args.action || 'list',
			message: 'Memory command executed'
		})
	});

	// /search command
	registerCommand({
		name: 'search',
		description: 'Search across all memory entries',
		aliases: ['find', 's'],
		category: 'memory',
		args: [
			{
				name: 'query',
				description: 'Search query',
				type: 'string',
				required: true
			}
		],
		handler: async (args) => ({
			status: 'ok',
			query: args.query,
			results: [],
			message: 'Search completed'
		})
	});

	// /dream command
	registerCommand({
		name: 'dream',
		description: 'Control the dreaming system',
		aliases: ['d'],
		category: 'dreaming',
		args: [
			{
				name: 'action',
				description: 'Action to perform (status, run, cancel, history)',
				type: 'enum',
				required: false,
				enum: ['status', 'run', 'cancel', 'history']
			}
		],
		handler: async (args) => ({
			status: 'ok',
			action: args.action || 'status',
			message: 'Dream command executed'
		})
	});

	// /tools command
	registerCommand({
		name: 'tools',
		description: 'List and execute available tools/skills',
		aliases: ['tool', 't'],
		category: 'tools',
		args: [
			{
				name: 'action',
				description: 'Action to perform (list, info, execute)',
				type: 'enum',
				required: false,
				enum: ['list', 'info', 'execute']
			},
			{
				name: 'tool_name',
				description: 'Name of the tool',
				type: 'string',
				required: false
			}
		],
		handler: async (args) => ({
			status: 'ok',
			action: args.action || 'list',
			message: 'Tools command executed'
		})
	});

	// /status command
	registerCommand({
		name: 'status',
		description: 'Get system status',
		aliases: ['st'],
		category: 'status',
		args: [],
		handler: async (args) => ({
			status: 'ok',
			agent: 'ready',
			memory: { entries: 0 },
			dreaming: { enabled: false },
			discord: { connected: false }
		})
	});

	// /help command
	registerCommand({
		name: 'help',
		description: 'Show help for commands',
		aliases: ['h', '?'],
		category: 'help',
		args: [
			{
				name: 'command',
				description: 'Specific command to get help for',
				type: 'string',
				required: false
			}
		],
		handler: async (args) => {
			const cmd = args.command ? getCommand(args.command) : undefined;
			const cmds = cmd ? [cmd] : getAllCommands();
			return {
				status: 'ok',
				commands: cmds
					.filter(Boolean)
					.map((c) => ({
						name: c?.name,
						description: c?.description,
						aliases: c?.aliases
					}))
			};
		}
	});

	// /clear command
	registerCommand({
		name: 'clear',
		description: 'Clear chat history',
		aliases: ['clr'],
		category: 'system',
		args: [],
		handler: async () => ({
			status: 'ok',
			message: 'Chat cleared'
		})
	});

	// /reset command
	registerCommand({
		name: 'reset',
		description: 'Reset agent state',
		aliases: ['rs'],
		category: 'system',
		args: [],
		handler: async () => ({
			status: 'ok',
			message: 'Agent reset'
		})
	});
}

// Initialize on module load
registerBuiltInCommands();

export const commands: Command[] = [
  {
    name: "help",
    description: "Show available commands",
    action: async () => "Available commands: /help, /memory, /dreaming, /tools, /status, /search, /run"
  },
  // More commands to be added
];
