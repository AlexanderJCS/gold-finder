from unittest import TestCase

import src.helper.unit_conversion as uc
import src.gold_finder.data_loading as dl

import random


class TestUnitConversion(TestCase):
    def test_back_and_forth(self):
        for i in range(100_000):
            rand_coords = (random.randint(0, 1000), random.randint(0, 1000))
            rand_bar_pos = random.choice(list(dl.BarPosition))
            
            px_mic_px = uc.pixels_to_microns(
                *uc.micron_to_pixels(*rand_coords, bar_pos=rand_bar_pos),
                bar_pos=rand_bar_pos
            )
            
            # pixels to microns to pixels
            for coord1, coord2 in zip(rand_coords, px_mic_px):
                self.assertAlmostEqual(
                    coord1,
                    coord2,
                    msg=f"Failed on iteration {i}, random bar pos: {rand_bar_pos}\n"
                        f"pixels to micron: {uc.pixels_to_microns(*rand_coords, bar_pos=rand_bar_pos)}",
                    delta=0.001
                )
            
            mic_px_mic = uc.micron_to_pixels(
                *uc.pixels_to_microns(*rand_coords, bar_pos=rand_bar_pos),
                bar_pos=rand_bar_pos
            )
            
            # microns to pixels to microns
            for coord1, coord2 in zip(rand_coords, mic_px_mic):
                self.assertAlmostEqual(
                    coord1,
                    coord2,
                    delta=0.001,
                    msg=f"Failed on iteration {i}, random bar pos: {rand_bar_pos}\n"
                        f"micron to pixels: {uc.micron_to_pixels(*rand_coords, bar_pos=rand_bar_pos)}"
                )
    
    def test_pixels_to_nm(self):
        self.assertAlmostEqual(*uc.pixels_to_microns(0), 0.0, delta=0.001)
        
        # 6nm set #14 on the S13 image
        self.assertAlmostEqual(*uc.pixels_to_microns(1232), 0.688, delta=0.001)  # x
        self.assertAlmostEqual(*uc.pixels_to_microns(1150), 0.642, delta=0.001)  # y
        
        # 12nm set #1 for the S15 image
        self.assertAlmostEqual(*uc.pixels_to_microns(1166), 0.651, delta=0.001)  # x
        self.assertAlmostEqual(*uc.pixels_to_microns(878), 0.491, delta=0.001)   # y
        