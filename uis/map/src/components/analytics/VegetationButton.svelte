<script>
  import Sprout from "svelte-material-icons/Sprout.svelte";

  export let name;

  export let selectedAnalysis;

  $: selected = selectedAnalysis === name;

  const click = () => {
    selectedAnalysis === name
      ? (selectedAnalysis = "")
      : (selectedAnalysis = name);
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
