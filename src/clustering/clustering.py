from sklearn.cluster import DBSCAN

import numpy as np


def gold_cluster(particle_locs: list[tuple[int, int]], image_dim: tuple[int, int]) -> dict[int, list[tuple[int, int]]]:
    """
    Clusters the immunigold particles
    
    :param particle_locs: The particle locations
    :param image_dim: The image dimensions
    :return: A dictionary of the cluster name and a list of its points
    """
    
    clustering = DBSCAN(
        eps=min(image_dim) / 10,  # just provide a rough estimate of a good EPS
        min_samples=3
    )

    clusters = clustering.fit_predict(np.array(particle_locs))
    
    cluster_dict = {}
    for cluster_num in set(clusters):
        # generate a list of the particle locations only if the cluster == cluster_num
        cluster_dict[cluster_num] = [
            tuple(particle_locs[i])
            for i, cluster in enumerate(clusters)
            if cluster == cluster_num
        ]
    
    return cluster_dict
