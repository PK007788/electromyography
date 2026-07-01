import numpy as np
from PIL import Image
from crop_emg_images import to_rgb, find_title_clusters

def find_title_clusters_raw(arr, thresh=40, cluster_gap=20):
    b = arr[:, :, 2].astype(int)
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    mask   = (b - r > 80) & (b - g > 80) & (b > 80)
    counts = mask.sum(axis=1)
    rows   = np.where(counts >= thresh)[0]

    raw, start, prev = [], rows[0], rows[0]
    for row in rows[1:]:
        if row - prev > cluster_gap:
            raw.append((start, prev))
            start = row
        prev = row
    raw.append((start, prev))
    return raw, mask

arr = to_rgb(Image.open("data/uncropped images/image.png"))
raw_clusters, mask = find_title_clusters_raw(arr)

for s, e in raw_clusters:
    ncols = mask[s:e+1, :].any(axis=0).sum()
    print(f"Cluster {s}-{e}: ncols = {ncols}")
