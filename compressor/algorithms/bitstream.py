"""Shared helpers for prefix-code bit streams."""


def pack_bits(encoded_text):
    padding = 8 - len(encoded_text) % 8
    padded_text = f"{padding:08b}" + encoded_text + "0" * padding
    return bytearray(
        int(padded_text[index : index + 8], 2)
        for index in range(0, len(padded_text), 8)
    )


def unpack_bits(byte_data):
    bit_string = "".join(f"{byte:08b}" for byte in byte_data)
    padding = int(bit_string[:8], 2)
    return bit_string[8:-padding] if padding else bit_string[8:]


def decode_prefix_codes(encoded_text, codes):
    reverse_codes = {code: character for character, code in codes.items()}
    current_code = ""
    decoded = []

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded.append(reverse_codes[current_code])
            current_code = ""

    if current_code:
        raise ValueError("Invalid prefix-code stream.")
    return "".join(decoded)
