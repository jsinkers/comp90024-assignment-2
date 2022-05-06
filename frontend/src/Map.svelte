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
                'data':'sa2-seifa-lang-small.geojson'
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
            map.addLayer({
                'id': 'sa2-outline',
                'type': 'line',
                'source': 'sa2',
                'layout': {},
                'paint': {
                    'line-color': '#000',
                    'line-width': 1
                },
                'filter': ['==', '$type', 'Polygon']
            });
			map.loadImage(
				'2021 Twitter logo - white.png',
				(error, image) => {
				if (error) throw error;
				// Add the image to the map style.
				map.addImage('tweet', image);
				map.addSource('tweets', {
					'type': 'geojson',
					'data': 'twitter-melb-filtered.geojson'
				});
				map.addLayer({
					'id': 'tweets-points',
					'type': 'symbol',
					'source': 'tweets',
					'layout': {
						'icon-image': 'tweet',
						'icon-size': 0.015,
						'icon-allow-overlap': true
					}
				});
				});
        }, 2000);

		map.on('click', 'tweets-points', (e) => {
			const coordinates = e.features[0].geometry.coordinates.slice();
			const description = e.features[0].properties.text;

			while(Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
				coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
			}

			new mapbox.Popup()
				.setLngLat(coordinates)
				.setHTML(description)
				.addTo(map);
		});

		map.on('mouseenter', 'tweets-points', () => {
			map.getCanvas().style.cursor = 'pointer';
		});
		map.on('mouseleave', 'tweets-points', () => {
			map.getCanvas().style.cursor = '';
		});
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
		@apply h-full w-11/12 absolute right-0 top-0 z-10;
	}
</style>
