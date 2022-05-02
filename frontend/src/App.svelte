<script>
	import Tailwindcss from './Tailwindcss.svelte';
	import Sidebar from './Sidebar.svelte';
	import Map from './Map.svelte';
	export let name;
</script>

<Tailwindcss />
<Sidebar />
<Map lat={-37.8136} lon={144.9631} zoom={10.7}/>


