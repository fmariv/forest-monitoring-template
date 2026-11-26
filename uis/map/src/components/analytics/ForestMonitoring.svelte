<script>
	import Sprout from 'svelte-material-icons/Sprout.svelte';
	import TrendingUp from 'svelte-material-icons/TrendingUp.svelte';
	import Pie from '$components/viz/Pie.svelte';
	import ImageLayer from '$components/map/ImageLayer.svelte';
	import { analyticsStore, currentAnalytic } from '$stores/analytics.js';
	import {
		GROWTH_COLORS,
		HEALTH_PIE_COLORS,
		CHART,
		OVERLAY_OPACITY
	} from '$lib/colors.js';

	export let title;
	export let analytics;
	export let date;
	export let xyz_url;
	export let xyz_query = '';
	export let api_url;
	export let left;

	$: title = $currentAnalytic;
	$: image = 'vegetation_masked_';
	$: bands = [1];
	$: stretch = [0, 1];
	$: palette = 'RdYlGn';

	let selectedButton = 'growth';
	let selected = true;

	const haFormatter = (v) => Number.parseInt(v).toLocaleString('en-US') + ' Ha';
	const totalFormatter = (w) => {
		const total = w.globals.seriesTotals.reduce((a, b) => a + b, 0);
		return parseInt(total).toLocaleString('en-US') + ' Ha';
	};

	const sharedDonutOptions = {
		dataLabels: {
			enabled: false
		},
		plotOptions: {
			pie: {
				customScale: 0.92,
				donut: {
					size: '62%',
					labels: {
						show: true,
						name: {
							show: true,
							fontSize: '13px',
							fontWeight: 600,
							color: CHART.totalLabel,
							offsetY: -4
						},
						value: {
							show: true,
							fontSize: '22px',
							fontWeight: 700,
							color: CHART.totalValue,
							offsetY: 4,
							formatter: haFormatter
						},
						total: {
							show: true,
							label: 'Total',
							fontSize: '13px',
							fontWeight: 600,
							color: CHART.totalLabel,
							formatter: totalFormatter
						}
					}
				}
			}
		},
		legend: {
			position: 'bottom',
			fontSize: '11px',
			fontWeight: 500,
			itemMargin: {
				horizontal: 8,
				vertical: 2
			}
		}
	};

	let options = {};
	$: if (analytics && date && title === 'Vegetation Growth') {
		options = {
			...sharedDonutOptions,
			series: [analytics['Vegetation Ha'][date], analytics['Not Vegetation Ha'][date]],
			labels: ['Vegetation Ha', 'Not Vegetation Ha'],
			tooltip: {
				y: {
					formatter: function (value) {
						return parseInt(value).toLocaleString('en-US') + ' Ha';
					}
				}
			},
			colors: GROWTH_COLORS
		};
	} else if (analytics && date && title === 'Vegetation Health') {
		options = {
			...sharedDonutOptions,
			series: [
				analytics['Bare Ground'][date],
				analytics['Healthy Vegetation'][date],
				analytics['Sparse or Unhealthy Vegetation'][date],
				analytics['Very Healthy Vegetation'][date]
			],
			labels: ['Bare ground', 'Healthy', 'Sparse / Unhealthy', 'Very Healthy'],
			tooltip: {
				y: {
					formatter: function (value) {
						return parseInt(value).toLocaleString('en-US') + ' Ha';
					}
				}
			},
			colors: HEALTH_PIE_COLORS
		};
	}

	const fetchQuality = async () => {
		if (selected && $currentAnalytic === 'Vegetation Health') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/AOI_Vegetation_Quality`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('Vegetation Health');
		image = 'quality_masked_rgb_';
		bands = [1, 2, 3];
		stretch = [0, 255];
		palette = 'RdYlGn';
		selectedButton = 'quality';
	};

	const fetchGrowth = async () => {
		if (selected && $currentAnalytic === 'Vegetation Growth') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/AOI_Vegetation_Growth`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('Vegetation Growth');
		image = 'vegetation_masked_';
		bands = [1];
		stretch = [0, 1];
		palette = 'RdYlGn';
		selectedButton = 'growth';
	};
</script>

<button
	data-tip="Vegetation Growth"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'growth' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fetchGrowth}
>
	<TrendingUp size="100%" />
</button>

<button
	data-tip="Vegetation Health"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'quality' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fetchQuality}
>
	<Sprout size="100%" />
</button>

	{#if selected && options?.series}
	<h3>{title}</h3>
	<div class="donut-wrap">
		{#key title}
			<Pie {options} height={280} />
		{/key}
	</div>
{/if}

{#if selected && left && date}
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={image + left + '.tif'}
		query={xyz_query}
		options={{
			maxZoom: 20,
			pane: 'left',
			opacity: OVERLAY_OPACITY
		}}
		{bands}
		{stretch}
		{palette}
	/>
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={image + date + '.tif'}
		query={xyz_query}
		options={{
			maxZoom: 20,
			pane: 'right',
			opacity: OVERLAY_OPACITY
		}}
		{bands}
		{stretch}
		{palette}
	/>
{/if}

<style>
	.donut-wrap {
		width: 100%;
		min-height: 280px;
	}

	h3 {
		margin: 8px 0 0;
		font-size: 15px;
		font-weight: 600;
		color: var(--text, #172033);
	}
</style>
