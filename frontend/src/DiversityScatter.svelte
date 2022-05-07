<!-- based on https://svelte.dev/examples/scatterplot-->
<script>
    import { onMount } from 'svelte';
    import { scaleLinear } from 'd3-scale';
    import { json } from 'd3';

    let data_url = "/sa2-diversity-sentiment-fit.json";
    //let data_url = 'http://172.26.134.62/api/analytics/diversity/sentiment/diversity/'

    let points = [];
    let svg;
    let margin = {top: 20, right: 30, bottom: 30, left: 60};
    let width = 600;
    let height= 600;

    const padding = { top: 20, right: 40, bottom: 40, left: 25 };

    $: xScale = scaleLinear()
        .domain([0, 1])
        .range([padding.left, width-padding.right]);

    $: yScale = scaleLinear()
        .domain([-1, 1])
        .range([height-padding.bottom, padding.top]);

    $: xTicks = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1]
    $: yTicks = [-1, -0.5, 0, 0.5, 1]

    onMount(() => {
        resize();
    });

    function resize() {
        ({ width, height } = svg.getBoundingClientRect());
        console.log(height);
        console.log(width);
    }

    async function fetchData() {
        await json(data_url).then((dataset) => {
            for (let i = 0; i < dataset.compound.length; i++) {
                let point = {'compound': dataset.compound[i],
                    'prop_spk_other_lang': dataset.prop_spk_other_lang[i],
                    'fit': dataset.fit[i]}
                points.push(point);
            }
            console.log(points);
        });
        return points;
    }

</script>

<svelte:window on:resize='{resize}'/>
<!--<div class="relative flex items-center justify-center flex-col h-full w-full p-2 bg-white bg-opacity-30 rounded-2xl backdrop-filter">-->
<div class="container">
    <div class="flex-item">
        <h1 class="flex-item">Tweet sentiment vs diversity</h1>
    </div>
    <div class="chart flex-item" bind:clientWidth={width}>
        <svg id="plot" bind:this={svg} {width} {height}>
            <!-- y axis -->
            <g class='axis y-axis'>
                {#each yTicks as tick}

                    <g class='tick tick-{tick}' transform='translate(0, {yScale(tick)})'>
                        <line x1='{padding.left}' x2='{xScale(1)}'/>
                        <text x='{padding.left - 8}' y='+4'>{tick}</text>
                    </g>
                {/each}
            </g>

            <!-- x axis -->
            <g class='axis x-axis'>
                {#each xTicks as tick}
                    <g class='tick' transform='translate({xScale(tick)},0)'>
                        <line y1='{yScale(-1)}' y2='{yScale(1)}'/>
                        <text y='{height - padding.bottom + 16}'>{tick}</text>
                    </g>
                {/each}
            </g>

            <!-- data -->
            {#await fetchData()}
                <p>loading></p>
            {:then points}

                {#each points as point}
                    <circle cx='{xScale(point.prop_spk_other_lang)}' cy='{yScale(point.compound)}' r='3'/>
                {/each}
                <g id="fit-line">
                    <line x1='{xScale(points[0].prop_spk_other_lang)}'
                          x2='{xScale(points[points.length-1].prop_spk_other_lang)}'
                          y1='{yScale(points[0].fit)}'
                          y2='{yScale(points[points.length-1].fit)}'/>
                </g>
                <text class="y-label">

                </text>

            {:catch error}
                <p>{error.message}</p>
            {/await}await

        </svg>
    </div>
    <div class="flex-item">
        <p>Diversity measure: Proportion of people who speak a language other than English at home (Census 2016)</p>
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

    circle {
        fill: orange;
        fill-opacity: 0.6;
        stroke: rgba(0,0,0,0.5);
    }

    .tick line {
        stroke: #ddd;
        stroke-dasharray: 2;
    }

    text {
        font-size: 12px;
        fill: #999;
    }

    .x-axis text {
        text-anchor: middle;
    }

    .y-axis text {
        text-anchor: end;
    }

    #fit-line line {
        stroke: #950d0d;
        stroke-dasharray: 0;
    }
</style>
