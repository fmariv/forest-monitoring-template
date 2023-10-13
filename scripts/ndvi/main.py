from spai.storage import Storage
import numpy as np

# retrieve all images
storage = Storage("data")
images = storage.list("S2*")
print("Found the following images:", images)


# compute ndvis


def ndvi(image):
    ds = storage.read(image)
    red = ds.read(4).astype(np.float32)
    nir = ds.read(8)
    ndvi = (nir - red) / (nir + red)
    date = image.split("_")[1].split(".")[0]
    return storage.create(ndvi, f"NDVI_{date}.tif", ds=ds)


paths = [ndvi(image) for image in images]
print("NDVI images saved at", paths)
