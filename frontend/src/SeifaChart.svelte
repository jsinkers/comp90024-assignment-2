<!-- based on https://svelte.dev/examples/scatterplot-->
<script>
	import BarChart from "./BarChart.svelte";
</script>

<div class="container">
	<div class="flex-item">
		<h1>Tweet counts for different election issues</h1>
		<div class="chart">
			<!-- TODO: bar chart -->
			<BarChart/>
		</div>
	</div>
	<div class="flex-item">
		<h1>Mean tweet sentiment by election issue</h1>
		<div class="chart">
			<!-- TODO: bar chart -->
			<BarChart/>
		</div>
	</div>
</div>

<style>
   .container {
        @apply h-full w-11/12 absolute right-0 top-0;
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
</style>