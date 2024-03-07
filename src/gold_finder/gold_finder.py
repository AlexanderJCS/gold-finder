import sys

from PIL import Image

import numpy as np


class GoldFinder:
    def __init__(self, image: Image, mask_threshold: float = 0.4, circle_threshold: float = 0.25, min_pixels: int = 5):
        """
        
        :param image: The image (which only has a luminosity channel) to analyze
        :param mask_threshold: The threshold to color a pixel white instead of black (e.g., 0.1 means luminosity < 25.5)
        :param circle_threshold: The percentage of points that must be within the inscribed circle for the splotch to be
                            considered a circle
        :param min_pixels: The minimum number of pixels for a splotch to be considered a gold particle
        """
        
        self.image = image
        
        self.mask_threshold = mask_threshold
        self.circle_threshold = circle_threshold
        self.min_pixels = min_pixels
        self.processed_coords = set()
    
    def find_gold(self) -> list[tuple[int, int]]:
        """
        :return: A list of coordinates of the gold particles, in pixels
        """
        
        masked = self.mask_on_luminosity()
        bool_array = np.array(masked.getdata()).reshape(masked.size[::-1])
        
        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(1000000)  # big number for the next function, which is recursive
        
        circle_coords = self.find_circles(bool_array)
        
        sys.setrecursionlimit(original_recursion_limit)
        
        # flip the x and y for some reason
        return [(coord[1], coord[0]) for coord in circle_coords]
        
    def mask_on_luminosity(self) -> Image:
        return self.image.point(lambda p: p < 255 * self.mask_threshold, mode="1")
    
    @staticmethod
    def get_all_splotch_coords(
            image_data: np.array,
            coords: tuple[int, int],
            splotch_coords: set | None = None) \
            -> set[tuple[int, int]]:
        """
        Returns all coordinates of a splotch

        :param image_data: The image gold_finder
        :param coords: A coordinate that is on the splotch
        :param splotch_coords: A set of coordinates that are already known to be part of the splotch
        :return: A list of coordinates that are part of the splotch
        """
        
        if not image_data[*coords]:
            return set()  # not sure how this will happen, but it's a good idea to check for it
        
        if splotch_coords is None:
            splotch_coords = set()
        
        splotch_coords.add(coords)
        
        for offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_coords = (coords[0] + offset[0], coords[1] + offset[1])
            
            coords_out_of_bounds = (new_coords[0] < 0 or new_coords[0] >= image_data.shape[0]
                                    or new_coords[1] < 0 or new_coords[1] >= image_data.shape[1])
            
            # Check now to prevent is_white throwing a key error
            if coords_out_of_bounds:
                continue
            
            not_already_in_splotch = new_coords not in splotch_coords
            is_white = image_data[*new_coords]
            
            if not_already_in_splotch and is_white:
                splotch_coords.update(GoldFinder.get_all_splotch_coords(image_data, new_coords, splotch_coords))
        
        return splotch_coords
    
    @staticmethod
    def get_perimeter_coords(splotch_coords: set[tuple[int, int]]) -> set[tuple[int, int]]:
        """
        Returns the coordinates of the perimeter of the splotch

        :param splotch_coords: A set of coordinates that are part of the splotch
        :return: A set of coordinates that are part of the perimeter of the splotch
        """
        
        perimeter_coords = set()
        
        for coord in splotch_coords:
            for offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                new_coords = (coord[0] + offset[0], coord[1] + offset[1])
                
                # You can also check for black pixels here - might be faster.
                # Only employ this optimization if you run into performance issues
                if new_coords not in splotch_coords:
                    perimeter_coords.add(coord)
                    break
        
        return perimeter_coords
    
    def analyze_splotch(self, image_data: np.array, coords: tuple[int, int]) \
            -> tuple[bool, tuple[int, int]]:
        """
        :param image_data: The image gold_finder
        :param coords: A coordinate that is on the splotch
        :return: [if it is a circle, center of the splotch]
        """
        
        splotch_coords = self.get_all_splotch_coords(image_data, coords)
        
        if len(splotch_coords) < self.min_pixels:
            return False, coords
        
        splotch_center = (sum(coord[0] for coord in splotch_coords) // len(splotch_coords),
                          sum(coord[1] for coord in splotch_coords) // len(splotch_coords))
        
        if not image_data[*splotch_center]:
            return False, splotch_center
        
        perimeter_coords = self.get_perimeter_coords(splotch_coords)
        self.processed_coords.update(splotch_coords)  # optimization that prevents analyzing the same splotch twice
        
        # Find the closest distance from the perimeter coords to splotch center
        incircle_rad_squared = float("inf")
        for coord in perimeter_coords:
            dist_squared = (coord[0] - splotch_center[0]) ** 2 + (coord[1] - splotch_center[1]) ** 2
            
            if dist_squared < incircle_rad_squared:
                incircle_rad_squared = dist_squared
        
        # Find the percentage of points that are within the circle
        num_points_in_circle = 0
        for coord in splotch_coords:
            if (coord[0] - splotch_center[0]) ** 2 + (coord[1] - splotch_center[1]) ** 2 <= incircle_rad_squared:
                num_points_in_circle += 1
        
        circle_score = num_points_in_circle / len(splotch_coords)
        
        return circle_score > self.circle_threshold, splotch_center
    
    def find_circles(self, image_data: np.array) -> list[tuple[int, int]]:
        splotch_centers = []
        
        for x in range(image_data.shape[0]):
            for y in range(image_data.shape[1]):
                if not image_data[x, y] or (x, y) in self.processed_coords:
                    continue
                
                is_gold, coords = self.analyze_splotch(image_data, (x, y))
                
                if is_gold:
                    splotch_centers.append(coords)
        
        return splotch_centers
