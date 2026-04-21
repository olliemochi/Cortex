<!-- Source: NEW - Cortex Dreams Tab
CORTEX MODIFICATION: UI component for viewing and managing dream cycles -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { dreamingClient } from '$lib/api/cortex';

	interface Dream {
		timestamp: string;
		phase: string;
		duration: number;
		insights: string[];
		memories_processed: number;
	}

	let dreams: Dream[] = [];
	let currentStatus: any = null;
	let loading = false;
	let error = '';
	let expandedDream: number | null = null;

	onMount(async () => {
		await loadDreams();
		await loadStatus();
	});

	async function loadDreams() {
		loading = true;
		try {
			const response = await dreamingClient.history(20);
			if (response.status === 'ok') {
				dreams = response.data || [];
			} else {
				error = response.error || 'Failed to load dreams';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
		loading = false;
	}

	async function loadStatus() {
		try {
			const response = await dreamingClient.status();
			if (response.status === 'ok') {
				currentStatus = response.data;
			}
		} catch (e) {
			console.error('Failed to load status:', e);
		}
	}

	async function startDream() {
		loading = true;
		try {
			const response = await dreamingClient.run();
			if (response.status === 'ok') {
				currentStatus = response.data;
				await new Promise((r) => setTimeout(r, 500));
				await loadDreams();
			} else {
				error = response.error || 'Failed to start dream';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
		loading = false;
	}

	async function cancelDream() {
		try {
			const response = await dreamingClient.cancel();
			if (response.status === 'ok') {
				currentStatus = response.data;
			} else {
				error = response.error || 'Failed to cancel dream';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
	}

	function toggleExpand(index: number) {
		expandedDream = expandedDream === index ? null : index;
	}
</script>

<div class="dreams-tab">
	<div class="tab-header">
		<h3>Dreams & Memory Consolidation</h3>
		<div class="status-badge" class:active={currentStatus?.enabled}>
			{currentStatus?.phase || 'waking'}
		</div>
	</div>

	{#if error}
		<div class="error-message">{error}</div>
	{/if}

	<div class="controls">
		<button on:click={startDream} disabled={loading || currentStatus?.phase !== 'waking'}>
			{loading ? 'Processing...' : 'Start Dream Cycle'}
		</button>
		<button on:click={cancelDream} disabled={loading || currentStatus?.phase === 'waking'}>
			Cancel
		</button>
		<button on:click={loadDreams} disabled={loading}>
			Refresh
		</button>
	</div>

	<div class="status-info">
		<p><strong>Status:</strong> {currentStatus?.phase || 'unknown'}</p>
		{#if currentStatus?.last_cycle}
			<p><strong>Last Cycle:</strong> {currentStatus.last_cycle}</p>
		{/if}
		{#if currentStatus?.next_cycle}
			<p><strong>Next Cycle:</strong> {currentStatus.next_cycle}</p>
		{/if}
	</div>

	<div class="dreams-list">
		{#if loading}
			<p class="loading">Loading dream history...</p>
		{:else if dreams.length === 0}
			<p class="empty">No dreams recorded yet. Start a dream cycle to begin.</p>
		{:else}
			{#each dreams as dream, idx}
				<div class="dream-item" class:expanded={expandedDream === idx}>
					<button class="dream-header" on:click={() => toggleExpand(idx)}>
						<span class="timestamp">{new Date(dream.timestamp).toLocaleString()}</span>
						<span class="duration">{dream.duration}m</span>
						<span class="icon">{expandedDream === idx ? '▼' : '▶'}</span>
					</button>
					{#if expandedDream === idx}
						<div class="dream-details">
							<p><strong>Phase:</strong> {dream.phase}</p>
							<p><strong>Memories Processed:</strong> {dream.memories_processed}</p>
							{#if dream.insights && dream.insights.length > 0}
								<p><strong>Insights:</strong></p>
								<ul>
									{#each dream.insights as insight}
										<li>{insight}</li>
									{/each}
								</ul>
							{/if}
						</div>
					{/if}
				</div>
			{/each}
		{/if}
	</div>
</div>

<style>
	.dreams-tab {
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

	.status-badge {
		display: inline-block;
		padding: 0.25rem 0.75rem;
		border-radius: 1rem;
		font-size: 0.85rem;
		background-color: #333;
		color: #999;
		text-transform: uppercase;
	}

	.status-badge.active {
		background-color: #4a90e2;
		color: white;
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
		flex: 1;
		padding: 0.5rem;
		border: none;
		border-radius: 0.25rem;
		background-color: #4a90e2;
		color: white;
		cursor: pointer;
		font-size: 0.9rem;
		transition: background-color 0.2s;
	}

	.controls button:hover:not(:disabled) {
		background-color: #357abd;
	}

	.controls button:disabled {
		background-color: #555;
		cursor: not-allowed;
		opacity: 0.5;
	}

	.status-info {
		padding: 0.75rem;
		background-color: #1e1e1e;
		border-radius: 0.25rem;
		font-size: 0.9rem;
	}

	.status-info p {
		margin: 0.25rem 0;
	}

	.dreams-list {
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

	.dream-item {
		margin-bottom: 0.5rem;
		border: 1px solid #333;
		border-radius: 0.25rem;
	}

	.dream-header {
		width: 100%;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem;
		background-color: #2a2a2a;
		border: none;
		cursor: pointer;
		text-align: left;
	}

	.dream-header:hover {
		background-color: #333;
	}

	.timestamp {
		flex: 1;
		font-size: 0.9rem;
	}

	.duration {
		padding: 0 0.5rem;
		font-size: 0.85rem;
		color: #999;
	}

	.icon {
		font-size: 0.75rem;
		color: #666;
	}

	.dream-details {
		padding: 0.75rem;
		background-color: #1e1e1e;
		font-size: 0.9rem;
	}

	.dream-details p {
		margin: 0.5rem 0;
	}

	.dream-details ul {
		margin: 0.5rem 0 0 1.5rem;
		padding: 0;
	}

	.dream-details li {
		margin: 0.25rem 0;
	}
</style>
