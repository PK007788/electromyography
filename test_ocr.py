import numpy as np
from PIL import Image
from crop_emg_images import to_rgb, try_ocr

def find_title_clusters_raw(arr, thresh=40, cluster_gap=20):
    b = arr[:, :, 2].astype(int)
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    mask   = (b - r > 80) & (b - g > 80) & (b > 80)
    counts = mask.sum(axis=1)
    rows   = np.where(counts >= thresh)[0]

    if not len(rows):
        return []

    raw, start, prev = [], rows[0], rows[0]
    for row in rows[1:]:
        if row - prev > cluster_gap:
            raw.append((start, prev))
            start = row
        prev = row
    raw.append((start, prev))
    return raw

arr = to_rgb(Image.open("data/uncropped images/image.png"))
H = arr.shape[0]
clusters = find_title_clusters_raw(arr)

named = {}
for s, e in clusters:
    top = max(0, s - 10)
    bot = min(H, e + 10)
    d = try_ocr(arr, top, bot)
    print(f"Cluster {s}-{e} (padded {top}-{bot}) -> OCR: {d}")
    if d and d not in named:
        named[d] = (s, e)
        
print("Final named:", named)
