<script lang="ts">
	import { api, type Book, type Author, type Series } from '$lib/api/client';
	import Nav from '$lib/components/Nav.svelte';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let loading = false;
	let error: string | null = null;
	let authors: Author[] = [];
	let series: Series[] = [];

	let title = '';
	let authorId = '';
	let publishedDate = '';
	let isbn = '';
	let pages = '';
	let language = '';
	let seriesId = '';
	let coverImage = '';

	onMount(async () => {
		try {
			const [authorData, seriesData] = await Promise.all([api.getAuthors(), api.getSeries()]);
			authors = authorData;
			series = seriesData;
		} catch (e) {
			console.error('Error loading form data:', e);
			error = 'Failed to load authors and series';
		}
	});

	async function handleSubmit() {
		try {
			loading = true;
			error = null;

			const bookData = {
				title,
				author_id: parseInt(authorId),
				published_date: publishedDate,
				isbn,
				pages: parseInt(pages),
				language,
				series_id: seriesId ? parseInt(seriesId) : undefined,
				cover_image: coverImage || undefined
			};

			const book = await api.createBook(bookData);
			goto(`/books/${book.id}`);
		} catch (e) {
			console.error('Error creating book:', e);
			error = 'Failed to create book';
		} finally {
			loading = false;
		}
	}
</script>

<Nav />

<main class="p-8">
	<div class="mx-auto max-w-2xl">
		<h1 class="mb-8 text-3xl font-bold text-gray-900">Add New Book</h1>

		<form on:submit|preventDefault={handleSubmit} class="space-y-6">
			{#if error}
				<div class="rounded border border-red-400 bg-red-100 px-4 py-3 text-red-700">
					{error}
				</div>
			{/if}

			<div>
				<label for="title" class="block text-sm font-medium text-gray-700">Title</label>
				<input
					type="text"
					id="title"
					bind:value={title}
					required
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="author" class="block text-sm font-medium text-gray-700">Author</label>
				<select
					id="author"
					bind:value={authorId}
					required
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				>
					<option value="">Select an author</option>
					{#each authors as author}
						<option value={author.id}>{author.name}</option>
					{/each}
				</select>
			</div>

			<div>
				<label for="published-date" class="block text-sm font-medium text-gray-700">
					Published Date
				</label>
				<input
					type="date"
					id="published-date"
					bind:value={publishedDate}
					required
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="isbn" class="block text-sm font-medium text-gray-700">ISBN</label>
				<input
					type="text"
					id="isbn"
					bind:value={isbn}
					required
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="pages" class="block text-sm font-medium text-gray-700">Pages</label>
				<input
					type="number"
					id="pages"
					bind:value={pages}
					required
					min="1"
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="language" class="block text-sm font-medium text-gray-700">Language</label>
				<input
					type="text"
					id="language"
					bind:value={language}
					required
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="series" class="block text-sm font-medium text-gray-700">Series</label>
				<select
					id="series"
					bind:value={seriesId}
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				>
					<option value="">None</option>
					{#each series as s}
						<option value={s.id}>{s.name}</option>
					{/each}
				</select>
			</div>

			<div>
				<label for="cover-image" class="block text-sm font-medium text-gray-700">
					Cover Image URL
				</label>
				<input
					type="url"
					id="cover-image"
					bind:value={coverImage}
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<button
					type="submit"
					disabled={loading}
					class="w-full rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:opacity-50"
				>
					{loading ? 'Creating...' : 'Create Book'}
				</button>
			</div>
		</form>
	</div>
</main>
