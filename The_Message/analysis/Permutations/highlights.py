import os
import shutil
import re

def closest(lst, K):
    """Return the value in the list closest to the target value"""
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

chunk_sizes = [1,4,8]
target_ratios = [1, 1.61803398875]  # square and golden ratio

# Ensure output directory exists
if not os.path.exists('highlights'):
    os.makedirs('highlights')

for chunk_size in chunk_sizes:
    path = f"./{chunk_size}"
    for root, dirs, files in os.walk(path):
        for target_ratio in target_ratios:
            closest_diff = float("inf")
            closest_file = None
            match = re.search(r'rotate_(\d+)', root)
            if not match:
                print(f"Unexpected directory structure at {root}, skipping")
                continue
            rotation_degree = match.group(1)
            try:
                color_map = root.split('\\')[4]  # 'bits' or 'bytes'
                bin_file_name = root.split('\\')[-1]
            except IndexError:
                print(f"Unexpected directory structure at {root}, skipping")
                continue

            for file in files:
                if file.endswith('.bmp'):
                    # Extract width from filename
                    width = int(re.findall(r'(\d+).bmp$', file)[0])

                    # Calculate image height from file size (note: this may vary depending on image file format)
                    image_height = os.path.getsize(os.path.join(root, file)) // width

                    # Calculate aspect ratio
                    aspect_ratio = width / image_height

                    # Calculate the difference from target ratios
                    diff = abs(aspect_ratio - target_ratio)

                    # If it's the closest one yet, store the filename
                    if diff < closest_diff:
                        closest_file = file
                        closest_diff = diff

            # Copy to highlights, prepending directory structure to filename to keep unique
            if closest_file:
                new_file_name = f'{chunk_size}_{rotation_degree}_{color_map}_{bin_file_name}_{closest_file.split("_")[-1]}'
                print(f"Copying {os.path.join(root, closest_file)} to highlights/{new_file_name}")
                shutil.copy2(os.path.join(root, closest_file), f'highlights/{new_file_name}')
