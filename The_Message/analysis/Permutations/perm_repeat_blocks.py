import os
import csv

block_sizes = range(3, 17)

def find_repeating_blocks(filename, block_size):
    block_counts = {}
    block_offsets = {}
    with open(filename, "rb") as file:
        data = file.read()
        for i in range(len(data) - block_size):
            block = data[i:i+block_size]
            if block in block_counts:
                block_counts[block] += 1
                block_offsets[block].append(i)
            else:
                block_counts[block] = 1
                block_offsets[block] = [i]
    return {block: {"count": block_counts[block], "offsets": block_offsets[block]} for block in block_counts if block_counts[block] > 1}

chunk_sizes = [1, 4, 8]

for chunk_size in chunk_sizes:
    path = f"./{chunk_size}"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.bin'):
                for block_size in block_sizes:
                    repeating_blocks = find_repeating_blocks(os.path.join(root, file), block_size)
                    # Exclude sequences that start or end with zeros
                    repeating_blocks = {block: info for block, info in repeating_blocks.items() if block[0] != 0 and block[-1] != 0}
                    if repeating_blocks:
                        output_dir = os.path.join(root, "stats")
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        with open(f'{output_dir}/{block_size}_byte_repeats_{file}_.csv', 'w', newline='') as csvfile:
                            fieldnames = ['block', 'count', 'offsets']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

                            writer.writeheader()
                            for block, info in repeating_blocks.items():
                                writer.writerow({
                                    'block': ' '.join(f'{i:02x}' for i in block),
                                    'count': info['count'],
                                    'offsets': str(info['offsets'])
                                })
