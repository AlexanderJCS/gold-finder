import argparse

import matplotlib.pyplot as plt
import numpy as np

from src.gold_finder import data_loading as dl
from src.gold_finder import gold_finder as gf
from src.helper import masking
from src.network import density


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Golden",
        description="Find gold particles and their density in electron microscopy images"
    )
    
    parser.add_argument(
        "name",
        type=str,
        help="The name of the dataset to analyze. This is the name of the folder in the 'analyzed synapses' directory,"
             "e.g., 'S1' or 'S7'"
    )
    
    parser.add_argument(
        "-m", "--mask",
        action="store_true",
        help="Whether to apply the mask to the image before finding gold particles. Default: False"
    )
    
    parser.add_argument(
        "-v", "--visual",
        action="store_true",
        help="Whether to display the image with the gold particles marked on it. Default: False"
    )
    
    return parser.parse_args()


def show_points_on_image(image, points):
    plt.imshow(np.array(image), cmap="gray")
    
    plt.scatter(
        x=[coord[0] for coord in points],
        y=[coord[1] for coord in points],
        c="red",
        alpha=0.25,
        s=5
    )
    
    plt.show()


def main():
    args = get_args()
    
    bundles = dl.get_image_bundles("./data/analyzed synapses/")
    bundle_dict = {bundle.name: bundle for bundle in bundles}
    
    if args.name not in bundle_dict:
        print(f"Dataset '{args.name}' not found")
        return
    
    bundle = bundle_dict[args.name]
    
    img_luminosity = gf.GoldFinder.get_avg_luminosity(bundle.image)
    image = masking.apply_mask(bundle.image, bundle.mask) if args.mask else bundle.image
    
    gold_locations = gf.GoldFinder(image, img_luminosity=img_luminosity).find_gold()
    density_score = density.density(gold_locations)
    
    print(f"{density_score=}")
    
    if args.visual is True:
        show_points_on_image(image, gold_locations)


if __name__ == "__main__":
    main()
