import src.gold_finder.data_loading as dl

PIXEL_PER_NM = 1.7897  # all images in the datset that I've seen has this scale
PIXEL_PER_MICRON = PIXEL_PER_NM * 1000


def pixels_to_microns(*args: int, pixels_per_micron: float = PIXEL_PER_MICRON,
                      bar_pos: dl.BarPosition = dl.BarPosition.TOP) -> tuple[float, ...]:
    """
    Converts pixel coordinates to microns
    
    :param args: The pixel coordinates
    :param pixels_per_micron: The conversion ratio of pixels to nanometers
    :param bar_pos: The position of the scale bar in the image. Used for adding the offset to the conversion
                    (since that's how the results csv files are formatted). Is only used if there are two args
    :return: The coordinates in microns
    """

    if len(args) == 2:
        offset = bar_pos.get_offset((args[0], args[1]))
        args = (args[0] + offset[0], args[1] + offset[1])
    
    return tuple(arg / pixels_per_micron for arg in args)


def micron_to_pixels(*args: float, pixels_per_micron: float = PIXEL_PER_MICRON,
                     bar_pos: dl.BarPosition = dl.BarPosition.TOP) -> tuple[int, ...]:
    """
    Converts micron coordinates to pixels
    
    :param args: The micron coordinates
    :param pixels_per_micron: The conversion ratio of pixels to nanometers
    :param bar_pos: The position of the scale bar in the image. Used for adding the offset to the conversion
                    (since that's how the results csv files are formatted). Is only used if there are two args
    :return: The coordinates in pixels
    """
    
    pixels = tuple(int(arg * pixels_per_micron) for arg in args)
    
    if len(pixels) == 2:
        # unpack and re-pack the tuple to avoid PyCharm giving a type warning
        offset = bar_pos.get_offset((pixels[0], pixels[1]))
        pixels = (pixels[0] - offset[0], pixels[1] - offset[1])
    
    return pixels
