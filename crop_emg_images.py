"""Deterministically crop fixed EMG/NCS graph regions from report images."""

from pathlib import Path
from typing import Dict, Iterable, Tuple

from PIL import Image, ImageOps


BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "data" / "uncropped images"
OUTPUT_DIR = BASE_DIR / "data" / "cropped images"

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}
RESIZED_SIZE = (660, 877)
OUTPUT_FORMAT = "PNG"

# Disabled by default. If enabled, crop coordinates are interpreted as
# percentages from 0.0 to 1.0 relative to RESIZED_SIZE.
USE_PERCENTAGE_CROPS = False

CROP_REGIONS: Dict[str, Tuple[float, float, float, float]] = {
    "medianus_left": (48, 42, 315, 280),
    "medianus_right": (336, 42, 612, 280),
    "ulnaris_left": (48, 318, 315, 560),
    "ulnaris_right": (336, 318, 612, 560),
    "tibialis_left": (48, 595, 315, 820),
    "tibialis_right": (336, 595, 612, 820),
}


def iter_image_paths(input_dir: Path) -> Iterable[Path]:
    """Yield supported image files in a stable order."""
    return sorted(
        path for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def resize_report(image: Image.Image) -> Image.Image:
    """Return an RGB image resized to the fixed report size."""
    image = ImageOps.exif_transpose(image)
    return image.convert("RGB").resize(RESIZED_SIZE, Image.Resampling.LANCZOS)


def crop_box_to_pixels(box: Tuple[float, float, float, float]) -> Tuple[int, int, int, int]:
    """Convert configured crop coordinates to pixels."""
    if not USE_PERCENTAGE_CROPS:
        return tuple(int(round(value)) for value in box)

    width, height = RESIZED_SIZE
    left, top, right, bottom = box
    return (
        int(round(left * width)),
        int(round(top * height)),
        int(round(right * width)),
        int(round(bottom * height)),
    )


def output_path_for(source_path: Path, crop_name: str) -> Path:
    """Build the output path while preserving the source filename stem."""
    nerve, side = crop_name.rsplit("_", 1)
    return OUTPUT_DIR / nerve / f"{source_path.stem}_{side}.png"


def save_fixed_crops(source_path: Path) -> None:
    """Resize one report image and save all six fixed crops."""
    print(f"Processing: {source_path.name}")

    with Image.open(source_path) as image:
        resized = resize_report(image)

    print(f"  Resized to: {RESIZED_SIZE[0]}x{RESIZED_SIZE[1]} px")

    for crop_name, crop_box in CROP_REGIONS.items():
        cropped = resized.crop(crop_box_to_pixels(crop_box))
        out_path = output_path_for(source_path, crop_name)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(out_path, format=OUTPUT_FORMAT)
        print(f"  Saved {crop_name}: {out_path}")


def main() -> None:
    if not INPUT_DIR.exists():
        raise SystemExit(f"ERROR: input folder not found: {INPUT_DIR}")

    image_paths = list(iter_image_paths(INPUT_DIR))
    if not image_paths:
        raise SystemExit(f"No supported images found in: {INPUT_DIR}")

    print(f"Found {len(image_paths)} image(s) in: {INPUT_DIR}")
    print(f"Output folder: {OUTPUT_DIR}")

    failures = 0
    for image_path in image_paths:
        try:
            save_fixed_crops(image_path)
        except Exception as exc:
            failures += 1
            print(f"  ERROR: failed to process {image_path.name}: {exc}")
            print("  Continuing with remaining images.")

    processed = len(image_paths) - failures
    print(f"\nDone. Processed {processed}/{len(image_paths)} image(s).")
    if failures:
        print(f"Failed image(s): {failures}")


if __name__ == "__main__":
    main()