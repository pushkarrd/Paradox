NOISE_RANGES = [
    (0x10, 0x18),
]


def is_noise(offset):
    return any(start <= offset <= end for start, end in NOISE_RANGES)


def compare_binaries(path_a, path_b):
    with open(path_a, "rb") as handle_a:
        data_a = handle_a.read()

    with open(path_b, "rb") as handle_b:
        data_b = handle_b.read()

    diffs = []
    compare_length = min(len(data_a), len(data_b))

    for index in range(compare_length):
        if data_a[index] == data_b[index] or is_noise(index):
            continue

        diffs.append(
            {
                "offset": hex(index),
                "suspect_byte": hex(data_a[index]),
                "trusted_byte": hex(data_b[index]),
            }
        )

    size_delta = len(data_a) - len(data_b)
    return diffs, size_delta
