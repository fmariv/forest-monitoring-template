import { env } from "$env/dynamic/private";

export async function load({ fetch }) {
  const xyz_url = "http://" + env.XYZ_URL;
  const analytics_url = "http://" + env.ANALYTICS_URL;
  let res = [
    await fetch(`${xyz_url}/`),
    await fetch(`${analytics_url}/AOI_Vegetation_Growth`),
    await fetch(`${analytics_url}/AOI_Vegetation_Quality`),
    await fetch(`${xyz_url}/aoi`),
  ];
  const [images, growth, health, aoi] = await Promise.all(
    res.map((r) => r.json())
  );
  return {
    xyz_url,
    images,
    analytics: {
      "Vegetation Quality": growth,
      "Vegetation Health": health,
    },
    colors: {
      "Vegetation Quality": ["#25dd47", "#ff0000"],
      "Vegetation Health": ["#1EA140", "#38EB67", "#F5F53D", "#F54B3D"],
    },
    aoi,
  };
}
