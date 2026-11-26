<script>
	import Chart from "./Chart.svelte";

	export let options;
	export let height;
	export let loading = false;

	const base_options = {
		chart: {
			height,
			type: "area",
			toolbar: { show: false },
			fontFamily: "Lato, system-ui, sans-serif",
		},
		series: [],
		dataLabels: {
			enabled: false,
		},
		stroke: {
			curve: "smooth",
			width: 2.5,
		},
		yaxis: {
			labels: {
				formatter: function (value) {
					return value + "%";
				},
				style: {
					colors: "#64748B",
					fontSize: "11px",
				},
			},
		},
		xaxis: {
			labels: {
				style: {
					colors: "#64748B",
					fontSize: "11px",
				},
			},
		},
		grid: {
			borderColor: "#E2E8F0",
			strokeDashArray: 3,
		},
		fill: {
			type: "gradient",
			gradient: {
				shadeIntensity: 1,
				opacityFrom: 0.35,
				opacityTo: 0.08,
				stops: [0, 90, 100],
			},
		},
		legend: {
			show: true,
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
		},
		tooltip: {
			y: {
				formatter: function (value) {
					return value?.toFixed(2) + "%";
				},
			},
		},
		noData: {
			text: loading ? "Loading..." : "No data",
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
		combined_options = {
			...combined_options,
			chart: {
				...combined_options.chart,
				height,
				toolbar: { show: false },
			},
			noData: {
				...combined_options.noData,
				text: loading ? "Loading..." : "No data",
			},
		};
	}
</script>

<Chart options={combined_options} />
