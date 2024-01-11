"""
Script to run the forest monitoring pipeline
"""

from os.path import join

from spai.models import ProjectConfig
from spai.pulses import forest_monitoring
from spai.storage import Storage
from tqdm import tqdm

storage = Storage("data")

project = ProjectConfig()


if __name__ == "__main__":
    sensor = "S2L2A"  # or 'S2L1C'
    images = storage.list(f"{sensor}*.tif")
    aoi = project.aoi
    for image in tqdm(images, desc="Processing images..."):
        forest_monitoring(image, aoi, storage)
