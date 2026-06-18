"""UTF-8 aware LZW text compression and decompression."""

import ast


MAX_DICTIONARY_SIZE = 65536


def _compress(text):
    data = text.encode("utf-8")
    dictionary = {bytes([value]): value for value in range(256)}
    next_code = 256
    current = b""
    compressed = []

    for value in data:
        character = bytes([value])
        candidate = current + character
        if candidate in dictionary:
            current = candidate
            continue

        compressed.append(dictionary[current])
        if next_code < MAX_DICTIONARY_SIZE:
            dictionary[candidate] = next_code
            next_code += 1
        current = character

    if current:
        compressed.append(dictionary[current])
    return compressed


def _decompress(compressed):
    if not compressed:
        return ""

    dictionary = {value: bytes([value]) for value in range(256)}
    next_code = 256
    current = dictionary[compressed[0]]
    result = [current]

    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current + current[:1]
        else:
            raise ValueError("Invalid LZW stream: dictionary entry not found.")

        result.append(entry)
        if next_code < MAX_DICTIONARY_SIZE:
            dictionary[next_code] = current + entry[:1]
            next_code += 1
        current = entry

    return b"".join(result).decode("utf-8")


def compress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as source:
        text = source.read()

    with open(output_path, "wb") as target:
        target.write((str({"method": "LZW"}) + "\n").encode("utf-8"))
        for code in _compress(text):
            target.write(code.to_bytes(2, byteorder="big"))


def decompress_file(input_path, output_path):
    with open(input_path, "rb") as source:
        ast.literal_eval(source.readline().decode("utf-8").strip())
        byte_data = source.read()

    if len(byte_data) % 2:
        raise ValueError("Invalid LZW stream length.")
    compressed = [
        int.from_bytes(byte_data[index : index + 2], byteorder="big")
        for index in range(0, len(byte_data), 2)
    ]
    with open(output_path, "w", encoding="utf-8") as target:
        target.write(_decompress(compressed))
