PIXEL_PER_NM = 1.7897  # all images in the datset that I've seen has this scale
PIXEL_PER_MICRON = PIXEL_PER_NM * 1000


def pixels_to_microns(*args: int, pixels_per_micron: float = PIXEL_PER_MICRON) -> tuple[float, ...]:
    """
    Converts pixel coordinates to microns
    
    :param args: The pixel coordinates
    :param pixels_per_micron: The conversion ratio of pixels to nanometers
    :return: The coordinates in microns
    """
    
    return tuple(arg / pixels_per_micron for arg in args)


def microns_to_pixels(*args: float, pixels_per_micron: float = PIXEL_PER_MICRON) -> tuple[int, ...]:
    """
    Converts micron coordinates to pixels
    
    :param args: The micron coordinates
    :param pixels_per_micron: The conversion ratio of pixels to nanometers
    :return: The coordinates in pixels
    """
    
    return tuple(int(arg * pixels_per_micron) for arg in args)
