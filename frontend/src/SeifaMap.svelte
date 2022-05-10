<script>
	import { writable } from 'svelte/store';
	import { onDestroy, setContext } from 'svelte';
	import {mapbox, key} from './mapbox.js';
	import Modal, {bind} from 'svelte-simple-modal';
	import SeifaPopup from './InfoSeifaMap.svelte';

	setContext(key, {
		getMap: () => map,
	});

	export let lat;
	export let lon;
	export let zoom;

	let container;
	let map;
	let popupTweet;
	let popupSentiment;
	let popupElectionIssue;

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

		let choropleth_colors_expression = [ 'interpolate', ['linear'], ['get', 'irsad_score']];
		for (let i = 0; i < choropleth_layers.length; i++) {
			choropleth_colors_expression.push(choropleth_layers[i]);
			choropleth_colors_expression.push(choropleth_colors[i]);
		}

		const sentiment_layers = ['Climate', 'Childcare', 'Housing', 'Taxation', 'Aged care', 'Health', 'Economy', 'Refugees'];
		// https://colorswall.com/palette/1751/
		const sentiment_colors = [ // "#03a8a0",
			 "#039c4b",
			"#66d313",
			"#fedf17",
			"#ff0984",
			"#21409a",
			"#04adff",
			// "#e48873",
			"#f16623",
			"#f44546"
		];
		// compile a color expression to color markers on the map
		let marker_colors_expression = ['match', ['get', 'issue']];
		for (let i = 0; i < sentiment_layers.length; i++) {
			marker_colors_expression.push(sentiment_layers[i]);
			marker_colors_expression.push(sentiment_colors[i]);
		}
		// add a default colour
		marker_colors_expression.push("#FFFFFF")

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
                'data':'http://melbourneliveability.live/api/analytics/socioeconomic/seifa/'
            });
            map.addLayer({
                'id':'sa2-fill',
                'type':'fill',
                'source':'sa2',
                'layout':{},
                'paint':{
					'fill-color': choropleth_colors_expression,
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
				'data': 'http://melbourneliveability.live/api/analytics/socioeconomic/tweets/'
			});
			map.addLayer({
				'id': 'tweets-points',
				'type': 'circle',
				'source': 'tweets',
				'paint': {
					'circle-radius': 5,
					'circle-color': marker_colors_expression,
					'circle-opacity': ['max', 0.5, ['abs', ['get', 'compound']]]
				}
			});
        }, 2000);

		// Create a popup, but don't add it to the map yet.
		const popup = new mapbox.Popup({
			closeButton: false,
			closeOnClick: false
		});

		// add popups on tweet markers
		map.on('mouseenter', 'tweets-points', (e) => {
			map.getCanvas().style.cursor = 'pointer';
			const coordinates = e.features[0].geometry.coordinates.slice();
			popupSentiment = e.features[0].properties.compound;
			popupTweet = e.features[0].properties.text;
			popupElectionIssue = e.features[0].properties.issue;
			let description = `<p><b>Tweet:</b> ${popupTweet}</p>`;
			description += `<p><b>Election issue:</b> ${popupElectionIssue}</p>`;
			description += `<p><b>Sentiment:</b> ${popupSentiment}</p>`;

			while(Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
				coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
			}

			popup.setLngLat(coordinates)
					.setHTML(description)
					.addTo(map);
		});

		map.on('mouseleave', 'tweets-points', (e) => {
			map.getCanvas().style.cursor = '';
			popup.remove();
		});

		// Add info for SA2: prop to legend
		map.on('mousemove', (event) => {
			if (map.loaded) {
				const sa2 = map.queryRenderedFeatures(event.point, {
					layers: ['sa2-fill']
				});
				document.getElementById('pd').innerHTML = sa2.length
						? `<p>${sa2[0].properties.name}</p><p>IRSAD: ${sa2[0].properties.irsad_score}</p>`
						: "";
			}
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

	const modal = writable(null);
	const showModal = () => modal.set(bind(SeifaPopup, {}));
</script>

<svelte:head>
	<link
			rel="stylesheet"
			href="https://unpkg.com/mapbox-gl/dist/mapbox-gl.css"
			on:load={load}
	/>
</svelte:head>

<div id="map" bind:this={container}>
	{#if map}
		<slot />
	{/if}
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
		<div id='features'><h2>SA2 SEIFA</h2><div id='pd'></div></div>
	</div>

</div>
<div class="map-overlay inset-0" id="info">
	<Modal show={$modal}>
		<span class="fa-solid fa-info-circle icon" on:click={showModal}></span>
	</Modal>
</div>

<style>
	.icon {
		font-size: 1.5em;
		padding: 1rem;
		@apply relative flex items-center justify-center mx-auto
		rounded-full hover:bg-blue-600 hover:text-white transition-all duration-200 ease-linear cursor-pointer;
	}

	#map {
		@apply h-full w-full absolute right-0 top-0 z-10;
	}

	/**
	* Set rules for how the map overlays
	* (information box and legend) will be displayed
	* on the page. */
	.map-overlay {
		position: absolute;
		top: 0;
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
		@apply z-20;
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

	#info {
		@apply z-20 bg-transparent inset-0 left-4 top-4;
		position: absolute;
		width: fit-content;
		height: fit-content;
	}
</style>
