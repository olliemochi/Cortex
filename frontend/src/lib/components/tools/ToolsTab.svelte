<!-- Source: NEW - Cortex Tools Tab
CORTEX MODIFICATION: UI component for listing and executing tools/skills -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { toolsClient } from '$lib/api/cortex';

	interface Tool {
		name: string;
		description: string;
		status: string;
		last_used?: string;
	}

	let tools: Tool[] = [];
	let loading = false;
	let error = '';
	let expandedTool: number | null = null;
	let selectedTool: Tool | null = null;
	let executing = false;

	onMount(async () => {
		await loadTools();
	});

	async function loadTools() {
		loading = true;
		try {
			const response = await toolsClient.list();
			if (response.status === 'ok') {
				tools = response.data || [];
			} else {
				error = response.error || 'Failed to load tools';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
		loading = false;
	}

	async function executeTool(toolName: string) {
		executing = true;
		try {
			const response = await toolsClient.execute(toolName, {});
			if (response.status === 'ok') {
				error = '';
			} else {
				error = response.error || 'Execution failed';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
		executing = false;
	}

	function toggleExpand(index: number) {
		expandedTool = expandedTool === index ? null : index;
	}
</script>

<div class="tools-tab">
	<div class="tab-header">
		<h3>Available Tools & Skills</h3>
		<span class="count">{tools.length}</span>
	</div>

	{#if error}
		<div class="error-message">{error}</div>
	{/if}

	<div class="controls">
		<button on:click={loadTools} disabled={loading}>Refresh</button>
	</div>

	<div class="tools-list">
		{#if loading}
			<p class="loading">Loading tools...</p>
		{:else if tools.length === 0}
			<p class="empty">No tools available.</p>
		{:else}
			{#each tools as tool, idx}
				<div class="tool-item" class:expanded={expandedTool === idx} class:active={tool.status === 'active'}>
					<button class="tool-header" on:click={() => toggleExpand(idx)}>
						<span class="name">{tool.name}</span>
						<span class="status-badge" class:active={tool.status === 'active'}>{tool.status}</span>
						<span class="icon">{expandedTool === idx ? '▼' : '▶'}</span>
					</button>
					{#if expandedTool === idx}
						<div class="tool-details">
							<p class="description">{tool.description}</p>
							{#if tool.last_used}
								<p class="last-used"><strong>Last used:</strong> {new Date(tool.last_used).toLocaleString()}</p>
							{/if}
							<div class="actions">
								<button on:click={() => executeTool(tool.name)} disabled={executing || tool.status !== 'active'}>
									{executing ? 'Executing...' : 'Execute'}
								</button>
							</div>
						</div>
					{/if}
				</div>
			{/each}
		{/if}
	</div>
</div>

<style>
  .tools-tab {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	padding: 1rem;
	height: 100%;
	overflow-y: auto;
  }

  .tab-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 0.5rem;
  }

  .tab-header h3 {
	margin: 0;
	font-size: 1.1rem;
  }

  .count {
	font-size: 0.85rem;
	color: #999;
  }

  .error-message {
	padding: 0.75rem;
	background-color: #e74c3c;
	color: white;
	border-radius: 0.25rem;
	font-size: 0.9rem;
  }

  .controls {
	display: flex;
	gap: 0.5rem;
  }

  .controls button {
	padding: 0.5rem 1rem;
	background-color: #4a90e2;
	color: white;
	border: none;
	border-radius: 0.25rem;
	cursor: pointer;
	font-size: 0.9rem;
  }

  .controls button:hover:not(:disabled) {
	background-color: #357abd;
  }

  .controls button:disabled {
	background-color: #555;
	cursor: not-allowed;
	opacity: 0.5;
  }

  .tools-list {
	flex: 1;
	overflow-y: auto;
  }

  .loading,
  .empty {
	text-align: center;
	color: #999;
	padding: 1rem;
	font-size: 0.9rem;
  }

  .tool-item {
	margin-bottom: 0.5rem;
	border: 1px solid #333;
	border-radius: 0.25rem;
  }

  .tool-item.active {
	border-color: #27ae60;
	background-color: rgba(39, 174, 96, 0.1);
  }

  .tool-header {
	width: 100%;
	display: flex;
	justify-content: flex-start;
	align-items: center;
	gap: 0.75rem;
	padding: 0.75rem;
	background-color: #2a2a2a;
	border: none;
	cursor: pointer;
	text-align: left;
  }

  .tool-header:hover {
	background-color: #333;
  }

  .name {
	flex: 1;
	font-size: 0.9rem;
  }

  .status-badge {
	font-size: 0.75rem;
	padding: 0.25rem 0.5rem;
	background-color: #555;
	border-radius: 0.25rem;
	flex-shrink: 0;
  }

  .status-badge.active {
	background-color: #27ae60;
  }

  .icon {
	font-size: 0.75rem;
	color: #666;
	flex-shrink: 0;
  }

  .tool-details {
	padding: 0.75rem;
	background-color: #1e1e1e;
	font-size: 0.9rem;
  }

  .description {
	margin: 0 0 0.5rem 0;
	line-height: 1.4;
  }

  .last-used {
	margin: 0.5rem 0;
	font-size: 0.85rem;
	color: #999;
  }

  .actions {
	display: flex;
	gap: 0.5rem;
	margin-top: 0.75rem;
  }

  .actions button {
	flex: 1;
	padding: 0.4rem;
	background-color: #4a90e2;
	color: white;
	border: none;
	border-radius: 0.25rem;
	cursor: pointer;
	font-size: 0.85rem;
  }

  .actions button:hover {
	background-color: #357abd;
  }

  .actions button:disabled {
	background-color: #555;
	cursor: not-allowed;
	opacity: 0.5;
  }
</style>
