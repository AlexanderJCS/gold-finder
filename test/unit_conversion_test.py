from unittest import TestCase
import src.helper.unit_conversion as uc


class TestUnitConversion(TestCase):
    def test_pixels_to_nm(self):
        self.assertAlmostEqual(*uc.pixels_to_microns(0), 0.0, delta=0.001)
        
        # 6nm set #14 on the S13 image
        self.assertAlmostEqual(*uc.pixels_to_microns(1232), 0.688, delta=0.001)  # x
        self.assertAlmostEqual(*uc.pixels_to_microns(1150), 0.642, delta=0.001)  # y
        
        # 12nm set #1 for the S15 image
        self.assertAlmostEqual(*uc.pixels_to_microns(1166), 0.651, delta=0.001)  # x
        self.assertAlmostEqual(*uc.pixels_to_microns(878), 0.491, delta=0.001)   # y
        