import pandas as pd

from unittest import TestCase

from src.helper import masking, unit_conversion as uc
from src.gold_finder import gold_finder as gf, data_loading as dl


POSITIVE_DISTANCE = 0.01  # units: micrometers, the leeway for a predicted gold particle position vs actual position


class AccuracyTest(TestCase):
    @staticmethod
    def get_confusion_matrix(name, gold_locations, ground_truth_6nm, ground_truth_12nm):
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
        
        print(f"--- CONFUSION MATRIX FOR {name} ---")
        print(f"false positives: {false_positive}")
        print(confusion_matrix_df)
        print()
        
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
            masked = masking.apply_mask(bundle.image, bundle.mask)
            gold_locations = gf.GoldFinder(masked).find_gold()
            
            false_positives, confusion_matrix = self.get_confusion_matrix(
                bundle.name,
                gold_locations,
                bundle.ground_truth_6nm,
                bundle.ground_truth_12nm
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
        