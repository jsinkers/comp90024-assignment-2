<script>
	import { onDestroy, setContext } from 'svelte';
	import {mapbox, key} from './mapbox.js';

	setContext(key, {
		getMap: () => map,
	});

	export let lat;
	export let lon;
	export let zoom;

	let container;
	let map;

	function load() {
		map = new mapbox.Map({
			container,
			style: 'mapbox://styles/mapbox/streets-v11',
			center: [lon, lat],
			zoom,
		});

        setTimeout(() => {
            map.addSource('sa2', {
                'type':'geojson',
                'data':'SA3_2021_AUST_SHP_GDA2020-greater-melb.geojson'
            });
            map.addLayer({
                'id':'sa2-fill',
                'type':'fill',
                'source':'sa2',
                'layout':{},
                'paint':{
					'fill-color': [
						'interpolate',
						['linear'],
						['get', 'irsad_score'],
						700,
						'#F2F12D',
						750,
						'#EED322',
						800,
						'#E6B71E',
						850,
						'#DA9C20',
						900,
						'#CA8323',
						950,
						'#B86B25',
						1000,
						'#A25626',
						1050,
						'#8B4225',
						1100,
						'#723122'
					],
                    //'fill-color':'#0080ff', //blue color fill
                    'fill-opacity':0.6
                },
                'filter': ['==', '$type', 'Polygon']
            });
            // map.addLayer({
            //     'id': 'sa2-outline',
            //     'type': 'line',
            //     'source': 'sa2',
            //     'layout': {},
            //     'paint': {
            //         'line-color': '#000',
            //         'line-width': 1
            //     },
            //     'filter': ['==', '$type', 'Polygon']
            // });

        }, 2000);
	}

	onDestroy(() => {
		if (map) map.remove();
	});
</script>

<!-- this special element will be explained in a later section -->
<svelte:head>
	<link
		rel="stylesheet"
		href="https://unpkg.com/mapbox-gl/dist/mapbox-gl.css"
		on:load={load}
	/>
</svelte:head>

<div bind:this={container}>
	{#if map}
		<slot />
	{/if}
</div>

<style>
	div {
		@apply h-full w-11/12 absolute right-0 top-0;
	}
</style>
