from dataclasses import dataclass
from typing import Iterator
from PIL import Image

import pandas as pd
import pathlib


@dataclass
class ImageBundle:
    name: str
    image: Image
    mask: Image
    ground_truth_6nm: pd.DataFrame | None
    ground_truth_12nm: pd.DataFrame | None


def get_image_bundles(base_path) -> Iterator[ImageBundle]:
    for subdir in pathlib.Path(base_path).iterdir():
        if not subdir.is_dir():
            continue
        
        bundle = ImageBundle(subdir.name, None, None, None, None)
        
        for file in subdir.iterdir():
            if file.is_file() and file.suffix == ".tif" and "mask" not in file.name and "color" not in file.name:
                bundle.image = load_image(file)
            
            elif file.is_file() and file.suffix == ".tif" and "mask" in file.name:
                bundle.mask = load_image(file)
        
        for file in (subdir / "Results").glob("*.csv"):
            if "6nm" in file.name:
                bundle.ground_truth_6nm = pd.read_csv(file)
            elif "12nm" in file.name:
                bundle.ground_truth_12nm = pd.read_csv(file)
        
        yield bundle


def load_image(path: pathlib.Path) -> Image:
    image = Image.open(path)
    return image.convert("L").crop((0, 0, image.width, image.width))
