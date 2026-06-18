# Compressor

A dark-themed desktop application for comparing classic text compression
algorithms. Compressor supports UTF-8 text, reports compression results, and
previews original or restored content in the interface.

## Algorithms

- Huffman coding
- Shannon–Fano coding
- Lempel–Ziv–Welch (LZW)
- Lossy text filtering for demonstration

The first three algorithms are lossless. The lossy method removes vowels and
punctuation and converts the input to lowercase, so it cannot restore the
original text.

## Requirements

- Python 3.9 or newer
- Tkinter

Tkinter is included with most Python distributions. On macOS with Homebrew,
install the package matching your Python version if needed:

```bash
brew install python-tk@3.14
```

On Debian or Ubuntu:

```bash
sudo apt install python3-tk
```

## Run

From the project root:

```bash
python3 -m compressor
```

You can also install the project locally and use the `compressor` command:

```bash
python3 -m pip install -e .
compressor
```

## Test

```bash
python3 -m unittest discover -s tests -v
```

The test suite covers UTF-8 input, empty files, and single-character input for
all lossless algorithms. GitHub Actions runs the same suite on every push and
pull request.

## Project structure

```text
.
├── compressor/
│   ├── __main__.py
│   ├── app.py
│   └── algorithms/
│       ├── bitstream.py
│       ├── huffman.py
│       ├── lossy.py
│       ├── lzw.py
│       └── shannon_fano.py
├── docs/
│   └── report.pdf
├── examples/
├── tests/
├── pyproject.toml
└── README.md
```

## File format

Compressed files use the `.inf365` extension. Each file begins with a small
header identifying the algorithm used. This is an educational file format, not
a secure container; only open files from trusted sources.
