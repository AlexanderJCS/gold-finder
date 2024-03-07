import matplotlib.pyplot as plt
import numpy as np

from src.data import data_loading as dl
from src.data import gold_finder as gf
from src.helper import masking


def main():
    for bundle in dl.get_image_bundles("../data/analyzed synapses/"):
        if bundle.name != "S1":
            continue
        
        masked = masking.apply_mask(bundle.image, bundle.mask)
        
        gold_locations = gf.GoldFinder(masked).find_gold()
        
        plt.imshow(np.array(masked), cmap="gray")
        plt.scatter(
            x=[coord[0] for coord in gold_locations],
            y=[coord[1] for coord in gold_locations],
            c="red",
            alpha=0.5,
            s=5
        )
        plt.show()
        
        bundle.image.close()
        input("Press enter to continue")


if __name__ == "__main__":
    main()
