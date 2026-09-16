"""
Script to download satellite images and run the forest monitoring pipeline
"""

import logging

from spai.data.satellite import download_satellite_imagery, explore_satellite_imagery
from spai.analytics.forest_monitoring import forest_monitoring
from spai.storage import Storage
from spai.config import SPAIVars
from spai.logging.log import Result, log_inputs, log_results
from tqdm import tqdm

from src.status_registry import BUILDING, READY, set_error, set_status

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s"
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    storage = None
    try:
        storage = Storage()["data"]
        vars = SPAIVars()
        set_status(storage, BUILDING, "Preparing forest monitoring pipeline...")

        # explore available images
        logger.info("Looking for images in the last month")
        aoi = vars["AOI"]
        dates = vars["DATES"]

        log_inputs({"AOI": aoi, "DATES": dates})

        set_status(storage, BUILDING, "Looking for satellite images...")
        images = explore_satellite_imagery(aoi, dates, cloud_cover=10)

        if not images:
            raise ValueError(f"No images found for the given datetime: {dates}")

        # download images and save them in the storage
        collection = "sentinel-2-l2a"
        logger.info("Found %s image%s", len(images), "s" if len(images) > 1 else "")
        set_status(storage, BUILDING, "Downloading satellite images...")
        for image in tqdm(images, desc="Downloading images..."):
            existing_images = storage.list(f"{collection}*.tif")
            existing_dates = [
                img.split("_")[1].split(".")[0] for img in existing_images
            ]
            date = image["datetime"].split("T")[0]
            # check if image is already downloaded
            if date in existing_dates or image in existing_images:
                continue
            logger.info("Downloading new image: %s", date)
            path = download_satellite_imagery(storage, aoi, date, collection)
            logger.info("Image saved at %s", path)

        # Process and run the forest monitoring pipeline
        collection = "sentinel-2-l2a"
        downloaded_images = storage.list(f"{collection}*.tif")

        set_status(storage, BUILDING, "Processing forest monitoring analytics...")
        for downloaded_image in tqdm(downloaded_images, desc="Processing images..."):
            date = downloaded_image.split("_")[1].split(".")[
                0
            ]  # Extract date from image name
            forest_monitoring(downloaded_image, date, aoi, storage)

        # Read analytics tables written by forest_monitoring and log the most recent row
        results = []
        if storage.exists("AOI_Vegetation_Growth.json"):
            growth_df = storage.read("AOI_Vegetation_Growth.json")
            latest = growth_df.iloc[0]
            results += [
                Result(
                    label="Vegetation area",
                    value=round(latest["Vegetation Ha"], 2),
                    unit="ha",
                ),
                Result(
                    label="Non-vegetation area",
                    value=round(latest["Not Vegetation Ha"], 2),
                    unit="ha",
                ),
            ]
        if storage.exists("AOI_Vegetation_Quality.json"):
            quality_df = storage.read("AOI_Vegetation_Quality.json")
            latest = quality_df.iloc[0]
            results += [
                Result(
                    label="Healthy vegetation",
                    value=round(latest["Healthy Vegetation"], 2),
                    unit="ha",
                ),
                Result(
                    label="Very healthy vegetation",
                    value=round(latest["Very Healthy Vegetation"], 2),
                    unit="ha",
                ),
                Result(
                    label="Sparse or unhealthy vegetation",
                    value=round(latest["Sparse or Unhealthy Vegetation"], 2),
                    unit="ha",
                ),
                Result(
                    label="Bare ground",
                    value=round(latest["Bare Ground"], 2),
                    unit="ha",
                ),
            ]
        if results:
            log_results(results)

        set_status(storage, READY, "Pipeline completed successfully")
    except Exception:
        logger.exception("Pipeline failed")
        try:
            if storage is None:
                storage = Storage()["data"]
            set_error(storage)
        except Exception:
            logger.warning("Failed to write pipeline error status", exc_info=True)
        raise
