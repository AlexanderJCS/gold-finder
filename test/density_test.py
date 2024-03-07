from src.network import density

from unittest import TestCase
import numpy as np


class DensityTest(TestCase):
    def test_density(self):
        dense = gen_points(1, 100)
        sparse = gen_points(10, 100)
        
        dense_score = density.density(dense)
        sparse_score = density.density(sparse)
        
        print(f"\n{dense_score=:.2f}, {sparse_score=:.2f}")
        
        self.assertGreater(dense_score, sparse_score)
        

def gen_points(std_dev, num):
    return [(np.random.normal(0, std_dev), np.random.normal(0, std_dev)) for _ in range(num)]
    