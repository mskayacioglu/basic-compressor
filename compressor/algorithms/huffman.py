"""Huffman text compression and decompression."""

import ast
import heapq
from collections import defaultdict

from .bitstream import decode_prefix_codes, pack_bits, unpack_bits


class Node:
    def __init__(self, character=None, frequency=0):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def _build_codes(text):
    frequencies = defaultdict(int)
    for character in text:
        frequencies[character] += 1

    heap = [Node(character, frequency) for character, frequency in frequencies.items()]
    heapq.heapify(heap)
    if not heap:
        return {}

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(frequency=left.frequency + right.frequency)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)

    codes = {}

    def visit(node, code):
        if node.character is not None:
            codes[node.character] = code or "0"
            return
        visit(node.left, code + "0")
        visit(node.right, code + "1")

    visit(heap[0], "")
    return codes


def compress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as source:
        text = source.read()

    codes = _build_codes(text)
    encoded = "".join(codes[character] for character in text)
    header = {"method": "Huffman", "codes": codes}

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
