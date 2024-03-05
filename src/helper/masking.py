from PIL import Image


def apply_mask(image: Image, mask: Image) -> Image:
    """
    Applies a mask to an image

    :param image: The image to apply the mask to
    :param mask: The mask to apply
    :return: The masked image
    """
    mask = mask.point(lambda p: p != 255, mode="1")
    return Image.composite(image, Image.new("L", image.size, 255), mask)
    