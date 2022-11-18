import math

import numpy as np

from image_extraction.bbox import BoundingBox, extract_bounding_boxes, get_bounding_boxes


def test_bbox_definition():
    bbox = BoundingBox(np.array([
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 1],
    ]), BoundingBox.Type.Min)

    assert bbox.width == 1 and bbox.height == 1
    
    bbox = BoundingBox(np.array([
        [0, 0],
        [1, 1]
    ]), BoundingBox.Type.Min)

    assert bbox.width == 0 and math.isclose(bbox.height, 1.414213562, rel_tol=1e-7)


# TODO: Extend tests to
#     Alignment correctness
#     Input image size limits
#     Random blob generation
#     Multiple iterations
#     Various rotations
#     Limit contour size
#     Large amount of contours
#     Bbox size warp tolerance
#     Speed
