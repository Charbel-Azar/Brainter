from PIL import Image
import svgwrite
import numpy as np
import cv2
import os


def vectorization(input_folder, output_folder, line_spacing=1, line_thickness=1):
    """
    Process all images in the specified input folder, converting them to SVG format with dense lines
    within shape fills using contour detection, and save the results in the output folder.

    Parameters:
    - input_folder: Path to the folder containing the input images.
    - output_folder: Path to the folder where the SVG files will be saved.
    - line_spacing: The spacing between lines used to fill the shapes.
    - line_thickness: The thickness of the lines used to fill the shapes.
    """

    def process_image(image_path, svg_path, line_spacing=1, line_thickness=1):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        height, width = img.shape[:2]
        dwg = svgwrite.Drawing(svg_path, profile="tiny", size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="black"))

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            for line_y in range(y, y + h, line_spacing):
                for line_x in range(x, x + w, line_spacing):
                    if cv2.pointPolygonTest(contour, (line_x, line_y), False) >= 0:
                        line_start = (line_x, line_y)
                        line_end = (line_x + line_spacing, line_y)
                        dwg.add(
                            dwg.line(
                                start=line_start,
                                end=line_end,
                                stroke="white",
                                stroke_width=line_thickness,
                            )
                        )

        dwg.save()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            svg_filename = os.path.splitext(filename)[0] + ".svg"
            svg_path = os.path.join(output_folder, svg_filename)
            process_image(image_path, svg_path)
            print(f"Processed {filename} into {svg_filename}")


# # Example usage
# input_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Segmented Images/img_5"
# output_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Vectorized Images/img_5_contour"
# vectorization(input_folder, output_folder)
