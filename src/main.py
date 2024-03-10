import argparse

from PIL import Image

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from src.gold_finder import data_loading as dl
from src.gold_finder import gold_finder as gf
from src.clustering import clustering
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
    
    parser.add_argument(
        "--dataloc",
        type=str,
        default=None,
        help="The location to store the data CSV file. If not specified, the data will not be saved."
    )
    
    parser.add_argument(
        "--figloc",
        type=str,
        default=None,
        help="The location to store the figure shown with the -m flag. If not specified, the figure will not be saved."
    )
    
    return parser.parse_args()


def show_points_on_image(image: Image, clusters: dict, display: bool, save_to: str) -> None:
    """
    Shows the image with the clusters and identified particles marked on it
    
    :param image: The base image to show
    :param clusters: The clusters of particles
    :param display: Whether to display the image
    :param save_to: The location to save the figure to. If None, the figure will not be saved
    """
    
    if not display and not save_to:
        return  # no sense in doing any work
    
    plt.imshow(np.array(image), cmap="gray")
    
    for cluster_num, cluster_values in clusters.items():
        cluster_color = np.random.rand(3,)
        
        plt.scatter(
            x=[coord[0] for coord in cluster_values],
            y=[coord[1] for coord in cluster_values],
            label=f"Cluster {cluster_num}",
            alpha=0.9,
            color=cluster_color,
            s=7
        )
        
        for coord in cluster_values:
            plt.text(coord[0], coord[1], f"C: {cluster_num}", fontsize=7, color="white")
    
    if display is True:
        plt.show()
    
    if save_to is not None:
        plt.savefig(save_to)


def create_df_from_clusters(clusters: dict) -> pd.DataFrame:
    """
    Creates a DataFrame from the clusters that can be saved as a CSV file
    
    :param clusters: The clusters of particles
    :return: A DataFrame of the clusters
    """
    
    df = pd.DataFrame(columns=["x", "y", "cluster_id", "cluster_density"])
    
    rows_list = []
    
    for cluster_num, cluster_values in clusters.items():
        cluster_density = density.density(cluster_values)
        
        for coord in cluster_values:
            rows_list.append({
                "x": coord[0],
                "y": coord[1],
                "cluster_id": cluster_num,
                "cluster_density": cluster_density
            })
    
    return pd.DataFrame(rows_list)


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
    clusters = clustering.gold_cluster(gold_locations, image.size)
    
    output_data = create_df_from_clusters(clusters)
    
    print(output_data)
    
    if args.dataloc is not None:
        output_data.to_csv(args.dataloc, index=False)
    
    show_points_on_image(image, clusters, args.visual, args.figloc)


if __name__ == "__main__":
    main()
