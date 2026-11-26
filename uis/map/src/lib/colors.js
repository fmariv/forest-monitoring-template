/** Unified domain palette for Forest Monitoring charts (Growth + Health). */

export const GROWTH = {
	vegetation: '#2E7D32',
	notVegetation: '#C45C26'
};

export const HEALTH = {
	veryHealthy: '#1B5E20',
	healthy: '#66A63A',
	sparse: '#F9A825',
	bare: '#D84315'
};

/** Order matches Growth donut series / labels. */
export const GROWTH_COLORS = [GROWTH.vegetation, GROWTH.notVegetation];

/**
 * Order matches Health donut series:
 * Bare, Healthy, Sparse, Very Healthy
 */
export const HEALTH_PIE_COLORS = [
	HEALTH.bare,
	HEALTH.healthy,
	HEALTH.sparse,
	HEALTH.veryHealthy
];

/**
 * Order matches Health timeline series:
 * Very Healthy, Healthy, Sparse, Bare
 */
export const HEALTH_TIMELINE_COLORS = [
	HEALTH.veryHealthy,
	HEALTH.healthy,
	HEALTH.sparse,
	HEALTH.bare
];

export const CHART = {
	totalLabel: '#64748B',
	totalValue: '#172033',
	noData: '#64748B'
};

/** Leaflet tile opacity for analytic overlays (sat stays at 1). */
export const OVERLAY_OPACITY = 0.55;
