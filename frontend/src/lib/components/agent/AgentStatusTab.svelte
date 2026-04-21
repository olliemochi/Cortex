<!-- Source: NEW - Cortex Agent Status Tab
CORTEX MODIFICATION: UI component for viewing agent system status -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { chatClient, cortexStore } from '$lib/api/cortex';

	let context: any = null;
	let loading = false;
	let error = '';
	let refreshInterval: NodeJS.Timeout | null = null;

	onMount(async () => {
		await loadStatus();
		// Auto-refresh every 5 seconds
		refreshInterval = setInterval(loadStatus, 5000);
		return () => {
			if (refreshInterval) clearInterval(refreshInterval);
		};
	});

	async function loadStatus() {
		loading = true;
		try {
			const response = await chatClient.context();
			if (response.status === 'ok') {
				context = response.data;
			} else {
				error = response.error || 'Failed to load status';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
		loading = false;
	}
</script>

<div class="agent-status-tab">
	<div class="tab-header">
		<h3>System Status</h3>
		<button on:click={loadStatus} disabled={loading} class="refresh-btn">⟳</button>
	</div>

	{#if error}
		<div class="error-message">{error}</div>
	{/if}

	{#if loading && !context}
		<p class="loading">Loading status...</p>
	{:else if context}
		<div class="status-cards">
			<div class="status-card">
				<h4>Agent</h4>
				<div class="status-value" class:active={context.agent_ready}>
					{context.agent_ready ? '✓ Ready' : '✗ Unavailable'}
				</div>
			</div>

			<div class="status-card">
				<h4>Memory Entries</h4>
				<div class="status-value">{context.memory_entries || 0}</div>
			</div>

			<div class="status-card">
				<h4>Last Dream</h4>
				<div class="status-value">{context.last_dream ? new Date(context.last_dream).toLocaleString() : 'Never'}</div>
			</div>

			<div class="status-card">
				<h4>Discord Bot</h4>
				<div class="status-value" class:connected={context.discord_status === 'connected'}>
					{context.discord_status}
				</div>
			</div>

			<div class="status-card full-width">
				<h4>Available Tools</h4>
				<div class="tools-list">
					{#if context.available_tools && context.available_tools.length > 0}
						{#each context.available_tools as tool}
							<span class="tool-tag">{tool}</span>
						{/each}
					{:else}
						<span class="empty">No tools available</span>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
  .agent-status-tab {
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

  .refresh-btn {
	background: none;
	border: none;
	cursor: pointer;
	font-size: 1.1rem;
	color: #4a90e2;
	padding: 0;
	width: 24px;
	height: 24px;
	display: flex;
	align-items: center;
	justify-content: center;
  }

  .refresh-btn:hover {
	color: #357abd;
  }

  .refresh-btn:disabled {
	color: #555;
	cursor: not-allowed;
  }

  .error-message {
	padding: 0.75rem;
	background-color: #e74c3c;
	color: white;
	border-radius: 0.25rem;
	font-size: 0.9rem;
  }

  .loading {
	text-align: center;
	color: #999;
	padding: 1rem;
	font-size: 0.9rem;
  }

  .status-cards {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 0.75rem;
  }

  .status-card {
	background-color: #2a2a2a;
	border: 1px solid #333;
	border-radius: 0.25rem;
	padding: 0.75rem;
  }

  .status-card.full-width {
	grid-column: 1 / -1;
  }

  .status-card h4 {
	margin: 0 0 0.5rem 0;
	font-size: 0.85rem;
	text-transform: uppercase;
	color: #999;
	letter-spacing: 0.05em;
  }

  .status-value {
	font-size: 0.95rem;
	font-weight: 500;
	color: #ccc;
  }

  .status-value.active {
	color: #27ae60;
  }

  .status-value.connected {
	color: #27ae60;
  }

  .tools-list {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
  }

  .tool-tag {
	display: inline-block;
	padding: 0.25rem 0.75rem;
	background-color: #4a90e2;
	color: white;
	border-radius: 0.25rem;
	font-size: 0.8rem;
  }

  .tools-list .empty {
	color: #999;
	font-style: italic;
  }
</style>
