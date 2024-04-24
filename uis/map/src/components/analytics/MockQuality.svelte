<script>
  import ImageLayer from "$components/map/ImageLayer.svelte";
  import Pie from "$components/viz/Pie.svelte";

  export let name;
  export let analytics;
  export let date;
  export let xyz_url;
  export let left;
  export let selectedAnalysis;

  let options = {};
  $: if (analytics && date) {
    console.log(analytics);
    options = {
      series: [
        analytics["Vegetation Ha"][date],
        analytics["Not Vegetation Ha"][date],
      ],
      labels: ["Vegetation Ha", "Not Vegetation Ha"],
      tooltip: {
        y: {
          formatter: function (value) {
            return parseInt(value).toLocaleString("en-US") + " Has";
          },
        },
      },
      dataLabels: {
        formatter: function (val, opts) {
          return parseInt(0.01 * val * analytics.Total[date]).toLocaleString(
            "en-US"
          );
        },
      },
      colors: ["#25dd47", "#ff0000"],
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
                  const total = w.globals.seriesTotals.reduce((a, b) => {
                    return a + b;
                  }, 0);
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

  $: selected = selectedAnalysis === name;
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
