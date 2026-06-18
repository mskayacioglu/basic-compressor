import tempfile
import unittest
from pathlib import Path

from compressor.algorithms.huffman import compress_file as compress_huffman
from compressor.algorithms.huffman import decompress_file as decompress_huffman
from compressor.algorithms.lzw import compress_file as compress_lzw
from compressor.algorithms.lzw import decompress_file as decompress_lzw
from compressor.algorithms.shannon_fano import compress_file as compress_shannon_fano
from compressor.algorithms.shannon_fano import decompress_file as decompress_shannon_fano


LOSSLESS_METHODS = (
    ("Huffman", compress_huffman, decompress_huffman),
    ("Shannon-Fano", compress_shannon_fano, decompress_shannon_fano),
    ("LZW", compress_lzw, decompress_lzw),
)


class CompressionRoundTripTests(unittest.TestCase):
    def test_lossless_algorithms_restore_utf8_text(self):
        self.assert_round_trip("Hello, world!\nÇa va? İstanbul — 你好")

    def test_lossless_algorithms_restore_single_repeated_character(self):
        self.assert_round_trip("x" * 128)

    def test_lossless_algorithms_restore_empty_file(self):
        self.assert_round_trip("")

    def assert_round_trip(self, original):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source.txt"
            source.write_text(original, encoding="utf-8")

            for name, compress, decompress in LOSSLESS_METHODS:
                with self.subTest(algorithm=name):
                    compressed = base / f"{name}.inf365"
                    restored = base / f"{name}.txt"
                    compress(source, compressed)
                    decompress(compressed, restored)
                    self.assertEqual(restored.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
