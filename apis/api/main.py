"""
Analytics API
"""

import argparse

import pandas as pd

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from spai.storage import Storage
from spai.config import SPAIVars

from prometheus_fastapi_instrumentator import Instrumentator

from src.pipeline_status import (
    data_available_payload,
    data_unavailable_http,
    read_pipeline_status,
)
from src.lazy import LazyObject

app = FastAPI(title="SPAI API — forest-monitoring")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app=app)

storage = LazyObject(lambda: Storage()["data"])
vars = LazyObject(SPAIVars)


@app.get("/", include_in_schema=False)
def root():
    return {
        "service": "SPAI API",
        "name": "forest-monitoring",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
        "pipeline_status": "/pipeline/status",
    }


@app.get("/analytics/{analytics_file}")
async def analytics(analytics_file: str):
    """
    Return forest monitoring analytics

    Parameters
    ----------
    analytics_file : str
        Name of analytics file

    Returns
    -------
    analytics : dict
        Dictionary with analytics

    Raises
    ------
    HTTPException
        If analytics file doesn't exist
    """
    try:
        if not storage.exists(f"{analytics_file}.json"):
            raise HTTPException(
                status_code=404, detail="Not found."
            )
        analytics = storage.read(f"{analytics_file}.json")
        # Format date to ensure it is in the correct format
        if isinstance(analytics.index, pd.DatetimeIndex):
            analytics.index = analytics.index.strftime("%Y-%m-%d")
        analytics = analytics.to_dict()
        return analytics
    except HTTPException:
        raise
    except Exception:
        raise data_unavailable_http()


@app.get("/images")
def retrieve_images():
    """
    Return available images

    Returns
    -------
    images : list
        List of available images in tif format
    """
    try:
        return storage.list("*.tif")
    except Exception:
        raise data_unavailable_http()


@app.get("/aoi")
def retrieve_aoi():
    try:
        return vars["AOI"]
    except Exception:
        raise data_unavailable_http()


@app.get("/pipeline/status")
def pipeline_status():
    """Current pipeline status registry from storage."""
    return read_pipeline_status(storage)


@app.get("/data_available")
def data_available():
    return data_available_payload(read_pipeline_status(storage))


@app.get("/health")
def health():
    return {"status": "ok"}


# need this to run in background
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
