Sample project checking if polygons loaded from test_kml/ are within/outside/intersecting polygons loaded from base_kml/

Algorithm:

1. Iterate over each coordinate per test_kml polygon.
2. If the test coordinate is outside the base polygon's x min/max and y min/max, that test coordinate is marked as False. In other words, it is outside of the base polygon.
3. If the test coordinate is within the base polygon's x min/max and y min/max, then confirm that the test coordinate is bound by base polygon edges on all 4 sides. If the test coordinate is bound on all 4 sides, the test coordinate is marked as True.
   1. Check if the test coordinate is between two base polygon coordinates on the X-axis (upper/lower bound check) or on the Y-axis (left/right bound check).
   2. Calculate the slope between the two base polygon coordinates. Identify the point on the edge formed between the two base polygon coordinates that has the same X-axis value (upper/lower bound) or same Y-axis value (left/right bound) as the test coordinate.
      1. Left Bound: The test coordinate X value is greater than the derived base polygon coordinate's X value.
      2. Right Bound: The test coordinate X value is less than the derived base polygon coordinate's X value.
      3. Upper Bound: The test coordinate Y value is less than the derived base polygon coordinate's Y value
      4. Lower Bound: The test coordinate Y value is greater than the derived base polygon coordinate's Y value.
4. If all test coordinates are True then the test polygon is contained within the base polygon. If all test coordinates are False then the test polygon is outside of the base polygon. If at least one but not all test coordinates are True then the test polygon intersects the base polygon.

Running Manually within Docker:

`docker build -t (imageName) . `

`docker run -dit (imageName)`

`docker exec -it (container id) /bin/bash`

`python test_kml.py`

TODO:

1. Generate better test_kml sample files and test more thoroughly.
2. This does not account for the curvature of the earth and as such is only an approximation. There are formulas for converting between lat/long and x/y that could be leveraged potentially.
3. Github actions to build / push docker image to Dockerhub
4. The case in which a test polygon's coordinates are all within the x/y min/max vaues of the base polygon will fail to recognize intersection if all test coordinates are outside the base polygon. In addition to the bound checks, must add an explicit intersection check.
