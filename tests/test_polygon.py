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

@pytest.fixture
def coordinates_rectangle_three():
    """
    Coordinates (lat, long) of a simple rectangle.
    Inside rectangle_one, outside rectangle_two
    """
    return (
        (-5, -25),
        (-5, 25),
        (15, 25),
        (15, -25)
    )

@pytest.fixture
def coordinates_rectangle_four():
    """
    Coordinates (lat, long) of a simple rectangle
    Intersects rectangle_one
    """
    return (
        (-30, 20),
        (-30, 40),
        (0, 40),
        (0, -20)
    )

@pytest.fixture
def coordinates_rectangle_five():
    """
    Coordinates (lat, long) of a simple rectangle.
    Intersects rectangle_one WITHOUT having any coordinates
    contained within rectangle_one
    """
    return (
        (-20, -10),
        (-20, 10),
        (30, 10),
        (30, -10)
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

def test_outside_rectangles(coordinates_rectangle_one, coordinates_rectangle_two, coordinates_rectangle_three):
    """
    Confirm rectangle_two is outside of rectangle_one
    """
    rectangle_one = Polygon(coordinates_rectangle_one, 'base_file_name', 1)
    rectangle_two = Polygon(coordinates_rectangle_two, 'test_file_name', 1)
    rectangle_three = Polygon(coordinates_rectangle_three, 'test_file_name', 2)
    assert(const.OUTSIDE == rectangle_one.compare_polygon(rectangle_two))
    assert(const.OUTSIDE == rectangle_two.compare_polygon(rectangle_three)) 

def test_inside_rectangles(coordinates_rectangle_one, coordinates_rectangle_three):
    rectangle_one = Polygon(coordinates_rectangle_one, 'base_file_name', 1)
    rectangle_three = Polygon(coordinates_rectangle_three, 'test_file_name', 1)    
    assert(const.INSIDE == rectangle_one.compare_polygon(rectangle_three))

def test_intersection_rectangles(coordinates_rectangle_one, coordinates_rectangle_four, coordinates_rectangle_five):
    """
    Test intersection between two rectangles.
    Condition 1: Test Rectangle has at least 1 coordinate within Base Rectangle
    Condition 2: Test Rectangle has no coordinate within Base Rectangle
    """
    rectangle_one = Polygon(coordinates_rectangle_one, 'base_file_name', 1)
    rectangle_four = Polygon(coordinates_rectangle_four, 'test_file_name', 1)
    rectangle_five = Polygon(coordinates_rectangle_five, 'test_file_name', 2)
    assert(const.INTERSECT == rectangle_one.compare_polygon(rectangle_four))
    assert(const.INTERSECT == rectangle_one.compare_polygon(rectangle_five))



