import pandas as pd
import numpy as np

from unittest import TestCase

from src.helper import units as uc, data_loading as dl
from src.gold_finder import gold_finder as gf

POSITIVE_DISTANCE_NM = 10  # units: nanometers, the leeway for a predicted gold particle position vs actual position
POSITIVE_DISTANCE_MICRONS = POSITIVE_DISTANCE_NM / 1000


class AccuracyTest(TestCase):
    @staticmethod
    def get_confusion_matrix(bundle: dl.ImageBundle, gold_locations):
        true_positive_12nm = 0
        true_positive_6nm = 0
        
        false_positive = 0
        
        for location in gold_locations:
            # This value is true if the location is in the mask, false if it isn't
            # This is required since, for some reason, the ground truth data also includes some particles that are not
            # in the mask. To fix this, if the particle is outside the mask but is found in the ground truth data anyway
            # count it as a true positive. But if the particle is outside the mask and is not found in the ground truth
            # data, do *not* count it as a false positive.
            in_mask: bool = bundle.mask.getpixel(location) != 255

            micron_location = uc.pixels_to_microns(*location)

            distances_6nm = np.sqrt((bundle.ground_truth_6nm["X"] - micron_location[0]) ** 2 +
                                    (bundle.ground_truth_6nm["Y"] - micron_location[1]) ** 2)
            
            distances_12nm = np.sqrt((bundle.ground_truth_12nm["X"] - micron_location[0]) ** 2 +
                                     (bundle.ground_truth_12nm["Y"] - micron_location[1]) ** 2)

            if any(distances_12nm <= POSITIVE_DISTANCE_MICRONS):
                true_positive_12nm += 1
            
            elif any(distances_6nm <= POSITIVE_DISTANCE_MICRONS):
                true_positive_6nm += 1
            
            elif in_mask:
                false_positive += 1
        
        false_negitive_12nm = len(bundle.ground_truth_12nm) - true_positive_12nm
        false_negitive_6nm = len(bundle.ground_truth_6nm) - true_positive_6nm
        
        confusion_matrix_df = pd.DataFrame({
            "12nm": [true_positive_12nm, false_negitive_12nm],
            "6nm": [true_positive_6nm, false_negitive_6nm]
        }, index=["true positive", "false negative"])
        
        print(f"\n--- CONFUSION MATRIX FOR {bundle.name} ---")
        print(f"false positives: {false_positive}")
        print(confusion_matrix_df)
        
        return false_positive, confusion_matrix_df
    
    def test_accuracy(self):
        image_bundles = list(dl.get_image_bundles("../data/analyzed synapses/"))
        
        for bundle in image_bundles:
            self.assertIsNotNone(bundle.image, msg=f"Bundle name: {bundle.name}")
            self.assertIsNotNone(bundle.mask, msg=f"Bundle name: {bundle.name}")
            self.assertEqual(bundle.image.size, bundle.mask.size, msg=f"Bundle name: {bundle.name}")
            self.assertIsNotNone(bundle.ground_truth_6nm, msg=f"Bundle name: {bundle.name}")
            self.assertIsNotNone(bundle.ground_truth_12nm, msg=f"Bundle name: {bundle.name}")
        
        if len(image_bundles) == 0:
            self.fail("No image bundles were found")
        
        confusion_matrices = []
        sum_false_positives = 0
        
        # Calculate the gold locations and get the confusion matrices
        for bundle in image_bundles:
            gold_locations = gf.GoldFinder(bundle.image).find_gold()
            
            false_positives, confusion_matrix = self.get_confusion_matrix(
                bundle,
                gold_locations
            )
            
            sum_false_positives += false_positives
            confusion_matrices.append(confusion_matrix)
        
        # Calculate the summed confusion matrix
        summed_confusion_matrix = pd.DataFrame({
            "12nm": [0, 0],
            "6nm": [0, 0]
        }, index=["true positive", "false negative"])
        
        for matrix in confusion_matrices:
            summed_confusion_matrix += matrix
            
        print("\n--- SUMMED CONFUSION MATRIX ---")
        print(f"false positives: {sum_false_positives}")
        print(summed_confusion_matrix)
        