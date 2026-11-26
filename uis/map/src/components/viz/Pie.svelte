<script>
	import Chart from "./Chart.svelte";

	export let options;
	export let height;

	const base_options = {
		series: [],
		labels: [],
		chart: {
			type: "donut",
			height,
			toolbar: { show: false },
		},
		dataLabels: {
			enabled: false,
		},
		stroke: {
			width: 2,
			colors: ["#ffffff"],
		},
		plotOptions: {
			pie: {
				customScale: 0.92,
				donut: {
					size: "62%",
					labels: {
						show: true,
						name: {
							show: true,
							fontSize: "13px",
							fontWeight: 600,
							color: "#64748B",
							offsetY: -4,
						},
						value: {
							show: true,
							fontSize: "22px",
							fontWeight: 700,
							color: "#172033",
							offsetY: 4,
						},
						total: {
							show: true,
							label: "Total",
							fontSize: "13px",
							fontWeight: 600,
							color: "#64748B",
						},
					},
				},
			},
		},
		legend: {
			position: "bottom",
			fontSize: "12px",
			fontWeight: 500,
			labels: {
				colors: "#475569",
			},
			markers: {
				width: 10,
				height: 10,
				radius: 10,
			},
			itemMargin: {
				horizontal: 10,
				vertical: 4,
			},
		},
		noData: {
			text: "Loading...",
			align: "center",
			verticalAlign: "middle",
			offsetX: 0,
			offsetY: 0,
			style: {
				color: "#64748B",
				fontSize: "14px",
				fontFamily: "Lato, system-ui, sans-serif",
			},
		},
	};

	function deepMerge(base, override) {
		if (!override || typeof override !== "object" || Array.isArray(override)) {
			return override === undefined ? base : override;
		}
		const out = { ...base };
		for (const key of Object.keys(override)) {
			const b = base?.[key];
			const o = override[key];
			if (
				b &&
				o &&
				typeof b === "object" &&
				typeof o === "object" &&
				!Array.isArray(b) &&
				!Array.isArray(o)
			) {
				out[key] = deepMerge(b, o);
			} else {
				out[key] = o;
			}
		}
		return out;
	}

	let combined_options = { ...base_options };
	$: {
		combined_options = deepMerge(base_options, options || {});
		if (height) {
			combined_options = {
				...combined_options,
				chart: { ...combined_options.chart, height },
			};
		}
	}
</script>

<Chart options={combined_options} />
