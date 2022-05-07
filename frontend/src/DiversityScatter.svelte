<!-- based on https://svelte.dev/examples/scatterplot-->
<script>
    import { onMount } from 'svelte';
    import { axisLeft, axisBottom, scaleLinear } from 'd3-scale';
    import {json} from 'd3';

    let data_url = "/sa2-diversity-sentiment-fit.json";
    let dataset;
    //let data_url = 'http://172.26.134.62/api/analytics/diversity/sentiment/diversity/'

    let points = [];

    let svg;
    let margin = {top: 10, right: 30, bottom: 30, left: 60};
    let width = 460 - margin.left - margin.right;
    let height = 400 - margin.top - margin.bottom;

    const padding = { top: 20, right: 40, bottom: 40, left: 25 };

    var xScale = scaleLinear()
        .domain([0, 1])
        .range([0, width]);

    var yScale = scaleLinear()
        .domain([-1, 1])
        .range([height, 0]);

    $: xTicks = width > 180 ?
        [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.100] : [0, 0.5, 1];

    $: yTicks = height > 180 ?
        [-1, -0.5, 0, 0.5, 1] :
        [-1, 0, 1];

    onMount(() => {
        console.log(dataset);
        resize();
        console.log(svg);

        // Add X axis
        let x = scaleLinear()
            .domain([0, 1])
            .range([ 0, width ]);
        svg.append("g")
            //.attr("transform", "translate(-1," + height + ")")
            .call(axisBottom(x));

        // Add Y axis
        let y = scaleLinear()
            .domain([-1, 1])
            .range([ height, 0]);
        svg.append("g")
            .call(axisLeft(y));
    });

    function resize() {
        ({ width, height } = svg.getBoundingClientRect());
    }

    async function fetchData() {
        await json(data_url).then((dataset) => {
            //     console.log(dataset)
            //     svg.append("g")
            //         .selectAll("dot")
            //         .data(dataset)
            //         .enter()
            //         .append("circle")
            //             .attr("cx", function (d) {return x(d.prop_spk_other_lang);})
            //             .attr("cy", function (d) {return y(d.sentiment);})
            //             .attr("r", 1.5)
            for (let i = 0; i < dataset.compound.length; i++) {
                let point = {'compound': dataset.compound[i], 'prop_spk_other_lang': dataset.prop_spk_other_lang[i]}
                points.push(point);
            }
            console.log(points);
        });
        return points;
    }
</script>

<svelte:window on:resize='{resize}'/>

<svg bind:this={svg}>
    <!-- y axis -->
<!--
    <g class='axis y-axis'>
        {#each yTicks as tick}
            <g class='tick tick-{tick}' transform='translate(0, {yScale(tick)})'>
                <line x1='{padding.left}' x2='{xScale(22)}'/>
                <text x='{padding.left - 8}' y='+4'>{tick}</text>
            </g>
        {/each}
    </g>
-->

    <!-- x axis -->
<!--
    <g class='axis x-axis'>
        {#each xTicks as tick}
            <g class='tick' transform='translate({xScale(tick)},0)'>
                <line y1='{yScale(0)}' y2='{yScale(13)}'/>
                <text y='{height - padding.bottom + 16}'>{tick}</text>
            </g>
        {/each}
    </g>
-->

    <!-- data -->
    {#await fetchData()}
        <p>loading></p>
    {:then points}
        {#each points as point}
            <circle cx='{xScale(point.prop_spk_other_lang)}' cy='{yScale(point.compound)}' r='5'/>
        {/each}
    {:catch error}
        <p>{error.message}</p>
    {/await}await

</svg>

<style>
    div {
        /*@apply h-full w-11/12 absolute right-0 top-0 z-10;*/
        width: 100%;
        height: 100%;
    }

    svg {
        width: 100%;
        height: 100%;
        /*float: left;*/
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
</style>
