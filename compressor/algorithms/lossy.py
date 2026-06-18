"""Demonstrative lossy text filtering."""

import string


def compress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as source:
        text = source.read()

    vowels = "aeiouAEIOU"
    filtered = "".join(
        character
        for character in text.lower()
        if character not in vowels and character not in string.punctuation
    )

    with open(output_path, "w", encoding="utf-8") as target:
        target.write(str({"method": "Lossy"}) + "\n")
        target.write(filtered)


def decompress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as source:
        source.readline()
        compressed = source.read()

    message = "[Lossy compression: the original data cannot be restored]\n"
    with open(output_path, "w", encoding="utf-8") as target:
        target.write(message + compressed)
