"""Shannon–Fano text compression and decompression."""

import ast
from collections import defaultdict

from .bitstream import decode_prefix_codes, pack_bits, unpack_bits


class Symbol:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.code = ""


def _assign_codes(symbols):
    if len(symbols) <= 1:
        return

    total = sum(symbol.frequency for symbol in symbols)
    accumulated = 0
    split_index = 0
    for index, symbol in enumerate(symbols):
        accumulated += symbol.frequency
        if accumulated >= total / 2:
            split_index = index + 1
            break

    for symbol in symbols[:split_index]:
        symbol.code += "0"
    for symbol in symbols[split_index:]:
        symbol.code += "1"

    _assign_codes(symbols[:split_index])
    _assign_codes(symbols[split_index:])


def _build_codes(text):
    frequencies = defaultdict(int)
    for character in text:
        frequencies[character] += 1

    symbols = [
        Symbol(character, frequency)
        for character, frequency in sorted(frequencies.items(), key=lambda item: -item[1])
    ]
    _assign_codes(symbols)
    return {symbol.character: symbol.code or "0" for symbol in symbols}


def compress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as source:
        text = source.read()

    codes = _build_codes(text)
    encoded = "".join(codes[character] for character in text)
    header = {"method": "Shannon-Fano", "codes": codes}

    with open(output_path, "wb") as target:
        target.write((str(header) + "\n").encode("utf-8"))
        target.write(pack_bits(encoded))


def decompress_file(input_path, output_path):
    with open(input_path, "rb") as source:
        header = ast.literal_eval(source.readline().decode("utf-8").strip())
        encoded = unpack_bits(source.read())

    text = decode_prefix_codes(encoded, header["codes"])
    with open(output_path, "w", encoding="utf-8") as target:
        target.write(text)
