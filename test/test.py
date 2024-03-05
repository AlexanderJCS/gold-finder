import math

import pandas as pd

from unittest import TestCase

from src.helper import masking, unit_conversion as uc
from src.data import gold_finder as gf, data_loading as dl


POSITIVE_DISTANCE = 0.01  # units: micrometers, the leeway for a predicted gold particle position vs actual position

MICRON_OFFSET_X = 0.00822  # the ground truth data is offset by a fixed amount. this offset is equivalen to 15 pixels
MICRON_OFFSET_Y = 0.01479  # the ground truth data is offset by a fixed amount. this offset is equivalent to 27 pixels


class AccuracyTest(TestCase):
    @staticmethod
    def verify_gold(gold_locations, ground_truth_6nm, ground_truth_12nm):
        true_positive_12nm = 0
        true_positive_6nm = 0
        
        false_positive = 0
        
        for location in gold_locations:
            micron_location = uc.pixels_to_microns(*location)

            distances_6nm = ((ground_truth_6nm["X"] - micron_location[0]) ** 2 +
                             (ground_truth_6nm["Y"] - micron_location[1]) ** 2) ** 0.5
            
            distances_12nm = ((ground_truth_12nm["X"] - micron_location[0]) ** 2 +
                              (ground_truth_12nm["Y"] - micron_location[1]) ** 2) ** 0.5

            if any(distances_12nm <= POSITIVE_DISTANCE):
                true_positive_12nm += 1
            
            elif any(distances_6nm <= POSITIVE_DISTANCE):
                true_positive_6nm += 1
            
            else:
                false_positive += 1
        
        false_negitive_12nm = len(ground_truth_12nm) - true_positive_12nm
        false_negitive_6nm = len(ground_truth_6nm) - true_positive_6nm
        
        confusion_matrix_df = pd.DataFrame({
            "12nm": [true_positive_12nm, false_negitive_12nm],
            "6nm": [true_positive_6nm, false_negitive_6nm]
        }, index=["true positive", "false negative"])
        
        print("--- CONFUSION MATRICES ---")
        print(f"False positives: {false_positive}")
        print(confusion_matrix_df)
    
    def test_accuracy(self):
        image_bundles = list(dl.get_image_bundles("../data/analyzed synapses/"))
        
        # for bundle in image_bundles:
        #     self.assertIsNotNone(bundle.image)
        #     self.assertIsNotNone(bundle.mask)
        #     self.assertIsNotNone(bundle.ground_truth_6nm)
        #     self.assertIsNotNone(bundle.ground_truth_12nm)
        
        if len(image_bundles) == 0:
            self.fail("No image bundles were found")
        
        for bundle in image_bundles:
            bundle.ground_truth_6nm["X"] -= MICRON_OFFSET_X
            bundle.ground_truth_6nm["Y"] -= MICRON_OFFSET_Y

            bundle.ground_truth_12nm["X"] -= MICRON_OFFSET_X
            bundle.ground_truth_12nm["Y"] -= MICRON_OFFSET_Y
            
            masked = masking.apply_mask(bundle.image, bundle.mask)
            gold_locations = gf.GoldFinder(masked).find_gold()
            self.verify_gold(gold_locations, bundle.ground_truth_6nm, bundle.ground_truth_12nm)
            break


def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

