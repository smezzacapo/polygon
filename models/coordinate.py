class Coordinate():
    """
    x (longitude)
    y (latitude)

    TODO: Current Implementation is an approximation that does not account for the curvature of the earth.
    Need something like this:
    x = r λ cos(φ0)
    y = r φ

    φ0 - latitude near center of shape
    """
    def __init__(self, longitude, latitude):
        self.x = longitude
        self.y = latitude