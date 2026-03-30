import os

# Known noise regions (ignore these offsets)
NOISE_RANGES = [
    (0x10, 0x18),  # ELF timestamp area (basic filtering)
]


def is_noise(offset):
    return any(start <= offset <= end for start, end in NOISE_RANGES)


def compare_binaries(path_a, path_b):
    # Read both files as binary
    with open(path_a, "rb") as f:
        data_a = f.read()

    with open(path_b, "rb") as f:
        data_b = f.read()

    diffs = []

    # Compare byte-by-byte
    for i in range(min(len(data_a), len(data_b))):
        byte_a = data_a[i]
        byte_b = data_b[i]

        if byte_a != byte_b and not is_noise(i):
            diffs.append({
                "offset": hex(i),
                "suspect_byte": hex(byte_a),
                "trusted_byte": hex(byte_b)
            })

    # Calculate size difference
    size_delta = len(data_a) - len(data_b)

    return diffs, size_delta