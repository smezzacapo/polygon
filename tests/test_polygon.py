import pytest

from models import const
from models.polygon import Polygon

@pytest.fixture
def coordinates_rectangle_one():
    """
    Coordinates (lat, long) of a simple rectangle
    """
    return (
        (-10, -30),
        (-10, 30),
        (20, 30),
        (20, -30)
    )

@pytest.fixture
def coordinates_rectangle_two():
    """
    Coordinates (lat, long) of a simple rectangle.
    Outside of rectangle_one
    """
    return (
        (40, -60),
        (40, -50),
        (80, -50),
        (80, -60)
    )

def test_polygon_creation(coordinates_rectangle_one):
    """
    Confirm a Polygon object is created with the correct
    x/y min and max values
    """
    poly = Polygon(coordinates_rectangle_one, 'base_file_name', 1)
    assert(poly._min_x == -30)
    assert(poly._max_x == 30)
    assert(poly._min_y == -10)
    assert(poly._max_y == 20)

def test_outside_rectangles(coordinates_rectangle_one, coordinates_rectangle_two):
    """
    Confirm rectangle_two is outside of rectangle_one
    """
    rectangle_one = Polygon(coordinates_rectangle_one, 'base_file_name', 1)
    rectangle_two = Polygon(coordinates_rectangle_two, 'test_file_name', 1)
    assert(const.OUTSIDE == rectangle_one.compare_polygon(rectangle_two))



