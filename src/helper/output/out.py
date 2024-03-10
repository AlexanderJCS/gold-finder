from PIL import Image

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from src.network import density


def gen_visualization(image: Image, clusters: dict, display: bool, save_to: str) -> None:
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
        cluster_color = np.random.rand(3, )
        
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


def create_output_df(clusters: dict) -> pd.DataFrame:
    """
    Creates a DataFrame from the clusters that can be saved to a CSV file. This dataframe is representative of
    everything the Golden algorithm found during its run

    :param clusters: The clusters of particles
    :return: A DataFrame of the clusters
    """
    
    rows_list = []
    
    for cluster_num, cluster_values in clusters.items():
        cluster_density = density.density(cluster_values)
        
        for coord in cluster_values:
            rows_list.append({
                "particle_x": coord[0],
                "particle_y": coord[1],
                "cluster_id": cluster_num,
                "cluster_density": cluster_density
            })
    
    return pd.DataFrame(rows_list)
