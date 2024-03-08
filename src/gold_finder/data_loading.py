from dataclasses import dataclass
from typing import Iterator
from enum import Enum

from PIL import Image

import pandas as pd
import pathlib


class BarPosition(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


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
        
        # Load the image
        image_bar_pos = None
        
        for file in subdir.iterdir():
            if file.is_file() and file.suffix == ".tif" and "mask" not in file.name and "color" not in file.name:
                image_bar_pos = get_bar_position(Image.open(file).convert("L"))
                bundle.image = load_image(file, image_bar_pos)
                break
        
        if bundle.image is None or image_bar_pos is None:
            raise FileNotFoundError(f"No image found for {bundle.name}!")
        
        # Load the mask if it exists
        mask_files = list(subdir.glob("*mask.tif"))
        if len(mask_files) > 0:
            bundle.mask = load_image(mask_files[0], image_bar_pos)
        
        for file in (subdir / "Results").glob("*.csv"):
            if "6nm" in file.name:
                bundle.ground_truth_6nm = pd.read_csv(file)
            elif "12nm" in file.name:
                bundle.ground_truth_12nm = pd.read_csv(file)
        
        yield bundle


def load_image(path: pathlib.Path, src_img_bar_pos: BarPosition | None = None) -> Image:
    """
    Loads an image from a file path and crops the scale bar
    
    :param path: The path to the image to load
    :param src_img_bar_pos: The original image. Used for cropping masks where you otherwise can't tell where to crop.
                            Leave as None if the image is not a mask
    :return: The loaded image
    """
    
    image = Image.open(path)
    return crop_scale_bar(image.convert("L"), src_img_bar_pos if src_img_bar_pos is not None else image)


def get_bar_position(image: Image) -> BarPosition:
    """
    Determines the position of the scale bar in the image
    
    :param image: The image to analyze
    :return: The position of the scale bar
    """
    
    if image.getpixel((image.width // 2, 0)) == 0:
        return BarPosition.TOP
    if image.getpixel((image.width // 2, image.height - 1)) == 0:
        return BarPosition.BOTTOM
    if image.getpixel((0, image.height // 2)) == 0:
        return BarPosition.LEFT
    if image.getpixel((image.width - 1, image.height // 2)) == 0:
        return BarPosition.RIGHT
    
    raise ValueError("No scale bar found")


def crop_scale_bar(image: Image, bar_position: BarPosition | None = None) -> Image:
    """
    Crops the scale bar from the image
    
    :param image: The image to crop
    :param bar_position: The position of the scale bar. If None, the function will determine the position
    :return: The cropped image, or the original image if no scale bar was found
    """
    
    if bar_position is None:
        bar_position = get_bar_position(image)
    
    if bar_position == BarPosition.TOP:
        return image.crop((0, image.height - image.width, image.width, image.width))
    
    if bar_position == BarPosition.BOTTOM:
        return image.crop((0, 0, image.width, image.width))
    
    if bar_position == BarPosition.LEFT:
        return image.crop((image.width - image.height, 0, image.height, image.height))
    
    if bar_position == BarPosition.RIGHT:
        return image.crop((0, 0, image.height, image.height))
    
    return image
