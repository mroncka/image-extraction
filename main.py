import os
import shutil
import click

import cv2

from image_extraction.bbox import BoundingBox, get_bounding_boxes


def recreate_output_directory(directory):
    try:
        shutil.rmtree(directory)
    except Exception:
        print("Unable to remove existing results folder")

    os.makedirs(directory, exist_ok=True)

@click.command()
@click.option("-i", "--input", "input", default="assignment/RS_homework_BB.png", prompt="Input image path", help="Image for bbox extraction.")
@click.option("-o", "--output", default="output", prompt="Output directory", help="Directory to store extracted bbox images.")
@click.option("-t", "--threshold", default=4, help="Image intensity threshold used to extract contours.")
@click.option("-a", "--align", default=True, help="Align the bbox with the dominant dimension.")
@click.option("-f", "--min_factor", default=1, help="Bounding box dimension will be divisible by specified value.")
@click.option("-c", "--center", default=False, help="Center bbox around the contour.", is_flag=True)
@click.option("-v", "--visual", default=False, help="Input image and bounding box visualization.", is_flag=True)
def extract_bboxes(input, output, threshold, align, center, min_factor, visual):
    if not os.path.exists(input):
        raise Exception(f"File {input} is not accessible or doesn't exist")

    image = cv2.imread(input, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise Exception("Input image is empty")

    bbox_type = BoundingBox.Type.Min
    bboxes = get_bounding_boxes(image, threshold, bbox_type, align)

    output_directory = f"{output}/{os.path.basename(input)}"
    recreate_output_directory(output_directory)
    
    for i, bbox in enumerate(bboxes):
        crop = bbox.crop_axis_aligned(image, center, min_factor)
        cv2.imwrite(f"{output_directory}/contour_{i}.png", crop)

    if visual:
        color = (0, 255, 0)
        visual = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        for i, bbox in enumerate(bboxes):
            visual = bbox.draw(visual, color)
            crop = bbox.crop_axis_aligned(image, center, min_factor)
            cv2.imshow(f"crop_{i}", crop)

        cv2.imshow("visual", visual)
        cv2.waitKey(0)


if __name__ == "__main__":
    extract_bboxes()
