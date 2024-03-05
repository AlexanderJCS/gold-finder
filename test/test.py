from unittest import TestCase
import src.data.data_loading as dl


class AccuracyTest(TestCase):
    def test_accuracy(self):
        dl.get_image_bundles()
