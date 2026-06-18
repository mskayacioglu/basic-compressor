"""Compression algorithm registry used by the desktop application."""

from .huffman import compress_file as compress_huffman
from .huffman import decompress_file as decompress_huffman
from .lossy import compress_file as compress_lossy
from .lossy import decompress_file as decompress_lossy
from .lzw import compress_file as compress_lzw
from .lzw import decompress_file as decompress_lzw
from .shannon_fano import compress_file as compress_shannon_fano
from .shannon_fano import decompress_file as decompress_shannon_fano


ALGORITHMS = {
    "Huffman coding": compress_huffman,
    "Shannon–Fano coding": compress_shannon_fano,
    "LZW": compress_lzw,
    "Lossy text filtering": compress_lossy,
}

DECOMPRESSORS = {
    "Huffman": decompress_huffman,
    "Shannon-Fano": decompress_shannon_fano,
    "LZW": decompress_lzw,
    "Lossy": decompress_lossy,
}

__all__ = ["ALGORITHMS", "DECOMPRESSORS"]
