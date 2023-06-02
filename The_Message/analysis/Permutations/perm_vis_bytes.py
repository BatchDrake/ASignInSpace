import os
import numpy as np
from PIL import Image

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# List of image widths to try
powers_of_2 = [2**i for i in range(5, 7)]
primes = [i for i in range(37, 139) if is_prime(i)]
image_widths = powers_of_2 + primes

# Approximation of the Viridis color map
viridis = np.array([
    [0, 0, 0],  # Making 0x00 black
    [71, 18, 100],
    [72, 34, 115],
    [70, 50, 126],
    [64, 65, 131],
    [58, 80, 134],
    [51, 94, 134],
    [43, 108, 131],
    [36, 122, 125],
    [33, 137, 116],
    [44, 153, 104],
    [68, 168, 90],
    [97, 182, 77],
    [127, 194, 66],
    [161, 202, 58],
    [194, 209, 52],
    [224, 214, 46],
    [253, 218, 36],
    [253, 224, 28],
    [253, 231, 36],
    [253, 238, 46],
    [253, 246, 64],
    [255, 255, 255],  # Making 0xFF white
])

# Prepare viridis color map to PIL palette
viridis_palette = list(viridis.ravel()) * int(256 / len(viridis))

chunk_sizes = [1,4,8]

for chunk_size in chunk_sizes:
    path = f"./{chunk_size}"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.bin'):
                # Load binary data
                with open(os.path.join(root, file), 'rb') as f:
                    data = f.read()

                # Convert data to NumPy array
                np_data = np.frombuffer(data, dtype=np.uint8)

                output_dir = os.path.join(root, f"vis/bytes/{file}")

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                for image_width in image_widths:
                    try:
                        # Reshape data
                        image_height = len(np_data) // image_width
                        np_data_resized = np_data[:image_width * image_height]  # Truncate any overflow pixels
                        np_data_resized = np_data_resized.reshape(image_height, image_width)

                        # Create an image object
                        img = Image.fromarray(np_data_resized.astype(np.uint8), 'P')

                        # Apply the Viridis palette
                        img.putpalette(viridis_palette)

                        # Save it as a bmp file
                        img.save(f'{output_dir}/{file}_bytes_{image_width}.bmp')

                    except Exception as e:
                        print(f"Could not reshape and save image for width {image_width}. Error: {e}")
