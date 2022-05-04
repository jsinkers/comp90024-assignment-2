<script>
	import Tailwindcss from './Tailwindcss.svelte';
	import Sidebar from './Sidebar.svelte';
	import Map from './Map.svelte';
	import Landing from './Landing.svelte';
	export let name;
</script>

<Tailwindcss />
<Landing/>
<Sidebar />
<Map lat={-37.8136} lon={144.9631} zoom={9} />
