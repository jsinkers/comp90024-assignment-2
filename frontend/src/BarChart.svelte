<script>
	// based on https://svelte.dev/examples/bar-chart
	import { scaleLinear } from 'd3-scale';
	// title to display on the chart
	export let title;
	// data variable of interest
	export let variable;
	import { json, pointer } from 'd3';
	import {fade} from 'svelte/transition';

	let data_url = "http://melbourneliveability.live/api/analytics/socioeconomic/election-issues/";

	let ys = [];
	let issues;
	let xTicks = [];
	let yTicks;

	async function fetchData() {
		await json(data_url).then((dataset) => {
			let data = dataset.returned_data;
			issues = data.issue;
			// determine x axes
			xTicks = issues;

			// determine y axes and data
			if (variable === 'compound') {
				ys = data.mean_compound;
				// Math.max(...ys.map(Math.abs))
				yTicks = [-1, -0.5, 0, 0.5, 1];
			} else if (variable === 'count') {
				ys = data.count;
				yTicks = [];
				let step = 500;
				let max_y_tick = Math.ceil(Math.max(...ys)/step)*step;
				for (let i = 0; i <= max_y_tick; i += step) {
					yTicks.push(i);
				}
			}
		});
		return {"issues": issues, "ys": ys, "xTicks": xTicks, "yTicks": yTicks};
	}

	const padding = { top: 20, right: 15, bottom: 20, left: 25 };
	let width = 650;
	let height = 300;

	$: xScale = scaleLinear()
			.domain([0, xTicks.length])
			.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
			.domain([Math.min.apply(null, yTicks), Math.max.apply(null, yTicks)])
			.range([height - padding.bottom, padding.top]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / xTicks.length - 10;

	let tooltip;
	let opacity;
	let tooltip_left;
	let tooltip_top;
	let mouse_x;
	let mouse_y;
	let selected_point = undefined;

	const setMousePosition = function(event) {
		mouse_x = event.clientX;
		mouse_y = event.clientY;
	}

	let mousemove = function(d) {
		tooltip_left = (pointer(d)[0] + 20) + "px";
		tooltip_top = (pointer(d)[1] - 20 ) + "px";
	}
</script>

<h2>{title}</h2>

<div class="chart" bind:clientHeight={height}>
	<svg style="width: {width}; height: {height}">
		{#await fetchData()}
			<p>Loading</p>
		{:then chartData}
			<!-- y axis -->
			<g class="axis y-axis">
				{#each chartData.yTicks as tick}
					<g class="tick tick-{tick}" transform="translate(0, {yScale(tick)})">
						<line x2="100%"></line>
						<text y="-4">{tick}</text>
					</g>
				{/each}
			</g>
			<!-- x axis -->
			<g class="axis x-axis">
				{#each chartData.issues as issue, i}
					<g class="tick" transform="translate({xScale(i)},{height})">
						<text x="{barWidth/2}" y="-4">{issue}</text>
					</g>
				{/each}
			</g>

			<g class='bars'>
				{#each chartData.ys as point, i}
					<rect
							x="{xScale(i) + 2}"
							y="{Math.min(yScale(point), yScale(0))}"
							height="{Math.abs(yScale(0)-yScale(point))}"
							width="{barWidth}"
							on:mousemove={mousemove}
							on:mouseover={(event) => {selected_point = point; setMousePosition(event)}}
							on:mouseout={() => {selected_point = undefined}}
					></rect>
				{/each}
			</g>
		{:catch error}
			<p>{error.message}</p>
		{/await}
	</svg>
	{#if selected_point != undefined}
		<div transition:fade class="tooltip" bind:this={tooltip} opacity={opacity} style="left: {tooltip_left}; top: {tooltip_top}">
			<p>{variable}: {selected_point}</p>
		</div>
	{/if}
</div>

<style>
	h2 {
		text-align: center;
	}

	.chart {
		width: 100%;
		/*max-width: 500px;*/
		margin: 0 auto;
		display: flex;
		justify-content: center;
	}

	svg {
		display: block;
		position: relative;
		/*width: 100%;*/
		overflow: visible;
	}

	.tick {
		font-family: Helvetica, Arial;
		font-size: .725em;
		font-weight: 200;
	}

	.tick line {
		stroke: #e2e2e2;
		stroke-dasharray: 2;
	}

	.tick text {
		fill: #ccc;
		text-anchor: start;
	}

	.tick.tick-0 line {
		stroke-dasharray: 0;
	}

	.x-axis .tick text {
		text-anchor: middle;
	}

	.bars rect {
		fill: #a11;
		stroke: none;
		opacity: 0.65;
	}

	.tooltip {
		position: absolute;
		text-align: center;
		padding: 10px;
		background: white;
		font-size: small;
		border: 1px solid;
		border-radius: 4px;
		pointer-events: none;
	}
</style>
