import { env } from '$env/dynamic/private';

/**
 * SPAI local run sets hosts as `host:port` (no scheme).
 * Local hosts stay HTTP; cloud hosts use https when VITE_ENV=PRO.
 */
function resolveServiceUrl(raw, fallback) {
	const value = (raw ?? '').trim() || fallback;
	if (/^https?:\/\//i.test(value)) return value.replace(/\/$/, '');
	const isLocal =
		/^(localhost|127\.0\.0\.1)(:\d+)?$/i.test(value) ||
		value.startsWith('localhost:') ||
		value.startsWith('127.0.0.1:');
	const scheme = isLocal ? 'http' : import.meta.env.VITE_ENV === 'PRO' ? 'https' : 'http';
	return `${scheme}://${value}`;
}

export async function load({ fetch }) {
	const api_url = resolveServiceUrl(env.API_URL, 'localhost:8021');
	const xyz_url = resolveServiceUrl(env.XYZ_URL, 'localhost:8001');

	// Injected automatically by `spai run` / deploy
	const project_name = env.SPAI_PROJECT_NAME;
	const workspace = env.SPAI_WORKSPACE_NAME;
	const api_key = env.SPAI_API_KEY || '';
	const storage_name = env.STORAGE_NAME || 'data';

	const safeFetch = async (path) => {
		try {
			const res = await fetch(`${api_url}${path}`);
			if (res.ok) return await res.json();
		} catch {
			// API may be unavailable during bootstrap
		}
		return null;
	};

	/** Mint opaque XYZ session server-side; Leaflet only sees session=… */
	const mintXyzSession = async () => {
		const headers = { 'Content-Type': 'application/json' };
		if (api_key) headers['X-API-Key'] = api_key;
		try {
			const res = await fetch(`${xyz_url}/session`, {
				method: 'POST',
				headers,
				body: JSON.stringify({ project_name, storage_name, workspace })
			});
			if (!res.ok) return null;
			const data = await res.json();
			return data?.session ? `session=${encodeURIComponent(data.session)}` : null;
		} catch {
			return null;
		}
	};

	const [images, analytics, aoi, xyz_query] = await Promise.all([
		safeFetch('/images'),
		safeFetch('/analytics/AOI_Vegetation_Growth'),
		safeFetch('/aoi'),
		mintXyzSession()
	]);

	return {
		api_url,
		xyz_url,
		xyz_query: xyz_query || '',
		images: Array.isArray(images) ? images : [],
		analytics: analytics ?? null,
		aoi: aoi ?? null
	};
}
