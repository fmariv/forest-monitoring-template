"""
Script to run the forest monitoring pipeline
"""

from spai.analytics import forest_monitoring
from spai.storage import Storage
from tqdm import tqdm
from spai.config import SPAIVars

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    sensor = "S2L2A"  # or 'S2L1C'
    images = storage.list(f"{sensor}*.tif")
    aoi = vars["AOI"]
    for image in tqdm(images, desc="Processing images..."):
        forest_monitoring(image, aoi, storage)
