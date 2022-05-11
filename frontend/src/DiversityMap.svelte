<script>
	import { writable } from 'svelte/store';
	import { onDestroy, setContext } from 'svelte';
	import {mapbox, key} from './mapbox.js';
	import Modal, {bind} from 'svelte-simple-modal';
	import DiversityPopup from './InfoDiversityMap.svelte';
	import {DoubleBounce} from 'svelte-loading-spinners';

	setContext(key, {
		getMap: () => map,
	});

	export let lat;
	export let lon;
	export let zoom;

	let container;
	let map;
	let spinner = true;

	const modal = writable(null);
	const showModal = () => modal.set(bind(DiversityPopup, {}));

	function load() {
		const choropleth_layers = [
			"0-10%",
			"10-20%",
			"20-30%",
			"30-40%",
			"40-50%",
			"50-60%",
			"60-70%",
			"70-80%",
			">80%",
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
		const sentiment_layers = ["Negative", "Neutral", "Positive"];
		const sentiment_colors = ["#FF0040", "#000040", "#00FF40"]
		map = new mapbox.Map({
			container,
			style: 'mapbox://styles/mapbox/streets-v11',
			center: [lon, lat],
			zoom,
		});

		map.on('idle', () => {
			// once the sa2 layer is loaded, hide the spinner
			if (map.getSource('sa2') && map.isSourceLoaded('sa2')) {
				spinner = false;
			}
		});

		map.on('load', () => {
			map.addSource('sa2', {
				'type': 'geojson',
				'data': 'http://melbourneliveability.live/api/analytics/diversity/language/'
			});
			map.addLayer({
				'id': 'sa2-fill',
				'type': 'fill',
				'source': 'sa2',
				'layout': {},
				'paint': {
					'fill-color': [
						'interpolate',
						['linear'],
						['get', 'prop'],
						0,
						'#F2F12D',
						0.1,
						'#EED322',
						0.2,
						'#E6B71E',
						0.3,
						'#DA9C20',
						0.4,
						'#CA8323',
						0.5,
						'#B86B25',
						0.6,
						'#A25626',
						0.7,
						'#8B4225',
						0.8,
						'#723122'
					],
					'fill-opacity': 0.7
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
				'data': 'http://melbourneliveability.live/api/analytics/diversity/tweets/'
			});
			map.addLayer({
				'id': 'tweets-points',
				'type': 'circle',
				'source': 'tweets',
				'paint': {
					'circle-radius': 5,
					'circle-color': ["rgb",
						// red: if compound < 0 then red is 0
						['*', 255, ['max', 0, ['get', 'compound']]],
						// green: if compound > 0 then green is 0
						['*', -255, ['min', 0, ['get', 'compound']]],
						// blue:
						40
					],
					'circle-opacity': ['max', 0.5, ['abs', ['get', 'compound']]]
				}
			});
		});

		// Create a popup, but don't add it to the map yet.
		const popup = new mapbox.Popup({
			closeButton: false,
			closeOnClick: false
		});
		// add popups on tweet markers
		map.on('mouseenter', 'tweets-points', (e) => {
			map.getCanvas().style.cursor = 'pointer';
			const coordinates = e.features[0].geometry.coordinates.slice();
			const popupSentiment = e.features[0].properties.compound;
			const popupTweet = e.features[0].properties.text;
			let description = `<p><b>Tweet:</b> ${popupTweet}</p>`;
			description += `<p><b>Sentiment:</b> ${popupSentiment}</p>`;

			while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
				coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
			}

			popup.setLngLat(coordinates)
					.setHTML(description)
					.addTo(map);
		});

		map.on('mouseleave', 'tweets-points', () => {
			map.getCanvas().style.cursor = '';
			popup.remove();
		});
		// Add info for SA2: prop to legend
		map.on('mousemove', (event) => {
			if (!spinner) {
				const sa2 = map.queryRenderedFeatures(event.point, {
					layers: ['sa2-fill']
				});
				document.getElementById('pd').innerHTML = sa2.length
						? `<p>${sa2[0].properties.name}</p><p>${Math.round(sa2[0].properties.prop * 1000) / 10}%</p>`
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
		const legend_sentiment = document.getElementById('legend-sentiment');
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
			legend_sentiment.appendChild(item);
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

<div id="map" bind:this={container}>
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
			<h2>Diversity</h2>
		</div>
		<div id='legend-sentiment'>
			<h2>Sentiment</h2>
		</div>
		<div id='features'><h2>SA2 Diversity</h2><div id='pd'></div></div>
	</div>
</div>
{#if spinner}
	<div id="spinner" class="map-overlay z-50">
		<DoubleBounce color="#4caf50"></DoubleBounce>
	</div>
{/if}
<div class="map-overlay " id="info">
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
	#legend-sentiment {
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

	#spinner {
		@apply z-50 bg-transparent;
		position: absolute;
		top: 50%;
		left: 50%;
	}
</style>
