# WhiteToAlpha

**WhiteToAlpha** is an image processing tool designed to convert images with white backgrounds into images with transparent backgrounds, preserving the original transparency and edge details. This is particularly useful for images where the edges blend into a white background due to anti-aliasing, making them suitable for use over various backgrounds without the common gray outline issue. It's ideal for graphics, logos, and any image rendered against a white backdrop that needs to be used in more versatile contexts.

## How To Use

The tool works best with manual selection and preparation of the image to target areas where transparency needs to be restored. It calculates the original transparency based on the principle that darker colors near the edges were once blending with the white background. The output is an image with restored transparency that can be overlayed onto any background seamlessly.

### Steps:

1. **Select the Background**: Select the white background of the image and expand the selection slightly less than halfway through any outlines to encompass all anti&#8209;aliased edges accurately.
2. **Prepare the Image**: Remove (cut) the selected area to create a separate image for processing. This step involves leaving behind the areas without the original aliasing and background, making them ready for transparency restoration.
3. **Run the Script**: Execute the script to calculate and restore the original transparency based on the intensity of pixel colors near the edges.
4. **Utilize the Output Image**: The output is an image with restored transparency. Overlay this on the image from which the background and aliasing have been removed.

## Installation

Ensure you have Python 3 and the Pillow library installed. Pillow can be installed using pip:

```sh
pip install pillow
```

## Usage

To use the tool, run the script from the command line with the input and output image paths:

```sh
python3 rebuild_transparency.py <input_image_path> <output_image_path>
```

## Dependencies

- Python 3
- Pillow library

## License

This project is open source and available under the [MIT License](LICENSE).
