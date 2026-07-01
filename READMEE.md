# Electromyography Image Cropping

This project contains a small Python toolset for working with EMG/NCS report images. The main script resizes each report to a fixed canvas and crops out six consistent regions for the medianus, ulnaris, and tibialis sections.

## Requirements

- Python 3.10 or newer
- [Pillow](https://python-pillow.org/)
- [NumPy](https://numpy.org/) for the debug scripts

Install the Python dependencies with:

```bash
pip install pillow numpy
```

## Folder Structure

- Put source images in [data/uncropped images](data/uncropped%20images)
- Cropped output images are written to [data/cropped images](data/cropped%20images)

## Usage

Run the main cropping script from the project root:

```bash
python crop_emg_images.py
```

The script will:

- Find supported image files in [data/uncropped images](data/uncropped%20images)
- Resize each image to a fixed canvas size
- Crop six regions from each image
- Save the cropped images under [data/cropped images](data/cropped%20images)

## Output

Each input image produces six cropped PNG files:

- `medianus_left`
- `medianus_right`
- `ulnaris_left`
- `ulnaris_right`
- `tibialis_left`
- `tibialis_right`

The output filenames keep the source image stem and add the side name.

## Configuration

The crop boxes are defined in [crop_emg_images.py](crop_emg_images.py). That file also includes a `USE_PERCENTAGE_CROPS` switch if you later want the crop coordinates to be interpreted as percentages instead of pixels.

## Debug Scripts

The other scripts in the repository are exploratory helpers:

- [debug_density.py](debug_density.py) saves image strips for inspecting boundary rows.
- [test_ocr.py](test_ocr.py) experiments with OCR around detected title clusters.
- [test_ncols.py](test_ncols.py) prints the number of matching columns for detected clusters.
- [writer.py](writer.py) is currently empty.

## Notes

The crop script is deterministic and does not try to detect regions dynamically. If the source reports change layout, the crop coordinates in [crop_emg_images.py](crop_emg_images.py) will need to be updated.