<script>
  import Lines from "$components/viz/Lines.svelte";
  import { selectedAnalysis } from "$stores/map/selectedAnalysis";
  import { compareAsc, parseISO } from "date-fns";

  export let height;
  export let analytics;
  export let colors;

  $: selectedColors = colors[$selectedAnalysis];

  $: displayedAnalytics = analytics[$selectedAnalysis];

  let options = {};
  $: sorted_dates = Object.keys(displayedAnalytics.Total).sort((a, b) =>
    compareAsc(parseISO(a), parseISO(b))
  );

  $: series = Object.keys(displayedAnalytics)
    .filter((key) => key !== "Total") // Exclude the "Total" key
    .map((category) => ({
      name: category,
      data: sorted_dates.map((date) => {
        const categoryValue = displayedAnalytics[category][date];
        const totalValue = displayedAnalytics.Total[date];
        return (100 * categoryValue) / totalValue; // Calculate percentage
      }),
    }))
    .sort((a, b) => {
      // Calculate the sum of each series
      const sumA = a.data.reduce((acc, curr) => acc + curr, 0);
      const sumB = b.data.reduce((acc, curr) => acc + curr, 0);
      return sumB - sumA; // Sort from high to low
    });

  $: options = {
    colors: selectedColors,
    xaxis: {
      categories: sorted_dates,
      type: "datetime",
    },
    series: series,
  };
</script>

<Lines {options} {height} />
