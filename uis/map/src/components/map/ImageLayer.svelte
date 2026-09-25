<script>
	import { onDestroy } from 'svelte';
	import { map } from '$stores/map/map';
	import { imageLayers } from '$stores/map/imageLayers';

	export let name = 'image';
	export let image;
	export let XYZ_URL;
	export let options = { maxZoom: 20 };
	export let bands = [4, 3, 2];
	export let stretch = [0, 3000];
	export let palette = 'viridis';
	/** Extra query string for spai-xyz, e.g. session=… from POST /session */
	export let query = '';

	const pane = options.pane || 'overlayPane';

	$: params = [`stretch=${stretch}`, `bands=${bands}`, `palette=${palette}`, query]
		.filter(Boolean)
		.join('&');

	$: url = `${XYZ_URL}/${image}/{z}/{x}/{y}.png?${params}`;

	$: if ($map && image) {
		(async () => {
			const L = await import('leaflet');
			if (!$map || !image) return;
			if ($imageLayers[pane]?.[name]) {
				$imageLayers[pane][name].setUrl(url);
			} else {
				const layer = L.tileLayer(url, options).addTo($map);
				imageLayers.addImageLayer(pane, name, layer);
			}
		})();
	}

	onDestroy(() => {
		imageLayers.removeImageLayer(name, pane);
	});
</script>
