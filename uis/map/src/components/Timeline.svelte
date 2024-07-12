<script>
	import { compareAsc, parseISO } from 'date-fns';
	import Lines from '$components/viz/Lines.svelte';
	import { analyticsStore, currentAnalytic } from '$stores/analytics.js';

	export let height;
	export let data;

	let analytic;

	$: data = $analyticsStore;
	$: analytic = $currentAnalytic;

	let options = {};
	$: sorted_dates = Object.keys(data.Total).sort((a, b) => compareAsc(parseISO(a), parseISO(b)));

	$: if (sorted_dates)
		if (analytic === 'Vegetation Growth') {
			options = {
				colors: ['#25dd47', '#ff0000'],
				xaxis: {
					categories: sorted_dates,
					type: 'datetime'
				},
				series: [
					{
						name: 'Vegetation Ha',
						data: sorted_dates.map((date) => (100 * data['Vegetation Ha'][date]) / data.Total[date])
					},
					{
						name: 'Not Vegetation Ha',
						data: sorted_dates.map(
							(date) => (100 * data['Not Vegetation Ha'][date]) / data.Total[date]
						)
					}
				]
			};
		} else if (analytic === 'Vegetation Quality') {
			options = {
				colors: ['#ff0000', '#90ee90', '#ffff00', '#006400'], // Rojo, Verde claro, Amarillo, Azul, Verde oscuro
				xaxis: {
					categories: sorted_dates,
					type: 'datetime'
				},
				series: [
					{
						name: 'Bare ground',
						data: sorted_dates.map((date) => ({
							x: date,
							y: data['Bare Ground'][date]
								? ((data['Bare Ground'][date] / data['Total'][date]) * 100).toFixed(2)
								: 0
						}))
					},
					{
						name: 'Healthy Vegetation',
						data: sorted_dates.map((date) => ({
							x: date,
							y: data['Healthy Vegetation'][date]
								? ((data['Healthy Vegetation'][date] / data['Total'][date]) * 100).toFixed(2)
								: 0
						}))
					},
					{
						name: 'Sparse or Unhealthy Vegetation',
						data: sorted_dates.map((date) => ({
							x: date,
							y: data['Sparse or Unhealthy Vegetation'][date]
								? (
										(data['Sparse or Unhealthy Vegetation'][date] / data['Total'][date]) *
										100
									).toFixed(2)
								: 0
						}))
					},
					{
						name: 'Very Health Vegetation',
						data: sorted_dates.map((date) => ({
							x: date,
							y: data['Very Health Vegetation'][date]
								? ((data['Very Health Vegetation'][date] / data['Total'][date]) * 100).toFixed(2)
								: 0
						}))
					}
				]
			};
		}
</script>

<Lines {options} {height} />
