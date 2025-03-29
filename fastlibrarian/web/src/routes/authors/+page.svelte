<script lang="ts">
	import { onMount } from 'svelte';
	import Nav from '$lib/components/Nav.svelte';
	import { api } from '$lib/api/client';

	let loading = true;
	let error: string | null = null;
	let authors = [];
	let currentPage = 1;
	const itemsPerPage = 20;

	async function loadAuthors(page: number) {
		try {
			loading = true;
			const skip = (page - 1) * itemsPerPage;
			const data = await api.getAuthors(skip, itemsPerPage);
			authors = data;
			error = null;
		} catch (e) {
			console.error('Error loading authors:', e);
			error = 'Failed to load authors';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		loadAuthors(currentPage);
	});

	function handleNextPage() {
		currentPage += 1;
		loadAuthors(currentPage);
	}

	function handlePrevPage() {
		if (currentPage > 1) {
			currentPage -= 1;
			loadAuthors(currentPage);
		}
	}
</script>

<Nav />

<main class="p-8">
	<div class="mx-auto max-w-6xl">
		<div class="mb-8 flex items-center justify-between">
			<h1 class="text-3xl font-bold text-gray-900">Authors</h1>
			<a href="/authors/new" class="rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600">
				Add New Author
			</a>
		</div>

		{#if loading}
			<div class="flex justify-center py-8">
				<div class="h-8 w-8 animate-spin rounded-full border-b-2 border-gray-900"></div>
			</div>
		{:else if error}
			<div class="rounded border border-red-400 bg-red-100 px-4 py-3 text-red-700">
				{error}
			</div>
		{:else if authors.length === 0}
			<div class="py-8 text-center text-gray-500">No authors found</div>
		{:else}
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
				{#each authors as author}
					<div class="rounded-lg bg-white p-6 shadow-md transition-shadow hover:shadow-lg">
						<h2 class="mb-2 text-xl font-semibold">
							<a href="/authors/{author.id}" class="text-blue-600 hover:text-blue-800">
								{author.name}
							</a>
						</h2>
						{#if author.book_count !== null}
							<p class="text-gray-600">
								{author.book_count}
								{author.book_count === 1 ? 'book' : 'books'}
							</p>
						{/if}
					</div>
				{/each}
			</div>

			<div class="mt-8 flex justify-center gap-4">
				<button
					class="rounded-md bg-gray-200 px-4 py-2 disabled:opacity-50"
					on:click={handlePrevPage}
					disabled={currentPage === 1}
				>
					Previous
				</button>
				<span class="py-2">Page {currentPage}</span>
				<button
					class="rounded-md bg-gray-200 px-4 py-2 disabled:opacity-50"
					on:click={handleNextPage}
					disabled={authors.length < itemsPerPage}
				>
					Next
				</button>
			</div>
		{/if}
	</div>
</main>
