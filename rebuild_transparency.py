#!/usr/bin/env python3
"""
Image Transparency Restoration Tool

This script is designed for converting images with a white background into images with transparent backgrounds,
preserving the original transparency and edge details. It's particularly useful for images where the edges blend into a
white background due to anti-aliasing. This scenario often results in unwanted outlines or halos when the image is
placed on non-white backgrounds. By calculating and applying the original transparency levels, this tool enables
seamless integration of the image over various backgrounds without the common gray outline issue, making it perfect for
graphics and logos that were rendered against white but now need to be used in more versatile contexts.

How to Use This Tool:
1. First, select the white background of the flattened image, ensuring to expand the selection slightly less than
   halfway through any outlines or encompassing all anti-aliased edges. This step is crucial for accurately targeting
   the areas where transparency needs to be restored.
2. Remove (cut) this selected area to create a separate image for processing. This leaves you with an image where the
   original aliasing and background are removed, ready for the transparency restoration process.
3. Running the script then calculates and restores the original transparency, based on the principle that darker colors
   near the edges were once blending with the white background.
4. Use the output image, with its restored transparency, to overlay onto the image from which the background and
   aliasing have been removed. This step reintegrates the anti-aliased, partially transparent edges so that the image
   can be used with different backgrounds.

This process requires manual selection and preparation of the image to ensure the transparency is accurately restored,
specifically tailored for images against a white background, inferring transparency from the intensity of pixel colors.

Dependencies:
- Python 3
- Pillow library

To Run:
python3 rebuild_transparency.py <input_image_path> <output_image_path>
"""

from PIL import Image
import sys
import os


EPSILON_HALF = 0.5 - sys.float_info.epsilon

def calculate_transparency(r, g, b):
    """Calculates the original color and transparency of a pixel that was anti-aliased against a white background.

    This function reverses the effect of flattening an anti-aliased image with a white background. It uses the minimum
    of the R, G, B values to calculate the alpha transparency, assuming that the closer a color is to white, the more
    it was originally blended with white, hence more transparent. The calculated alpha value reflects how much the
    original color was diluted with white. The original RGB values are then recalculated by reversing the blending
    process using the computed alpha. (`EPSILON_HALF` is used to ensure accurate rounding in the restoration process.)

    Args:
        r (int): The red component of the pixel
        g (int): The green component of the pixel
        b (int): The blue component of the pixel

    Returns:
        tuple: A tuple of (R, G, B, alpha) representing the original color and transparency
    """

    alpha = 255 - min(r, g, b)
    if alpha == 0:
        return (0, 0, 0, 0)
    ratio = alpha / 255
    new_r = int((r - (1 - ratio) * 255) / (ratio) + EPSILON_HALF)
    new_g = int((g - (1 - ratio) * 255) / (ratio) + EPSILON_HALF)
    new_b = int((b - (1 - ratio) * 255) / (ratio) + EPSILON_HALF)
    return (new_r, new_g, new_b, alpha)


def convert_image_to_transparent(input_file, output_file):
    """Converts an image into a version with a transparent background, assuming it was anti-aliased against white.

    This function processes an input image to calculate its original color and transparency before it was merged onto a
    white background. It warns if the image already contains transparency data, which will not be taken into account.

    Args:
        input_file (str): Path to the input image file
        output_file (str): Path for the output image with restored transparency
    """

    with Image.open(input_file) as img:
        # Check if the image has an alpha channel
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            print("Warning: Transparency data found in the image will not be used in the conversion.")

        # Process the image in RGB mode
        rgb_img = img.convert("RGB")
        pixels = list(calculate_transparency(*rgb) for rgb in rgb_img.getdata())

        # Build and save the new image
        transparent_img = Image.new("RGBA", img.size)
        transparent_img.putdata(pixels)
        transparent_img.save(output_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {os.path.basename(__file__)} <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_image_to_transparent(input_file, output_file)
    print("Conversion completed. Output saved as:", output_file)
