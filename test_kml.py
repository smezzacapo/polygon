"""
Iterate over all polygons found in KML files in test_kml/
and compare against polygons found in KML files in base_kml/
"""
import logging as log
import os
import sys

# Note - this library is only used to extract coordinates from KML files in _create_polygons(). No other functionality may be leveraged.
from fastkml import kml

from models import const
from models.polygon import Polygon

log.basicConfig(stream=sys.stdout, level=log.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s')


def _get_all_kml_files(directory):
    """
    Get file names of all KML files in directory
    """
    for file in os.listdir(directory):
        if file.endswith(const.KML_EXT):
            yield os.path.join(directory, file)

def _create_polygons(directory):
    """
    Create polygon objects for all KML files in
    directory.
    Return a list of polygon objects
    """
    polygons = []
    for kml_file in _get_all_kml_files(directory):
        with open(kml_file, 'rb') as current_file:
            kml_doc = current_file.read()
            k = kml.KML()
            k.from_string(kml_doc)
            for feature in k.features():
                for inner_feature in feature.features():
                    for i, coordinate_obj in enumerate(inner_feature.features()):
                        try:
                            polygons.append(
                                Polygon(
                                    coordinate_obj.geometry.exterior.coords, kml_file, i
                                )
                            )
                        except Exception:
                            log.exception('Non polygon found - skipping.')
                            continue
    return polygons


def main():
    log.info('Beginning Program.')
    log.info('Creating polygons for all base KML files.')
    base_polygons = _create_polygons(const.BASE_KML_DIR)
    if not base_polygons:
        raise ValueError("No Base Polygons Found - add a KML file to %s" % const.BASE_KML_DIR)
    log.info("Creating polygons for all test KML files")
    test_polygons = _create_polygons(const.TEST_KML_DIR)
    if not test_polygons:
        raise ValueError("No Test Polygons Found - add a KML file to %s" % const.TEST_KML_DIR)
    for test_polygon in test_polygons:
        for base_polygon in base_polygons:
            result = base_polygon.compare_polygon(test_polygon)
            log.info(
                'Test Polygon #%s from %s compared with Base Polygon #%s from %s: Result = %s' % (
                    test_polygon.polygon_number, test_polygon.file_name,
                    base_polygon.polygon_number, base_polygon.file_name,
                    result
                )
            )
    log.info('Finished, good bye!')


if __name__ == "__main__":
    main()