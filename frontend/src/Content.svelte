<script>
  import { getContext } from 'svelte';
  import Popup from './InfoSeifaMap.svelte';
  const { open } = getContext('simple-modal');
  const showInfo = () => open(Popup, {});
</script>

<p>
	<button on:click={showInfo}>Info</button>
</p>