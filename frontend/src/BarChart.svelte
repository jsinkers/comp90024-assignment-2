<script>
	// based on https://svelte.dev/examples/bar-chart
	import { scaleLinear } from 'd3-scale';
	// title to display on the chart
	export let title;
	// data variable of interest
	export let variable;

	const points = [
		{ issue: "health", count: 200, compound: -0.1},
		{ issue: "economy", count: 250, compound: 0.2},
		{ issue: "childcare",count: 123, compound: 0.3},
		{ issue: "housing", count: 54, compound: 0.2},
		{ issue: "tax cuts", count: 25, compound: -.3},
		{ issue: "aged care", count: 76, compound: -0.5}
	];

	// GET /api/analytics/socioeconomic/{election_issue}/summary
	//const xTicks = ["health", "economy", "childcare", "housing", "tax cuts", "aged care"];
	let xTicks = [];
	for (let i = 0; i < points.length; i++) {
		xTicks.push(points[i].issue)
	}
	console.log(xTicks);
	let yTicks;
	let ys = [];
	if (variable === 'compound') {
		yTicks = [-1, -0.5, 0, 0.5, 1];
		for (let i = 0; i < points.length; i++) {
			ys.push(points[i].compound)
		}
	} else if (variable === 'count') {
		yTicks = [0, 100, 200, 300, 400];
		for (let i = 0; i < points.length; i++) {
			ys.push(points[i].count)
		}
	}
	console.log(yTicks);
	console.log(Math.min.apply(null, yTicks));

	const padding = { top: 20, right: 15, bottom: 20, left: 25 };

	let width = 500;
	let height = 200;

	function formatMobile(tick) {
		return "'" + tick.toString().slice(-2);
	}

	$: xScale = scaleLinear()
			.domain([0, xTicks.length])
			.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
			.domain([Math.min.apply(null, yTicks), Math.max.apply(null, yTicks)])
			.range([height - padding.bottom, padding.top]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / xTicks.length - 10;

	console.log(width);
</script>

<h2>{title}</h2>

<!--<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>-->
<div class="chart" bind:clientHeight={height}>
	<svg>
		<!-- y axis -->
		<g class="axis y-axis">
			{#each yTicks as tick}
				<g class="tick tick-{tick}" transform="translate(0, {yScale(tick)})">
					<line x2="100%"></line>
					<text y="-4">{tick}</text>
				</g>
			{/each}
		</g>

		<!-- x axis -->
		<g class="axis x-axis">
			{#each points as point, i}
				<g class="tick" transform="translate({xScale(i)},{height})">
					<text x="{barWidth/2}" y="-4">{point.issue}</text>
				</g>
			{/each}
		</g>

		<g class='bars'>
			{#each ys as point, i}
				<rect
						x="{xScale(i) + 2}"
						y="{Math.min(yScale(point), yScale(0))}"
						height="{Math.abs(yScale(0)-yScale(point))}"
						width="{barWidth}"
				></rect>
			{/each}
		</g>
	</svg>
</div>

<style>
	h2 {
		text-align: center;
	}

	.chart {
		width: 100%;
		max-width: 500px;
		margin: 0 auto;
	}

	svg {
		position: relative;
		width: 100%;
		height: 200px;
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
</style>
