<script>
	import { onMount } from 'svelte';
	import Nav from '$lib/components/Nav.svelte';
	import { api } from '$lib/api/client';

	let activeTab = 'books';

	// Form data objects for each section
	let bookSettings = {
		defaultPath: '',
		allowedFormats: ['epub', 'pdf', 'mobi'],
		autoScan: false
	};

	let authorSettings = {
		preferredNameFormat: 'lastname_first',
		fetchMetadata: true
	};

	let audioSettings = {
		audioPath: '',
		supportedFormats: ['mp3', 'm4b', 'aac']
	};

	let backupSettings = {
		backupPath: '',
		autoBackup: false,
		backupFrequency: 'weekly'
	};

	let apiKeys = {
		googleBooks: '',
		openLibrary: ''
	};

	function saveConfig() {
		// TODO: Implement save functionality
		console.log('Saving configuration...');
	}

	function importConfig() {
		// TODO: Implement import functionality
		console.log('Importing configuration...');
	}

	function restoreConfig() {
		// TODO: Implement restore functionality
		console.log('Restoring configuration...');
	}
</script>

<Nav />
<div class="config-container">
	<h1>Configuration</h1>

	<div class="tabs">
		<button class:active={activeTab === 'books'} on:click={() => (activeTab = 'books')}
			>Book Settings</button
		>
		<button class:active={activeTab === 'authors'} on:click={() => (activeTab = 'authors')}
			>Author Settings</button
		>
		<button class:active={activeTab === 'audio'} on:click={() => (activeTab = 'audio')}
			>Audiobook Settings</button
		>
		<button class:active={activeTab === 'import'} on:click={() => (activeTab = 'import')}
			>Import</button
		>
		<button class:active={activeTab === 'backup'} on:click={() => (activeTab = 'backup')}
			>Backup & Restore</button
		>
		<button class:active={activeTab === 'api'} on:click={() => (activeTab = 'api')}>API Keys</button
		>
	</div>

	<div class="content">
		{#if activeTab === 'books'}
			<section>
				<h2>Book Settings</h2>
				<label>
					Default Library Path:
					<input type="text" bind:value={bookSettings.defaultPath} />
				</label>
				<label>
					Auto-scan Library:
					<input type="checkbox" bind:checked={bookSettings.autoScan} />
				</label>
			</section>
		{:else if activeTab === 'authors'}
			<section>
				<h2>Author Settings</h2>
				<label>
					Preferred Name Format:
					<select bind:value={authorSettings.preferredNameFormat}>
						<option value="lastname_first">Lastname, Firstname</option>
						<option value="firstname_first">Firstname Lastname</option>
					</select>
				</label>
			</section>
		{:else if activeTab === 'audio'}
			<section>
				<h2>Audiobook Settings</h2>
				<label>
					Audiobook Library Path:
					<input type="text" bind:value={audioSettings.audioPath} />
				</label>
			</section>
		{:else if activeTab === 'backup'}
			<section>
				<h2>Backup & Restore</h2>
				<label>
					Backup Location:
					<input type="text" bind:value={backupSettings.backupPath} />
				</label>
				<label>
					Auto Backup:
					<input type="checkbox" bind:checked={backupSettings.autoBackup} />
				</label>
				<label>
					Backup Frequency:
					<select bind:value={backupSettings.backupFrequency}>
						<option value="daily">Daily</option>
						<option value="weekly">Weekly</option>
						<option value="monthly">Monthly</option>
					</select>
				</label>
			</section>
		{:else if activeTab === 'import'}
			<section>
				<h2>Import Settings</h2>
				<label>
					Import Type:
					<select bind:value={importSettings.type}>
						<option value="readarr">Readarr</option>
						<option value="lazylibrarian">LazyLibrarian</option>
					</select>
				</label>
				<label>
					URL:
					<input type="text" bind:value={importSettings.url} />
				</label>
				<label>
					API Key:
					<input type="password" bind:value={importSettings.apiKey} />
				</label>
			</section>

			<div class="button-group">
				<button on:click={importConfig}>Import Configuration</button>
				<button on:click={restoreConfig}>Restore Configuration</button>
			</div>
		{:else if activeTab === 'api'}
			<section>
				<h2>API Keys</h2>
				<label>
					Google Books API Key:
					<input type="password" bind:value={apiKeys.googleBooks} />
				</label>
				<label>
					Open Library API Key:
					<input type="password" bind:value={apiKeys.openLibrary} />
				</label>
			</section>
		{/if}
	</div>

	<div class="actions">
		<button class="save-button" on:click={saveConfig}>Save Configuration</button>
	</div>
</div>

<style>
	.config-container {
		max-width: 800px;
		margin: 0 auto;
		padding: 20px;
	}

	.tabs {
		display: flex;
		gap: 10px;
		margin-bottom: 20px;
	}

	.tabs button {
		padding: 10px 20px;
		border: none;
		background: #f0f0f0;
		cursor: pointer;
	}

	.tabs button.active {
		background: #007bff;
		color: white;
	}

	.content {
		background: white;
		padding: 20px;
		border-radius: 4px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	section {
		display: flex;
		flex-direction: column;
		gap: 15px;
	}

	label {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}

	input[type='text'],
	input[type='password'],
	select {
		padding: 8px;
		border: 1px solid #ddd;
		border-radius: 4px;
	}

	.button-group {
		display: flex;
		gap: 10px;
	}

	.actions {
		margin-top: 20px;
		text-align: right;
	}

	.save-button {
		padding: 10px 20px;
		background: #28a745;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.save-button:hover {
		background: #218838;
	}
</style>
