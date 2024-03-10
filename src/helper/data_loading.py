from __future__ import annotations  # for type hinting the return type of bar_pos
from dataclasses import dataclass
from typing import Iterator
from enum import Enum

from PIL import Image

import pandas as pd
import pathlib


class BarPosition(Enum):
    """
    Represents the position of the scale bar. Used for cropping the scale bar from the image & converting to microns
    """
    
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    
    def bar_location(self, image_dim: tuple[int, int]) -> tuple[int, int, int, int]:
        """
        Gets the offset of the scale bar from the edge of the image
        :return: A 4-element tuple that represents the scale bar position (left, top, right, bottom)
        """
        
        bar_width = abs(image_dim[0] - image_dim[1])
        
        if self == BarPosition.TOP:
            return 0, 0, image_dim[0], bar_width
        if self == BarPosition.BOTTOM:
            return 0, image_dim[1] - bar_width, image_dim[0], image_dim[1]
        if self == BarPosition.LEFT:
            return 0, 0, bar_width, image_dim[1]
        if self == BarPosition.RIGHT:
            return image_dim[0] - bar_width, 0, image_dim[0], image_dim[1]
    
    @staticmethod
    def bar_pos(image: Image) -> BarPosition:
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
        scale_bar = None
        
        for file in subdir.iterdir():
            if file.is_file() and file.suffix == ".tif" and "mask" not in file.name and "color" not in file.name:
                scale_bar = BarPosition.bar_pos(Image.open(file).convert("L"))
                bundle.image = load_image(file, scale_bar)
                break
        
        if bundle.image is None or scale_bar is None:
            raise FileNotFoundError(f"No image found for {bundle.name}!")
        
        # Load the mask if it exists
        mask_files = list(subdir.glob("*mask.tif"))
        if len(mask_files) > 0:
            bundle.mask = load_image(mask_files[0], scale_bar)
        
        for file in (subdir / "Results").glob("*.csv"):
            if "6nm" in file.name:
                bundle.ground_truth_6nm = pd.read_csv(file)
            elif "12nm" in file.name:
                bundle.ground_truth_12nm = pd.read_csv(file)
        
        yield bundle


def load_image(path: pathlib.Path, src_img_bar_pos: BarPosition) -> Image:
    """
    Loads an image from a file path and crops the scale bar
    
    :param path: The path to the image to load
    :param src_img_bar_pos: The original image. Used for cropping masks where you otherwise can't tell where to crop.
    :return: The loaded image
    """
    
    image = Image.open(path)
    return fill_scale_bar(image.convert("L"), src_img_bar_pos)


def fill_scale_bar(image: Image, bar_position: BarPosition) -> Image:
    """
    Fills the scale bar with white, which effectively allows it to be ignored when finding gold particles
    
    :param image: The image to paste the scale bar onto. This image will be modified
    :param bar_position: The position of the scale bar
    :return: The modified image
    """
    
    image.paste(255, bar_position.bar_location(image.size))
    return image
