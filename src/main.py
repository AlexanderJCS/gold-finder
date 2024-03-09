import matplotlib.pyplot as plt
import numpy as np

from src.gold_finder import data_loading as dl
from src.gold_finder import gold_finder as gf
from src.helper import masking
from src.network import density


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
    for bundle in dl.get_image_bundles("../data/analyzed synapses/"):
        if bundle.name != "S4":
            continue
        
        apply_mask = True
        masked = masking.apply_mask(bundle.image, bundle.mask) if apply_mask else bundle.image
        
        gold_locations = gf.GoldFinder(masked).find_gold()
        density_score = density.density(gold_locations)
        
        print(f"{density_score=}")
        
        show_points_on_image(masked, gold_locations)
        
        bundle.image.close()
        
        input("Press enter to continue: ")


if __name__ == "__main__":
    main()
