// Source: NEW - Cortex API Client
// CORTEX MODIFICATION: Frontend client for Cortex backend API

import { writable } from 'svelte/store';

// API base URL - will use current host by default
const API_BASE = '/api/cortex';

interface CortexResponse<T> {
	status: 'ok' | 'error';
	data?: T;
	error?: string;
	timestamp: string;
}

/**
 * Cortex Memory API Client
 */
export const memoryClient = {
	/**
	 * Get all memory entries
	 */
	async list(): Promise<CortexResponse<any[]>> {
		const res = await fetch(`${API_BASE}/memory/`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Add a new memory entry
	 */
	async add(entry: {
		category: string;
		title: string;
		content: string;
		importance: number;
	}): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/memory/add`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(entry)
		});
		return res.json();
	},

	/**
	 * Search memory entries
	 */
	async search(query: string): Promise<CortexResponse<any[]>> {
		const res = await fetch(`${API_BASE}/memory/search?query=${encodeURIComponent(query)}`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Promote a memory entry to long-term storage
	 */
	async promote(entryId: number): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/memory/promote/${entryId}`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Delete a memory entry
	 */
	async delete(entryId: number): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/memory/${entryId}`, {
			method: 'DELETE',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	}
};

/**
 * Cortex Dreaming API Client
 */
export const dreamingClient = {
	/**
	 * Get current dreaming status
	 */
	async status(): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/dreaming/status`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Start a dream cycle manually
	 */
	async run(): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/dreaming/run`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Cancel current dream cycle
	 */
	async cancel(): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/dreaming/cancel`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Get dream history
	 */
	async history(limit: number = 10): Promise<CortexResponse<any[]>> {
		const res = await fetch(`${API_BASE}/dreaming/history?limit=${limit}`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	}
};

/**
 * Cortex Tools/Skills API Client
 */
export const toolsClient = {
	/**
	 * List available tools/skills
	 */
	async list(): Promise<CortexResponse<any[]>> {
		const res = await fetch(`${API_BASE}/tools/`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Get tool information
	 */
	async info(toolName: string): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/tools/${toolName}`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Execute a tool with arguments
	 */
	async execute(toolName: string, args: Record<string, any>): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/tools/${toolName}/execute`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(args)
		});
		return res.json();
	},

	/**
	 * Get tool execution status
	 */
	async status(toolName: string): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/tools/${toolName}/status`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	}
};

/**
 * Cortex Chat API Client
 */
export const chatClient = {
	/**
	 * Send message to Cortex agent
	 */
	async message(message: string, context?: Record<string, any>): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/chat/message`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ message, context, stream: false })
		});
		return res.json();
	},

	/**
	 * Stream message response from Cortex agent
	 * Returns an async iterable of response chunks
	 */
	async *streamMessage(
		message: string,
		context?: Record<string, any>
	): AsyncGenerator<any, void, unknown> {
		const res = await fetch(`${API_BASE}/chat/stream`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ message, context, stream: true })
		});

		if (!res.ok) throw new Error(`Stream error: ${res.statusText}`);

		const reader = res.body?.getReader();
		if (!reader) throw new Error('No response body');

		const decoder = new TextDecoder();
		let buffer = '';

		try {
			while (true) {
				const { done, value } = await reader.read();
				if (done) break;

				buffer += decoder.decode(value, { stream: true });
				const lines = buffer.split('\n');

				// Process all complete lines
				for (let i = 0; i < lines.length - 1; i++) {
					const line = lines[i].trim();
					if (line) {
						try {
							const chunk = JSON.parse(line);
							yield chunk;
						} catch (e) {
							console.error('Failed to parse chunk:', line);
						}
					}
				}

				// Keep incomplete line in buffer
				buffer = lines[lines.length - 1];
			}

			// Process final buffer content
			if (buffer.trim()) {
				try {
					const chunk = JSON.parse(buffer);
					yield chunk;
				} catch (e) {
					console.error('Failed to parse final chunk:', buffer);
				}
			}
		} finally {
			reader.releaseLock();
		}
	},

	/**
	 * Get chat history
	 */
	async history(chatId?: string, limit: number = 50): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/chat/history?chat_id=${chatId || ''}&limit=${limit}`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Get chat context (agent state, tools, etc.)
	 */
	async context(): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/chat/context`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Save a message to long-term memory
	 */
	async saveToMemory(messageId: string, chatId: string): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/chat/memory-update`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ message_id: messageId, chat_id: chatId })
		});
		return res.json();
	}
};

/**
 * Cortex Discord API Client
 */
export const discordClient = {
	/**
	 * Get Discord bot configuration (admin only)
	 */
	async getConfig(): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/discord/config`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Update Discord bot configuration (admin only)
	 */
	async updateConfig(config: Record<string, any>): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/discord/config`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(config)
		});
		return res.json();
	},

	/**
	 * Get Discord bot status
	 */
	async status(): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/discord/status`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Get Discord activity log (admin only)
	 */
	async activity(limit: number = 20): Promise<CortexResponse<any[]>> {
		const res = await fetch(`${API_BASE}/discord/activity?limit=${limit}`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	},

	/**
	 * Test Discord bot connection (admin only)
	 */
	async testConnection(): Promise<CortexResponse<any>> {
		const res = await fetch(`${API_BASE}/discord/test-connection`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' }
		});
		return res.json();
	}
};

/**
 * Cortex Store: Reactive state for Cortex features
 */
export const cortexStore = writable({
	agentReady: false,
	memoryCount: 0,
	lastDream: null as string | null,
	dreamingEnabled: false,
	discordConnected: false,
	tools: [] as any[],
	error: null as string | null
});

/**
 * Initialize Cortex store by fetching context
 */
export async function initializeCortexStore() {
	try {
		const contextRes = await chatClient.context();
		if (contextRes.status === 'ok') {
			const context = contextRes.data || {};
			cortexStore.update((state) => ({
				...state,
				agentReady: context.agent_ready || false,
				memoryCount: context.memory_entries || 0,
				lastDream: context.last_dream || null,
				tools: context.available_tools || [],
				error: null
			}));
		}
	} catch (error) {
		console.error('Failed to initialize Cortex store:', error);
		cortexStore.update((state) => ({
			...state,
			error: error instanceof Error ? error.message : 'Unknown error'
		}));
	}
}
