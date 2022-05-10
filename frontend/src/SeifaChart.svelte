<!-- based on https://svelte.dev/examples/scatterplot-->
<script>
	import BarChart from "./BarChart.svelte";
	import { writable } from 'svelte/store';
	import Modal, {bind} from 'svelte-simple-modal';
	import Popup from './InfoSeifaChart.svelte';

	const modal = writable(null);
	const showModal = () => modal.set(bind(Popup, {}));
</script>

<div class="container space-y-4">
	<div class="flex-item">
		<div class="chart">
			<BarChart title="Tweet count by election issue" variable="count"/>
		</div>
	</div>
	<div class="flex-item">
		<div class="chart">
			<BarChart title="Mean tweet sentiment by election issue" variable="compound"/>
		</div>
	</div>
</div>
<div id="info">
	<Modal show={$modal}>
		<span class="fa-solid fa-info-circle icon" on:click={showModal}></span>
	</Modal>
</div>

<style>
   .container {
        @apply h-full w-full;
        display: flex;
        flex-direction: column;
        flex-wrap: nowrap;
        justify-content: center;
        align-content: center;
    }

    .flex-item:nth-child(1) {
        order: 0;
        flex: 0 1 auto;
        align-self: auto;
    }

    .flex-item:nth-child(2) {
        order: 1;
        flex: 0 1 auto;
        align-self: auto;
    }

    .flex-item:nth-child(3) {
        order: 2;
        flex: 0 1 auto;
        align-self: auto;
    }

	h1 {
		@apply text-xl text-center;
	}

   #info {
	   @apply z-20 bg-transparent inset-0 left-4 top-4;
	   position: absolute;
	   width: fit-content;
	   height: fit-content;
   }

   .icon {
	   font-size: 1.5em;
	   padding: 1rem;
	   @apply relative flex items-center justify-center mx-auto
	   rounded-full hover:bg-blue-600 hover:text-white transition-all duration-200 ease-linear cursor-pointer;
   }
</style>