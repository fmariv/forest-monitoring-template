<script>
  import VegetationQuality from "$components/analytics/VegetationQuality.svelte";
  import GeoJSONLayer from "$components/map/GeoJSONLayer.svelte";
  import Forest from "svelte-material-icons/Forest.svelte";
  import MockButton from "./analytics/MockButton.svelte";
  import MockQuality from "./analytics/MockQuality.svelte";
  import VegetationButton from "./analytics/VegetationButton.svelte";

  export let analytics;
  export let aoi;
  export let date;
  export let xyz_url;
  export let left;
  export let selected = false;

  export let selectedAnalysis;

  const toggleAOI = () => {
    selected = !selected;
  };
</script>

<div>
  <h1>Asset</h1>
  <button
    class={`w-10 h-10 p-1 hover:bg-gray-100 'text-gray-800'} tooltip tooltip-bottom ${
      selected ? "text-green-600" : "text-gray-800"
    }`}
    on:click={toggleAOI}
    data-tip="AoI"
  >
    <Forest size="100%" />
  </button>
  <h1>Monitoring of</h1>
  <VegetationButton bind:selectedAnalysis name="Vegetation Quality" />
  <MockButton bind:selectedAnalysis name="Mock Quality" />

  <VegetationQuality
    {analytics}
    {date}
    {xyz_url}
    {left}
    {selectedAnalysis}
    name="Vegetation Quality"
  />

  <MockQuality
    {analytics}
    {date}
    {xyz_url}
    {left}
    {selectedAnalysis}
    name="Mock Quality"
  />
</div>

{#if selected}
  <GeoJSONLayer
    name={"aoi"}
    options={{
      style: { fillOpacity: 0, weight: 3, color: "blue", dashArray: "" },
      pane: "aoi",
      zIndex: 0,
    }}
    geojson={aoi}
  />
{/if}
