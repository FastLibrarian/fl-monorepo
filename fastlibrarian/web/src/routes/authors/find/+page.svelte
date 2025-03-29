<script lang="ts">
	import { api, type Author } from '$lib/api/client';
	import Nav from '$lib/components/Nav.svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let loading = false;
	let error: string | null = null;
	let name = $page.url.searchParams.get('name') || '';
</script>

<Nav />

<main class="p-7">
	<div class="mx-auto max-w-2xl">
		<h1 class="mb-8 text-3xl font-bold text-gray-900">Search Results for: {name}</h1>
		{#if name}
			{#await api.findAuthor({ name })}
				<div class="flex justify-center">
					<div
						class="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"
					></div>
				</div>
			{:then authors}
				{#if authors.length === 0}
					<p class="text-gray-600">No authors found</p>
				{:else}
					<div class="grid gap-4">
						{#each authors as author}
							<div class="rounded-lg bg-white p-4 shadow">
								<h2 class="text-xl font-semibold">{author.name}</h2>
								<button
									class="mt-2 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
									on:click={() => goto(`/authors/${author.id}`)}
								>
									View Details
								</button>
							</div>
						{/each}
					</div>
				{/if}
			{:catch err}
				<p class="text-red-600">Error: {err.message}</p>
			{/await}
		{:else}
			<p class="text-gray-600">No search query provided</p>
		{/if}
	</div>
</main>
