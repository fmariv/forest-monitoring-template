<script>
  import { selectedAnalysis } from "$stores/map/selectedAnalysis";
  import Sprout from "svelte-material-icons/Sprout.svelte";

  export let name;

  $: selected = $selectedAnalysis === name;
  $: if ($selectedAnalysis) selected = $selectedAnalysis === name;

  const click = () => {
    const currentSelection = $selectedAnalysis === name ? "" : name;
    $selectedAnalysis = currentSelection;
  };
</script>

<button
  data-tip={name}
  class={`w-10 h-10 p-1 hover:bg-gray-100 ${
    selected ? "text-green-600" : "text-gray-800"
  } ${name && "tooltip tooltip-bottom"}`}
  on:click={click}
>
  <Sprout size="100%" />
</button>
