"""
Script to run the forest monitoring pipeline
"""

from spai.analytics.forest_monitoring import forest_monitoring
from spai.storage import Storage
from tqdm import tqdm
from spai.config import SPAIVars

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    collection = "sentinel-2-l2a"
    images = storage.list(f"{collection}*.tif")

    if not images:
        raise ValueError("No images found for the given AoI. The process will stop.")

    aoi = vars["AOI"]
    for image in tqdm(images, desc="Processing images..."):
        date = image.split("_")[1].split(".")[0]  # Extract date from image name
        forest_monitoring(image, date, aoi, storage)
