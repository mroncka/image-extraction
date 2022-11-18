import click

import cv2
import numpy as np

from image_extraction.bbox import BoundingBox, extract_bounding_boxes, get_bounding_boxes


def extract_visual(image, visual_layer, threshold=8, bbox_type=BoundingBox.Type.Min, align=True, center_bbbox_points=False, min_dimension_factor=1):
    bboxes = get_bounding_boxes(image, threshold, bbox_type, align)

    color = (0, 255, 0)
    visual = cv2.cvtColor(visual_layer, cv2.COLOR_GRAY2BGR)
    for bbox in bboxes:
        visual = bbox.draw(visual, color)

    return visual, [bbox.crop_axis_aligned(visual_layer, center_bbbox_points, min_dimension_factor) for bbox in bboxes]

@click.group()
def examples():
    pass

@examples.command("min")
def example_min():
    image = cv2.imread("assignment/RS_homework_BB.png", cv2.IMREAD_GRAYSCALE)
    bboxes = extract_bounding_boxes(image)
    for i, bbox in enumerate(bboxes):
        cv2.imshow(f"{i}", bbox)

    cv2.waitKey(0)

@examples.command("visual")
def example_visual():
    image = cv2.imread("assignment/RS_homework_BB.png", cv2.IMREAD_GRAYSCALE)
    bboxes = get_bounding_boxes(image)

    color = (0, 255, 0)
    visual = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for bbox in bboxes:
        visual = bbox.draw(visual, color)

    cv2.imshow("visual", visual)
    cv2.waitKey(0)

@examples.command("rotation")
def example_rotation():
    for angle in range(0, 360, 1):
        image = cv2.imread("assignment/RS_homework_BB.png", cv2.IMREAD_GRAYSCALE)
        center = tuple(np.array(image.shape) // 2)
        threshold = np.median(image)

        rotation_matrix = cv2.getRotationMatrix2D(center[::-1], angle, 1)
        image = cv2.warpAffine(image, rotation_matrix, (0, 0))
        _, mask = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

        visual, bboxes = extract_visual(image, mask, threshold)
        bboxes = sorted(bboxes, key=lambda x: np.count_nonzero(x))
        for i, bbox in enumerate(bboxes):
            cv2.imshow(f"{i}", bbox)

        cv2.imshow("visual", visual)
        cv2.waitKey(0)


if __name__ == "__main__":
    examples()
