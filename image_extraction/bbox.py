import cv2
import numpy as np

from enum import Enum


class BoundingBox:
    class Type(Enum):
        AxisAligned = 1,
        Min = 2

    def __init__(self, contour, type: Type, align_dominant_dimension=True):
        if type == BoundingBox.Type.AxisAligned:
            self.rotated_rect = cv2.minAreaRect(contour)
            self.rect = cv2.boundingRect(contour)
            [x, y, w, h] = self.rect
            self.points = np.float32([[x, y + h], [x, y], [x + w, y], [x + w, y + h]])
            [self.center, self.shape, self.angle] = np.array([x, y]) + np.array([w, h]) // 2, [w, h], 0
        elif type == BoundingBox.Type.Min:
            self.rotated_rect = cv2.minAreaRect(contour)
            self.points = cv2.boxPoints(self.rotated_rect)
            [self.center, self.shape, self.angle] = self.rotated_rect

        # Shift points to match orientation if alignment required
        if align_dominant_dimension and np.argmax(self.shape) == 0:
            self.points = np.roll(self.points, 1, axis=0)
            self.shape = self.shape[::-1]

        [self.width, self.height] = self.shape

    def crop_axis_aligned(self, image, center_crop=True, min_crop_dimension_factor=1):
        # Determine dimension for the aligned bbox, must be divisible by min_crop_dimension_factor
        if min_crop_dimension_factor == 1:
            target_shape = np.int32(np.ceil(self.shape))
        else:
            target_shape = np.int32(min_crop_dimension_factor * np.ceil(np.array(self.shape) / min_crop_dimension_factor))

        # Align target to the top left corner or the center
        if center_crop:
            target_points = cv2.boxPoints((target_shape / 2, self.shape, 0))
        else:
            target_points = np.float32([[0, self.height], [0, 0], [self.width, 0], [self.width, self.height]])

        # Calculate the transformation matrix to allow for bbox warping for extraction
        M = cv2.getPerspectiveTransform(self.points, target_points)
        bbox_crop = cv2.warpPerspective(image, M, tuple(target_shape), flags=cv2.INTER_CUBIC)
        return bbox_crop

    def crop(self, image):
        rect = cv2.boundingRect(self.points)
        [x, y, w, h] = rect
        return image[y:y+h, x:x+w]

    def draw(self, image, color, orientation_color=(0, 0, 255)):
        image = cv2.polylines(image, np.int32([self.points]), True, color, 1, cv2.LINE_AA)
        orientation_vector = tuple(np.int32(np.round(self.center))), tuple(np.int32((self.points[1] + self.points[2]) / 2))
        image = cv2.arrowedLine(image, orientation_vector[0], orientation_vector[1], orientation_color, 1, cv2.LINE_AA)
        return image

def get_bounding_boxes(image, threshold=8, bbox_type=BoundingBox.Type.Min, align=True):
    _, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bboxes = []
    for contour in contours:
        bounding_box = BoundingBox(contour, bbox_type, align)
        bboxes.append(bounding_box)

    return bboxes

def extract_bounding_boxes(image, threshold=8, bbox_type=BoundingBox.Type.Min, align=True, center_bbbox_points=False, min_dimension_factor=1):
    bboxes = get_bounding_boxes(image, threshold, bbox_type, align)
    return [bbox.crop_axis_aligned(image, center_bbbox_points, min_dimension_factor) for bbox in bboxes]
