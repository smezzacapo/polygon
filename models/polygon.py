"""
Class describing the polygon formed by provided KML files
and providing methods to compare coordinates across polygons
"""
import logging as log

from models import const
from models.coordinate import Coordinate


class Polygon():
    def __init__(self, coordinates, file_name, index):
        """
        Polygon class contains all coordinates, min/max x and y values,
        and helper functions for comparing this polygon against another provided
        polygon.
        Coordinates are all (x, y) pairs instead of (lat, long)
        """
        # KML file containing the polygon coordinates
        self.file_name = file_name
        # Some KML files have multiple polygons - keep track of that order here
        self.polygon_number = index
        self.all_coords = []

        self._min_y = 90
        self._max_y = -90

        self._min_x = 180
        self._max_x = -180
        
        self._process_coords(coordinates)

    def _process_coords(self, coordinates):
        """
        Determine min/max for x and y axis.
        Create Coordinate for each lat/long pair
        """
        for geo_tuple in coordinates:
            latitude = geo_tuple[0]
            longitude = geo_tuple[1]
            new_coord = Coordinate(longitude, latitude)
            if latitude > self._max_y:
                self._max_y = latitude
            if latitude < self._min_y:
                self._min_y = latitude
            if longitude > self._max_x:
                self._max_x = longitude
            if longitude < self._min_x:
                self._min_x = longitude
            self.all_coords.append(new_coord)

    def _get_point_by_slope(self, cur_coord, next_coord, x=None, y=None):
        """
        Determine slope between cur_coord and next_coord.

        Identify the point between cur_coord and next_coord that is perpendicular
        to either x or y

        y = mx+b
        """
        # Check for vertical line - undefined slope
        if cur_coord.x-next_coord.x == 0:
            return Coordinate(cur_coord.x, y)
        m = (cur_coord.y-next_coord.y) / (cur_coord.x-next_coord.x)
        b = cur_coord.y
        if x is not None:
            new_y = m * x + b
            return Coordinate(x, new_y)
        if y is not None:
            new_x = (y-b) / m
            return Coordinate(new_x, y)

    def _check_bound(self, coordinate, axis, check_greater_than=True):
        """
        For the provided coordinate, does the polygon have any coordinates
        that bound the provided coordinate above.

        axis: Use y axis for left/right bound. x axis for upper/lower bound
        check_greater_than: True for upper/right bounds. False for lower/left bounds
        """
        for i, cur_coord in enumerate(self.all_coords):
            if i == len(self.all_coords):
                break
            # Final coordinate has a next_coord of the very first coordinate checked
            next_coord = None
            if i == len(self.all_coords) - 1:
                next_coord = self.all_coords[0]
            else:
                next_coord = self.all_coords[i+1]
            if axis == const.Y_AXIS:
                if min(cur_coord.y, next_coord.y) <= coordinate.y <= max(cur_coord.y, next_coord.y):
                    slope_point = self._get_point_by_slope(cur_coord, next_coord, y=coordinate.y)
                    if (check_greater_than and slope_point.x >= coordinate.x) or (not check_greater_than and slope_point.x <= coordinate.x):
                        return True
            elif axis == const.X_AXIS:
                if min(cur_coord.x, next_coord.x) <= coordinate.x <= max(cur_coord.x, next_coord.x):
                    slope_point = self._get_point_by_slope(cur_coord, next_coord, x=coordinate.x)
                    if (check_greater_than and slope_point.y >= coordinate.y) or (not check_greater_than and slope_point.y <= coordinate.y):
                        return True
            else:
                raise ValueError('Invalid axis provided for _check_bound: %s', axis)
        return False


    def _check_coord_bounds(self, coordinate):
        """
        Upper / lower / left / right check
        """
        is_upper = self._check_bound(coordinate, const.X_AXIS, check_greater_than=True)
        if not is_upper:
            return False
        is_lower = self._check_bound(coordinate, const.X_AXIS, check_greater_than=False)
        if not is_lower:
            return False
        is_left = self._check_bound(coordinate, const.Y_AXIS, check_greater_than=False)
        if not is_left:
            return False
        is_right = self._check_bound(coordinate, const.Y_AXIS, check_greater_than=True)
        if not is_right:
            return False
        return True


    def _check_coordinate(self, coordinate):
        """
        Is this coordinate inside / outside self?
        First check the min/max x and y values.
        If inside the appropriate range, then confirm it is bound in all directions

        Return true if the coordinate is within self, else false
        """
        if coordinate.x >= self._min_x and coordinate.x <= self._max_x and coordinate.y >= self._min_y and coordinate.y <= self._max_y:
            return self._check_coord_bounds(coordinate)
        return False


    def compare_polygon(self, polygon):
        """
        Return in/out/intersect

        Iterate over each coordinate to get True/False (true if in, false if out)
        """
        results = []
        for coord in polygon.all_coords:
            results.append(
                self._check_coordinate(coord)
            )
        log.info(results)
        if not results:
            return const.NO_RESULT
        if all(result for result in results):
            return const.INSIDE
        if all(not result for result in results):
            return const.OUTSIDE
        if any(result for result in results):
            return const.INTERSECT
        return const.NO_RESULT