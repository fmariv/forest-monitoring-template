"""
Script to download satellite images and run the forest monitoring pipeline
"""

from spai.data.satellite import download_satellite_imagery, explore_satellite_imagery
from spai.analytics.forest_monitoring import forest_monitoring
from spai.storage import Storage
from spai.config import SPAIVars
from tqdm import tqdm

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    try:
        # explore available images
        print("Looking for images in the last month")
        aoi = vars["AOI"]
        dates = vars["DATES"]
        images = explore_satellite_imagery(aoi, dates, cloud_cover=10)

        if not images:
            raise ValueError(f"No images found for the given datetime: {dates}")

        # download images and save them in the storage
        collection = "sentinel-2-l2a"
        print("Found", len(images), f"image{'s' if len(images) > 1 else ''}")
        for image in tqdm(images, desc="Downloading images..."):
            existing_images = storage.list(f"{collection}*.tif")
            dates = [image.split("_")[1].split(".")[0] for image in existing_images]
            date = image["datetime"].split("T")[0]
            # check if image is already downloaded
            if date in dates or image in existing_images:
                continue
            print("Downloading new image:", date)
            path = download_satellite_imagery(storage, aoi, date, collection)
            print("Image saved at", path)

        # Process and run the forest monitoring pipeline
        collection = "sentinel-2-l2a"
        downloaded_images = storage.list(f"{collection}*.tif")

        for downloaded_image in tqdm(downloaded_images, desc="Processing images..."):
            date = downloaded_image.split("_")[1].split(".")[
                0
            ]  # Extract date from image name
            forest_monitoring(downloaded_image, date, aoi, storage)

    except Exception as e:
        print(f"An error occurred: {e}. The process will stop.")
