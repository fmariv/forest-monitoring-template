<script>
  import Lines from "$components/viz/Lines.svelte";
  import { selectedAnalysis } from "$stores/map/selectedAnalysis";
  import { compareAsc, parseISO } from "date-fns";

  export let height;
  export let analytics;

  $: displayedAnalytics = analytics[$selectedAnalysis];

  let options = {};
  $: sorted_dates = Object.keys(displayedAnalytics.Total).sort((a, b) =>
    compareAsc(parseISO(a), parseISO(b))
  );

  $: if (sorted_dates)
    options = {
      colors: ["#25dd47", "#ff0000"],
      xaxis: {
        categories: sorted_dates,
        type: "datetime",
      },
      series: [
        {
          name: "Vegetation Ha",
          data: sorted_dates.map(
            (date) =>
              (100 * displayedAnalytics["Vegetation Ha"][date]) /
              displayedAnalytics.Total[date]
          ),
        },
        {
          name: "Not Vegetation Ha",
          data: sorted_dates.map(
            (date) =>
              (100 * displayedAnalytics["Not Vegetation Ha"][date]) /
              displayedAnalytics.Total[date]
          ),
        },
      ],
    };
</script>

<Lines {options} {height} />
