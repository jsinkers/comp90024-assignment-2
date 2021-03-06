<!-- based on https://svelte.dev/examples/scatterplot-->
<script>
    import { onMount } from 'svelte';
    import { scaleLinear } from 'd3-scale';
    import { pointer, json } from 'd3';
    import { regressionLinear } from 'd3-regression';
    import {fade} from 'svelte/transition';

    import { writable } from 'svelte/store';
    import Modal, {bind} from 'svelte-simple-modal';
    import Popup from './InfoDiversityChart.svelte';

    const modal = writable(null);
    const showModal = () => modal.set(bind(Popup, {}));

    let data_url = 'http://melbourneliveability.live/api/analytics/diversity/sentiment/'

    let points = [];
    let svg;
    let margin = {top: 20, right: 30, bottom: 30, left: 60};
    let width = 600;
    let height = 350;

    const padding = { top: 20, right: 40, bottom: 40, left: 25 };

    $: xScale = scaleLinear()
        .domain([0, 1])
        .range([padding.left, width-padding.right]);

    $: yScale = scaleLinear()
        .domain([-1, 1])
        .range([height-padding.bottom, padding.top]);

    $: xTicks = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1]
    $: yTicks = [-1, -0.5, 0, 0.5, 1]

    let tooltip;
    let opacity;
    let tooltip_left;
    let tooltip_top;
    let mouse_x;
    let mouse_y;
    let selected_point = undefined;
    let regression;

    const setMousePosition = function(event) {
        mouse_x = event.clientX;
        mouse_y = event.clientY;
    }

    let mousemove = function(d) {
        tooltip_left = (mouse_x + 20) + "px";
        tooltip_top = (mouse_y - 20) + "px";
    }

    onMount(() => {
        ({ width, height } = svg.getBoundingClientRect());
        console.log(width);
        console.log(height);
        resize();
    });

    function resize() {
        ({ width, height } = svg.getBoundingClientRect());
    }

    async function fetchData() {
        await json(data_url).then((dataset) => {
            dataset = dataset.returned_data;
            for (let i = 0; i < dataset.mean_compound.length; i++) {
                let point = {'compound': dataset.mean_compound[i],
                    'prop_spk_other_lang': dataset.prop_spk_other_lang[i],
                    'count': dataset.count[i],
                    'sa2': dataset.sa2[i]}
                points.push(point);

            }
            console.log(dataset);
            regression = regressionLinear()
                .x(d => d.prop_spk_other_lang)
                .y(d => d.compound)
                .domain([0, 1]);


        });
        return {'points': points, 'regression': regression(points)};
    }
</script>

<svelte:window on:resize='{resize}'/>
<div class="scatter-container" bind:clientWidth={width}>
    <div class="flex-item">
        <h1>Tweet sentiment vs diversity</h1>
    </div>
    <div class="chart flex-item" >
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
            {:then data}
                {#each data.points as point}
                    {#if point.prop_spk_other_lang != null}
                    <circle cx='{xScale(point.prop_spk_other_lang)}' cy='{yScale(point.compound)}' r='3'
                            on:mousemove={mousemove}
                            on:mouseover={(event) => {selected_point = point; setMousePosition(event)}}
                            on:mouseout={() => {selected_point = undefined}}/>
                    {/if}
                {/each}
                <g id="fit-line">
                    <line x1='{xScale(data.regression[0][0])}'
                          x2='{xScale(data.regression[1][0])}'
                          y1='{yScale(data.regression[0][1])}'
                          y2='{yScale(data.regression[1][1])}'/>
                </g>
                <text class="y-label">

                </text>



            {:catch error}
                <p>{error.message}</p>
            {/await}await
        </svg>
        {#if selected_point != undefined}
            <div transition:fade class="tooltip" bind:this={tooltip} opacity={opacity} style="left: {tooltip_left}; top: {tooltip_top}">
                <p>Diversity measure: {Math.round(selected_point.prop_spk_other_lang*1000)/10}%</p>
                <p>Mean sentiment: {Math.round(selected_point.compound*100)/100}</p>
<!--                <p>Tweet count: {selected_point.count}</p>-->
<!--                <p>SA2: {selected_point.sa2}</p>-->
            </div>
        {/if}
    </div>
    <div class="flex-item">
        <p>Diversity measure: Proportion of people who speak a language other than English at home (Census 2016)</p>
    </div>
</div>

<div id="info">
    <Modal show={$modal}>
        <span class="fa-solid fa-info-circle icon" on:click={showModal}></span>
    </Modal>
</div>

<style>
    .scatter-container {
        @apply h-full w-10/12;
        display: flex;
        flex-direction: column;
        flex-wrap: nowrap;
        justify-content: center;
        align-content: center;

    }
    .chart {
        justify-content: center;
    }

    svg {
        margin: 0 auto;
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

    h1 {
        @apply text-xl
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

    .tooltip {
        position: fixed;
        text-align: center;
        padding: 10px;
        background: white;
        font-size: small;
        border: 1px solid;
        border-radius: 4px;
        pointer-events: none;
    }
</style>
