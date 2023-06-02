import os
import itertools
import struct
from functools import reduce

def read_binary_file(file_name):
    with open(file_name, 'rb') as f:
        data = f.read()
    return data

def bitwise_xor(data):
    return bytes([reduce(lambda x, y: x ^ y, data)])

def bitwise_and(data):
    return bytes([reduce(lambda x, y: x & y, data)])

def bitwise_or(data):
    return bytes([reduce(lambda x, y: x | y, data)])

def sum_bytes(data):
    return bytes([sum(data) % 256])

def rotate_left(data, num):
    return bytes([(byte << num | byte >> (8 - num)) & 0xff for byte in data])

def apply_operations_and_write_file(operations, data, chunk_size, output_folder, output_file_name, degree=None):
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    result = bytes()
    for chunk in chunks:
        chunk_result = chunk
        for operation in operations:
            if operation == rotate_left and degree is not None:
                chunk_result = operation(chunk_result, degree)
            else:
                chunk_result = operation(chunk_result)
        result += chunk_result

    # Skip writing the file if all bytes in the result are 0
    if all(byte == 0 for byte in result):
        return

    # Skip writing the file if result is identical to input data
    if result == data:
        return

    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, output_file_name), 'wb') as f:
        f.write(result)


if __name__ == "__main__":
    input_file_name = "data17.bin"
    data = read_binary_file(input_file_name)

    operations = [bitwise_and, bitwise_or, bitwise_xor, sum_bytes]
    rotation_degrees = list(range(1, 9))  # Excluding zero rotation
    chunk_sizes = [1, 4, 8]  # Byte chunk sizes

    for chunk_size in chunk_sizes:
        # Padding data with zeros if necessary
        remainder = len(data) % chunk_size
        if remainder > 0:
            data += b'\x00' * (chunk_size - remainder)

        for r in range(1, len(operations) + 1):
            for perm in itertools.permutations(operations, r):
                for degree in rotation_degrees:
                    full_permutations = [[rotate_left] + list(perm), list(perm)]

                    for i, full_perm in enumerate(full_permutations):
                        if full_perm[0] == rotate_left:
                            operation_names = [f"rotate_left_{degree}"] + [op.__name__ for op in full_perm[1:]]
                            rotation_folder = f"rotate_{degree}"
                        else:
                            operation_names = [op.__name__ for op in full_perm]
                            rotation_folder = "rotate_0"
                        operation_str = '_'.join(operation_names)

                        output_folder = os.path.join(str(chunk_size), rotation_folder)
                        output_file_name = f"{operation_str}.bin"

                        print(f"Writing to file: {os.path.join(output_folder, output_file_name)}")
                        apply_operations_and_write_file(full_perm, data, chunk_size, output_folder, output_file_name, degree)
