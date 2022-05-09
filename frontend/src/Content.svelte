<script>
  import { getContext } from 'svelte';
  import SeifaPopup from './InfoSeifaMap.svelte';
  // import DiversityPopup from './InfoDiversityMap.svelte';

  const { open } = getContext('simple-modal');
  const showInfoSeifa = () => open(SeifaPopup, {});
  // const showInfoDiversity = () => open(DiversityPopup, {});
</script>

<p>
	<button on:click={showInfoSeifa}>Info</button>
</p>