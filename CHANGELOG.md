# Changelog

All notable changes to this project are documented in this file.

Releases use date-based versions: `YYYY.MM.dd`.

## [2026.09.25]

### Added

- Shared XYZ tile API integration: UI mints `POST /session` server-side and appends `session=…` to Leaflet tile URLs.
- Cloud UI image bakes `XYZ_URL=spai.staging.xyz.earthpulse.ai` and `STORAGE_NAME=data` via `.env` / Dockerfile (`ENV` + printf). Local fallback remains `localhost:8001` (`spai xyz`).

### Changed

- Raster tiles no longer served by the project API; map/analytics layers point at the shared XYZ host.
- `uis[].env` keeps only `API_URL: api.api` (deploy placeholders). Literal `XYZ_URL` cannot go in `spai.config.yaml` because deploy treats every env value as `type.name`.

### Removed

- API endpoint `GET /images/{image}/{z}/{x}/{y}.png` (tiles moved to shared XYZ). List endpoint `GET /images` kept for the date selector.

## [2026.09.16]

### Added

- Friendly `GET /` response (`service: "SPAI API"`, name: `forest-monitoring`).
- Pipeline status hardening: `/pipeline/status` never raises; banner guards missing `api_url` and keeps polling after Ready/Error (cron-friendly).
- UI Docker build uses `yarn.lock` when present (`--frozen-lockfile` with install fallback).
- `.env.example` with `VITE_ENV=PRO` only (no secrets).

### Changed

- Ready banner only appears on a live transition (e.g. Building → Ready), not on every dashboard visit or poll.
- After Ready, transient API blips no longer escalate to Unreachable.
- UI Docker images overwrite `.env` with `VITE_ENV=PRO` only (no secrets baked into images).
- API error responses use generic messages (no `detail=str(e)` leaks); data endpoints return 503 when Storage/vars fail.

### Fixed

- Bootstrap robustness: LazyObject Storage/Vars in the API; safe SSR fetches; scripts write `set_error` even if Storage fails early.
- Generic pipeline error messages for the UI banner (technical detail stays in logs).
- SSR bootstrap uses `safeFetch` for images/analytics/aoi (no crash when API is down).
- Removed the red “No images or layers have been found” banner while the pipeline is still preparing data; Analytics sidebar stays visible.
- Forest analytics pie/layers only render when dates and series are available (no broken requests during empty bootstrap).
- Script/API Docker builds: install GDAL build deps and bump `rasterio>=1.4.3` so images build on Python 3.12.

## [2026.09.15]

### Added

- Docker images pinned via `image: …/:latest` in `spai.config.yaml` (Artifact Registry).
- End-to-end pipeline status wiring: script registry → storage → `GET /pipeline/status` → UI banner.
- UI Dockerfiles switched to yarn; `VITE_ENV=PRO` for HTTPS API URLs in cloud.
