<!-- Source: NEW - Cortex Memory Tab
CORTEX MODIFICATION: UI component for viewing and managing long-term memory -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { memoryClient } from '$lib/api/cortex';

	interface MemoryEntry {
		id?: number;
		category: string;
		title: string;
		content: string;
		importance: number;
		date: string;
		status: string;
	}

	let memories: MemoryEntry[] = [];
	let loading = false;
	let error = '';
	let expandedMemory: number | null = null;
	let searchQuery = '';
	let searchResults: MemoryEntry[] = [];
	let showSearchResults = false;

	onMount(async () => {
		await loadMemories();
	});

	async function loadMemories() {
		loading = true;
		try {
			const response = await memoryClient.list();
			if (response.status === 'ok') {
				memories = response.data || [];
			} else {
				error = response.error || 'Failed to load memories';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
		loading = false;
	}

	async function search() {
		if (!searchQuery.trim()) {
			showSearchResults = false;
			return;
		}

		loading = true;
		try {
			const response = await memoryClient.search(searchQuery);
			if (response.status === 'ok') {
				searchResults = response.data || [];
				showSearchResults = true;
			} else {
				error = response.error || 'Search failed';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
		loading = false;
	}

	async function promote(id: number | undefined) {
		if (!id) return;
		try {
			const response = await memoryClient.promote(id);
			if (response.status === 'ok') {
				await loadMemories();
				showSearchResults = false;
			} else {
				error = response.error || 'Failed to promote';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
	}

	async function deleteEntry(id: number | undefined) {
		if (!id) return;
		try {
			const response = await memoryClient.delete(id);
			if (response.status === 'ok') {
				await loadMemories();
				showSearchResults = false;
			} else {
				error = response.error || 'Failed to delete';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		}
	}

	function toggleExpand(index: number) {
		expandedMemory = expandedMemory === index ? null : index;
	}

	function getDisplayMemories() {
		return showSearchResults ? searchResults : memories;
	}
</script>

<div class="memory-tab">
	<div class="tab-header">
		<h3>Long-term Memory</h3>
		<span class="count">{memories.length} entries</span>
	</div>

	{#if error}
		<div class="error-message">{error}</div>
	{/if}

	<div class="search-box">
		<input type="text" placeholder="Search memories..." bind:value={searchQuery} on:keydown={(e) => e.key === 'Enter' && search()} />
		<button on:click={search} disabled={loading || !searchQuery.trim()}>Search</button>
		{#if showSearchResults}
			<button on:click={() => { showSearchResults = false; searchQuery = ''; }}>Clear</button>
		{/if}
	</div>

	<div class="memories-list">
		{#if loading}
			<p class="loading">Loading memories...</p>
		{:else if getDisplayMemories().length === 0}
			<p class="empty">{showSearchResults ? 'No results found' : 'No memories recorded yet. Use /memory add to start recording.'}</p>
		{:else}
			{#each getDisplayMemories() as memory, idx}
				<div class="memory-item" class:expanded={expandedMemory === idx} class:promoted={memory.status === 'promoted'}>
					<button class="memory-header" on:click={() => toggleExpand(idx)}>
						<span class="category">[{memory.category}]</span>
						<span class="title">{memory.title}</span>
						<span class="importance">★ {memory.importance || 5}</span>
						<span class="icon">{expandedMemory === idx ? '▼' : '▶'}</span>
					</button>
					{#if expandedMemory === idx}
						<div class="memory-details">
							<p class="content">{memory.content}</p>
							<div class="meta">
								<span class="date">{new Date(memory.date).toLocaleDateString()}</span>
								<span class="status">{memory.status}</span>
							</div>
							<div class="actions">
								<button on:click={() => promote(memory.id)} disabled={memory.status === 'promoted'}>
									Promote
								</button>
								<button on:click={() => deleteEntry(memory.id)} class="delete">Delete</button>
							</div>
						</div>
					{/if}
				</div>
			{/each}
		{/if}
	</div>
</div>

<style>
	.memory-tab {
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

	.search-box {
		display: flex;
		gap: 0.5rem;
	}

	.search-box input {
		flex: 1;
		padding: 0.5rem;
		background-color: #2a2a2a;
		border: 1px solid #444;
		border-radius: 0.25rem;
		color: white;
		font-size: 0.9rem;
	}

	.search-box input::placeholder {
		color: #666;
	}

	.search-box button {
		padding: 0.5rem 1rem;
		background-color: #4a90e2;
		color: white;
		border: none;
		border-radius: 0.25rem;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.search-box button:hover:not(:disabled) {
		background-color: #357abd;
	}

	.search-box button:disabled {
		background-color: #555;
		cursor: not-allowed;
		opacity: 0.5;
	}

	.memories-list {
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

	.memory-item {
		margin-bottom: 0.5rem;
		border: 1px solid #333;
		border-radius: 0.25rem;
	}

	.memory-item.promoted {
		border-color: #f39c12;
		background-color: rgba(243, 156, 18, 0.1);
	}

	.memory-header {
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

	.memory-header:hover {
		background-color: #333;
	}

	.category {
		font-size: 0.75rem;
		color: #4a90e2;
		font-weight: bold;
		flex-shrink: 0;
	}

	.title {
		flex: 1;
		font-size: 0.9rem;
	}

	.importance {
		font-size: 0.85rem;
		color: #f39c12;
		flex-shrink: 0;
	}

	.icon {
		font-size: 0.75rem;
		color: #666;
		flex-shrink: 0;
	}

	.memory-details {
		padding: 0.75rem;
		background-color: #1e1e1e;
		font-size: 0.9rem;
	}

	.content {
		margin: 0 0 0.5rem 0;
		line-height: 1.4;
		white-space: pre-wrap;
		word-wrap: break-word;
	}

	.meta {
		display: flex;
		gap: 1rem;
		margin: 0.5rem 0;
		font-size: 0.85rem;
		color: #999;
	}

	.status {
		text-transform: capitalize;
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

	.actions button.delete {
		background-color: #e74c3c;
	}

	.actions button.delete:hover {
		background-color: #c0392b;
	}
</style>
