<script>
  import Sprout from "svelte-material-icons/Sprout.svelte";

  export let tooltip = "Mock Quality";

  export let selectedAnalysis;

  $: selected = selectedAnalysis === tooltip;

  const click = () => {
    selectedAnalysis === tooltip
      ? (selectedAnalysis = "")
      : (selectedAnalysis = tooltip);
  };
</script>

<button
  data-tip={tooltip}
  class={`w-10 h-10 p-1 hover:bg-gray-100 ${
    selected ? "text-green-600" : "text-gray-800"
  } ${tooltip && "tooltip tooltip-bottom"}`}
  on:click={click}
>
  <Sprout size="100%" />
</button>
