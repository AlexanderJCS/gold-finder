from unittest import TestCase

import src.helper.unit_conversion as uc

import random


class TestUnitConversion(TestCase):
    def test_back_and_forth(self):
        for i in range(100_000):
            rand_coords = (random.randint(0, 1000), random.randint(0, 1000))

            px_mic_px = uc.pixels_to_microns(*uc.micron_to_pixels(*rand_coords))
            
            # pixels to microns to pixels
            for coord1, coord2 in zip(rand_coords, px_mic_px):
                self.assertAlmostEqual(
                    coord1,
                    coord2,
                    msg=f"failed on iteration {i} | pixels to microns: {uc.pixels_to_microns(*rand_coords)}",
                    delta=0.001
                )
            
            mic_px_mic = uc.micron_to_pixels(*uc.pixels_to_microns(*rand_coords),)
            
            # microns to pixels to microns
            for coord1, coord2 in zip(rand_coords, mic_px_mic):
                self.assertAlmostEqual(
                    coord1,
                    coord2,
                    delta=0.001,
                    msg=f"failed on iteration {i}| microns to pixels: {uc.micron_to_pixels(*rand_coords)}"
                )
    
    def test_pixels_to_nm(self):
        self.assertAlmostEqual(*uc.pixels_to_microns(0), 0.0, delta=0.001)
        
        # 6nm set #14 on the S13 image
        self.assertAlmostEqual(*uc.pixels_to_microns(1232), 0.688, delta=0.001)  # x
        self.assertAlmostEqual(*uc.pixels_to_microns(1150), 0.642, delta=0.001)  # y
        
        # 12nm set #1 for the S15 image
        self.assertAlmostEqual(*uc.pixels_to_microns(1166), 0.651, delta=0.001)  # x
        self.assertAlmostEqual(*uc.pixels_to_microns(878), 0.491, delta=0.001)   # y
        