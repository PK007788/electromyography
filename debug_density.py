"""Debug: exact content at boundary rows."""
import numpy as np
from PIL import Image

img = np.array(Image.open("data/uncropped images/image.png").convert("RGB"), dtype=np.uint8)

# Save exact boundary rows
for row_range, name in [(250, 285, "medianus_bottom"), (283, 310, "ulnaris_start")]:
    strip = Image.fromarray(img[row_range:name])
    strip.save(f"debug_{name}.png")

# Actually let me do it properly
strip1 = Image.fromarray(img[250:283])
strip1.save("debug_medianus_bottom.png")
print("Saved rows 250-282 as debug_medianus_bottom.png")

strip2 = Image.fromarray(img[283:320])
strip2.save("debug_ulnaris_start.png")  
print("Saved rows 283-319 as debug_ulnaris_start.png")

# Also check: what does the left half of rows 250-282 look like?
strip3 = Image.fromarray(img[250:283, :392])
strip3.save("debug_medianus_bottom_left.png")
print("Saved rows 250-282, cols 0-392 as debug_medianus_bottom_left.png")
