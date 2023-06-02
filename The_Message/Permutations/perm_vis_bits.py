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
powers_of_2 = [2**i for i in range(6, 9)]
primes = [i for i in range(59, 258) if is_prime(i)]
image_widths = powers_of_2 + primes

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
                np_data = np.unpackbits(np.frombuffer(data, dtype=np.uint8))

                output_dir = os.path.join(root, f"vis/bits/{file}")

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                for image_width in image_widths:
                    try:
                        # Reshape data
                        image_height = len(np_data) // image_width
                        np_data_resized = np_data[:image_width * image_height]  # Truncate any overflow bits
                        np_data_resized = np_data_resized.reshape(image_height, image_width)

                        # Multiply by 255 to get black (0) and white (255) pixels
                        np_data_resized = np_data_resized * 255

                        # Create an image object and save it as a bmp file
                        img = Image.fromarray(np_data_resized.astype(np.uint8))
                        img.save(f'{output_dir}/{file}_bits_{image_width}.bmp')

                    except Exception as e:
                        print(f"Could not reshape and save image for width {image_width}. Error: {e}")
