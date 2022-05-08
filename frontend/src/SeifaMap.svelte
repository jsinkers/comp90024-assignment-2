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
		const choropleth_layers = [
			700,
			750,
			800,
			850,
			900,
			950,
			1000,
			1050,
			1100
		];
		const choropleth_colors = [
			'#F2F12D',
			'#EED322',
			'#E6B71E',
			'#DA9C20',
			'#CA8323',
			'#B86B25',
			'#A25626',
			'#8B4225',
			'#723122'
		];
		const sentiment_layers = ['childcare', 'housing', 'taxes', 'aged care', 'health', 'economy'];
		const sentiment_colors = ["#F8766D", "#F5EB67", "#00BA38", "#619CFF", "#012840", "#FFA15C" ];
		// compile a color expression to color markers on the map
		let color_expression = ['match', ['get', 'election_issue']];
		for (let i = 0; i < sentiment_layers.length; i++) {
			console.log(color_expression);
			color_expression.push(sentiment_layers[i]);
			color_expression.push(sentiment_colors[i]);
		}
		// add a default colour
		color_expression.push("#FFFFFF")
		console.log(color_expression);

		map = new mapbox.Map({
			container,
			style: 'mapbox://styles/mapbox/streets-v11',
			center: [lon, lat],
			zoom,
		});

        setTimeout(() => {
            map.addSource('sa2', {
                'type':'geojson',
				// TODO: replace with API URL
                'data':'/sa2-seifa-lang-small.geojson'
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
                    'fill-opacity':0.7
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
			// Add the image to the map style.
			map.addSource('tweets', {
				'type': 'geojson',
				// TODO: replace with API URL
				'data': '/twitter-melb-filtered-issues.geojson'
			});
			map.addLayer({
				'id': 'tweets-points',
				'type': 'circle',
				'source': 'tweets',
				'paint': {
					'circle-radius': 5,
					'circle-color': color_expression,
					'circle-opacity': ['max', 0.5, ['abs', ['get', 'compound']]]
				}
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
		// create legend
		const legend_choropleth = document.getElementById('legend-choropleth');
		choropleth_layers.forEach((layer, i) => {
			const color = choropleth_colors[i];
			const item = document.createElement('div');
			const key = document.createElement('span');
			key.className = 'legend-key';
			key.style.backgroundColor = color;

			const value = document.createElement('span');
			value.innerHTML = `${layer}`;
			item.appendChild(key);
			item.appendChild(value);
			legend_choropleth.appendChild(item);
		});
		const legend_marker = document.getElementById('legend-marker');
		sentiment_layers.forEach((layer, i) => {
			const color = sentiment_colors[i];
			const item = document.createElement('div');
			const key = document.createElement('span');
			key.className = 'legend-key';
			key.style.backgroundColor = color;

			const value = document.createElement('span');
			value.innerHTML = `${layer}`;
			item.appendChild(key);
			item.appendChild(value);
			legend_marker.appendChild(item);
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
	<!--<div class='map-overlay' id='description'><h2>Diversity</h2><div id='pd'><p>Hover over a state!</p></div></div>-->
	<div class="map-overlay" id="legend">
		<style>
			.legend-key {
				display: inline-block;
				border-radius: 20%;
				width: 20px;
				height: 10px;
				margin-right: 5px;
			}
		</style>
		<div id='legend-choropleth'>
			<h2>SEIFA - IRSAD Score</h2>
		</div>
		<div id='legend-marker'>
			<h2>Election Issue</h2>
		</div>
	</div>
</div>

<style>

	div {
		@apply h-full w-11/12 absolute right-0 top-0 z-10;
	}


	/**
	* Set rules for how the map overlays
	* (information box and legend) will be displayed
	* on the page. */
	.map-overlay {
		position: absolute;
		bottom: 0;
		right: 0;
		background: #fff;
		margin-right: 20px;
		font-family: Arial, sans-serif;
		overflow: auto;
		border-radius: 3px;
	}

	#legend {
		padding: 10px;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
		line-height: 18px;
		height: min-content;
		margin-bottom: 40px;
		width: 120px;
	}
	#legend-choropleth {
		position: relative;
		height: min-content;
	}
	#legend-marker {
		position: relative;
		height: min-content;
	}

	h2 {
		font-weight: bold;
	}

</style>
