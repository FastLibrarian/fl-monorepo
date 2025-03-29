<script lang="ts">
	import { onMount } from 'svelte';
	import Nav from '$lib/components/Nav.svelte';
	import { api, type Book, type Author } from '$lib/api/client';

	let loading = true;
	let recentBooks = [];
	let stats = {
		totalBooks: 0,
		totalAuthors: 0
	};

	onMount(async () => {
		try {
			const [books, authors] = await Promise.all([api.getBooks(), api.getAuthors()]);

			recentBooks = books.slice(0, 5);
			stats.totalBooks = books.length;
			stats.totalAuthors = authors.length;
		} catch (e) {
			console.error('Error loading dashboard data:', e);
		} finally {
			loading = false;
		}
	});

	async function handleAddBook() {
		window.location.href = '/books/new';
	}

	async function handleScanLibrary() {
		// TODO: Implement library scanning
		alert('Library scanning not implemented yet');
	}
</script>

<Nav />

<main>
	<h1>Dashboard</h1>

	<div class="dashboard-grid">
		<div class="card">
			<h2>Recent Books</h2>

			{#if loading}
				<p>Loading books...</p>
			{:else if recentBooks.length === 0}
				<p>No books added yet</p>
			{:else}
				<ul class="book-list">
					{#each recentBooks as book}
						<li>
							<span class="book-title">{book.title}</span>
							<span class="book-author">{book.author}</span>
						</li>
					{/each}
				</ul>
			{/if}
		</div>

		<div class="card">
			<h2>Statistics</h2>
			<p>Total Books: {stats.totalBooks}</p>
			<p>Total Authors: {stats.totalAuthors}</p>
		</div>

		<div class="card">
			<h2>Quick Actions</h2>
			<button on:click={handleAddBook}>Add New Book</button>
			<button on:click={handleScanLibrary}>Scan Library</button>
		</div>
	</div>
</main>

<style>
	main {
		padding: 2rem;
	}

	h1 {
		color: #2c3e50;
		margin-bottom: 2rem;
	}

	.dashboard-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 2rem;
	}

	.card {
		background: white;
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	button {
		background: #3498db;
		color: white;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		margin: 0.5rem;
		cursor: pointer;
	}

	button:hover {
		background: #2980b9;
	}

	.book-list {
		list-style: none;
		padding: 0;
	}
	.book-list li {
		padding: 0.5rem 0;
		border-bottom: 1px solid #eee;
	}
	.book-title {
		font-weight: bold;
		display: block;
	}
	.book-author {
		color: #666;
		font-size: 0.9em;
	}
	.error {
		color: red;
	}
</style>
