<script lang="ts">
	import { api } from '$lib/api/client';
	import Nav from '$lib/components/Nav.svelte';
	import { goto } from '$app/navigation';

	let loading = false;
	let error: string | null = null;
	let name = '';

	async function handleSubmit() {
		try {
			loading = true;
			error = null;
			await goto(`/authors/find?name=${encodeURIComponent(name)}`);
		} catch (e) {
			console.error('Error searching for author:', e);
			error = 'Failed to search for author';
		} finally {
			loading = false;
		}
	}
</script>

<Nav />

<main class="p-8">
	<div class="mx-auto max-w-2xl">
		<h1 class="mb-8 text-3xl font-bold text-gray-900">Add New Author</h1>

		<form on:submit|preventDefault={handleSubmit} class="space-y-6">
			{#if error}
				<div class="rounded border border-red-400 bg-red-100 px-4 py-3 text-red-700">
					{error}
				</div>
			{/if}

			<div>
				<label for="name" class="block text-sm font-medium text-gray-700">Author Name</label>
				<input
					type="text"
					id="name"
					bind:value={name}
					required
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<button
					type="submit"
					disabled={loading}
					class="w-full rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:opacity-50"
				>
					{loading ? 'Searching...' : 'Find Author'}
				</button>
			</div>
		</form>
	</div>
</main>
