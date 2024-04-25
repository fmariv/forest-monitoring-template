<script>
  import ImageLayer from "$components/map/ImageLayer.svelte";
  import Pie from "$components/viz/Pie.svelte";
  import { selectedAnalysis } from "$stores/map/selectedAnalysis";

  export let name;
  export let analytics;
  export let date;
  export let xyz_url;
  export let left;

  $: console.log(JSON.stringify(analytics));

  let options = {};
  $: if (analytics && date) {
    const categories = Object.keys(analytics).filter((key) => key !== "Total");
    const series = categories.map((category) => analytics[category][date]);
    const labels = categories;

    // Example of cycling through a predefined set of colors
    const baseColors = ["#25dd47", "#ff0000", "#0000ff", "#ffa500"]; // Extend this array as needed
    const colors = categories.map(
      (_, index) => baseColors[index % baseColors.length]
    );

    options = {
      series,
      labels,
      colors,
      chart: {
        type: "pie",
      },
      tooltip: {
        y: {
          formatter: function (value) {
            return parseInt(value).toLocaleString("en-US") + " Has";
          },
        },
      },
      plotOptions: {
        pie: {
          donut: {
            labels: {
              show: true,
              value: {
                formatter: function (v) {
                  return Number.parseInt(v).toLocaleString("en-US") + "Has";
                },
              },
              total: {
                show: true,
                label: "Total",
                color: "#373d3f",
                formatter: function (w) {
                  const total = w.globals.seriesTotals.reduce(
                    (a, b) => a + b,
                    0
                  );
                  return parseInt(total).toLocaleString("en-US") + "Has";
                },
              },
            },
          },
        },
      },
      legend: {
        position: "bottom",
      },
    };
  }

  $: selected = $selectedAnalysis === name;
  $: if ($selectedAnalysis) selected = $selectedAnalysis === name;
</script>

{#if selected}
  <h3>{name}</h3>
  <Pie {options} height={300} />
{/if}

{#if selected}
  <ImageLayer
    XYZ_URL={xyz_url}
    name="vegetation"
    image={"vegetation_masked_" + left + ".tif"}
    options={{
      maxZoom: 20,
      pane: "left",
    }}
    bands={[1]}
    stretch={[0, 1]}
    palette="RdYlGn"
  />
  <ImageLayer
    XYZ_URL={xyz_url}
    name="vegetation"
    image={"vegetation_masked_" + date + ".tif"}
    options={{
      maxZoom: 20,
      pane: "right",
    }}
    bands={[1]}
    stretch={[0, 1]}
    palette="RdYlGn"
  />
{/if}
