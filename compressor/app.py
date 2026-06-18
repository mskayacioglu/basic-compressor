"""Desktop interface for the INF365 text compression project."""

import ast
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .algorithms import ALGORITHMS, DECOMPRESSORS

COLORS = {
    "background": "#0b0f17",
    "surface": "#131a26",
    "surface_hover": "#1a2332",
    "border": "#263247",
    "text": "#f4f7fb",
    "muted": "#91a0b7",
    "accent": "#5b8cff",
    "accent_hover": "#739dff",
    "accent_pressed": "#4777e6",
    "success": "#4fd1a5",
}


def format_size(size):
    """Return a compact, human-readable byte size."""
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024


class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compressor")
        self.root.geometry("940x680")
        self.root.minsize(760, 580)

        self.algorithm = tk.StringVar(value=next(iter(ALGORITHMS)))
        self.status = tk.StringVar(value="Ready — choose an algorithm and a file.")
        self.metrics = tk.StringVar(value="No operation completed yet")

        self._configure_style()
        self._build_interface()

    def _configure_style(self):
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.root.configure(bg=COLORS["background"])
        self.root.option_add("*TCombobox*Listbox.background", COLORS["surface"])
        self.root.option_add("*TCombobox*Listbox.foreground", COLORS["text"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", COLORS["accent"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

        style.configure("TFrame", background=COLORS["background"])
        style.configure("Surface.TFrame", background=COLORS["surface"])
        style.configure(
            "TLabel",
            background=COLORS["background"],
            foreground=COLORS["text"],
        )
        style.configure(
            "Title.TLabel",
            font=("TkDefaultFont", 26, "bold"),
            foreground=COLORS["text"],
        )
        style.configure(
            "Subtitle.TLabel",
            foreground=COLORS["muted"],
            font=("TkDefaultFont", 11),
        )
        style.configure(
            "Eyebrow.TLabel",
            foreground=COLORS["accent"],
            font=("TkDefaultFont", 9, "bold"),
        )
        style.configure(
            "Surface.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["text"],
        )
        style.configure(
            "SurfaceMuted.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "Metric.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["success"],
            font=("TkDefaultFont", 10, "bold"),
        )
        style.configure(
            "Accent.TButton",
            background=COLORS["accent"],
            foreground="#ffffff",
            bordercolor=COLORS["accent"],
            lightcolor=COLORS["accent"],
            darkcolor=COLORS["accent"],
            font=("TkDefaultFont", 10, "bold"),
            padding=(20, 12),
        )
        style.map(
            "Accent.TButton",
            background=[("pressed", COLORS["accent_pressed"]), ("active", COLORS["accent_hover"])],
            bordercolor=[("pressed", COLORS["accent_pressed"]), ("active", COLORS["accent_hover"])],
        )
        style.configure(
            "Secondary.TButton",
            background=COLORS["surface_hover"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["surface_hover"],
            darkcolor=COLORS["surface_hover"],
            padding=(18, 11),
        )
        style.map(
            "Secondary.TButton",
            background=[("pressed", COLORS["border"]), ("active", COLORS["border"])],
            bordercolor=[("active", COLORS["accent"])],
        )
        style.configure(
            "Ghost.TButton",
            background=COLORS["background"],
            foreground=COLORS["muted"],
            borderwidth=0,
            padding=(10, 7),
        )
        style.map(
            "Ghost.TButton",
            foreground=[("active", COLORS["text"])],
            background=[("active", COLORS["surface_hover"])],
        )
        style.configure(
            "TCombobox",
            fieldbackground=COLORS["surface_hover"],
            background=COLORS["surface_hover"],
            foreground=COLORS["text"],
            arrowcolor=COLORS["muted"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["surface_hover"],
            darkcolor=COLORS["surface_hover"],
            padding=9,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", COLORS["surface_hover"])],
            foreground=[("readonly", COLORS["text"])],
            bordercolor=[("focus", COLORS["accent"])],
        )
        style.configure(
            "Vertical.TScrollbar",
            background=COLORS["surface_hover"],
            troughcolor=COLORS["surface"],
            bordercolor=COLORS["surface"],
            arrowcolor=COLORS["muted"],
        )

    def _build_interface(self):
        container = ttk.Frame(self.root, padding=(38, 30))
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="INF365  /  TEXT COMPRESSION", style="Eyebrow.TLabel").pack(
            anchor=tk.W, pady=(0, 7)
        )
        ttk.Label(container, text="Compressor", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            container,
            text="Compress, restore, and compare text files with classic algorithms.",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(5, 24))

        control_border = tk.Frame(
            container,
            background=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            borderwidth=0,
        )
        control_border.pack(fill=tk.X)
        controls = ttk.Frame(control_border, style="Surface.TFrame", padding=22)
        controls.pack(fill=tk.BOTH, expand=True)

        ttk.Label(controls, text="COMPRESSION ALGORITHM", style="SurfaceMuted.TLabel").grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 7)
        )
        algorithm_choice = ttk.Combobox(
            controls,
            values=list(ALGORITHMS),
            textvariable=self.algorithm,
            state="readonly",
            width=28,
        )
        algorithm_choice.grid(row=1, column=0, sticky=tk.EW, padx=(0, 12))

        ttk.Button(
            controls,
            text="Compress text file",
            command=self.compress_file,
            style="Accent.TButton",
        ).grid(row=1, column=1, padx=(0, 8))
        ttk.Button(
            controls,
            text="Decompress .inf365 file",
            command=self.decompress_file,
            style="Secondary.TButton",
        ).grid(row=1, column=2)
        controls.columnconfigure(0, weight=1)

        ttk.Label(controls, textvariable=self.metrics, style="Metric.TLabel").grid(
            row=2, column=0, columnspan=3, sticky=tk.W, pady=(16, 0)
        )

        preview_header = ttk.Frame(container)
        preview_header.pack(fill=tk.X, pady=(24, 10))
        ttk.Label(preview_header, text="Text preview", font=("TkDefaultFont", 12, "bold")).pack(
            side=tk.LEFT
        )
        ttk.Button(
            preview_header,
            text="Clear preview",
            command=self.clear_preview,
            style="Ghost.TButton",
        ).pack(side=tk.RIGHT)

        preview_border = tk.Frame(
            container,
            background=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            borderwidth=0,
        )
        preview_border.pack(fill=tk.BOTH, expand=True)
        preview_scrollbar = ttk.Scrollbar(preview_border, orient=tk.VERTICAL)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 3), pady=3)
        self.text_preview = tk.Text(
            preview_border,
            wrap=tk.WORD,
            height=16,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            padx=18,
            pady=16,
            font=("TkFixedFont", 11),
            background=COLORS["surface"],
            foreground=COLORS["text"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["accent"],
            selectforeground="#ffffff",
            yscrollcommand=preview_scrollbar.set,
        )
        self.text_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.configure(command=self.text_preview.yview)

        footer = ttk.Frame(container)
        footer.pack(fill=tk.X, pady=(14, 0))
        ttk.Label(footer, textvariable=self.status, style="Subtitle.TLabel").pack(side=tk.LEFT)
        ttk.Button(
            footer,
            text="Exit",
            command=self.root.destroy,
            style="Ghost.TButton",
        ).pack(side=tk.RIGHT)

    def clear_preview(self):
        self.text_preview.delete("1.0", tk.END)
        self.status.set("Preview cleared.")

    def _show_preview(self, path):
        with open(path, "r", encoding="utf-8", errors="replace") as source:
            text = source.read()
        self.text_preview.delete("1.0", tk.END)
        self.text_preview.insert(tk.END, text)

    def compress_file(self):
        input_path = filedialog.askopenfilename(
            title="Choose a text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not input_path:
            return

        algorithm = self.algorithm.get()
        default_output = f"{Path(input_path).stem}.inf365"
        output_path = filedialog.asksaveasfilename(
            title="Save compressed file",
            defaultextension=".inf365",
            initialdir=str(Path(input_path).parent),
            initialfile=default_output,
            filetypes=[("INF365 compressed files", "*.inf365")],
        )
        if not output_path:
            return

        try:
            original_size = os.path.getsize(input_path)
            ALGORITHMS[algorithm](input_path, output_path)
            compressed_size = os.path.getsize(output_path)
            change = (
                f"{100 * (1 - compressed_size / original_size):.1f}% smaller"
                if original_size
                else "empty input"
            )
            self.metrics.set(
                f"Original: {format_size(original_size)}   •   "
                f"Compressed: {format_size(compressed_size)}   •   {change}"
            )
            self._show_preview(input_path)
            self.status.set(f"Compressed with {algorithm}: {Path(output_path).name}")
            messagebox.showinfo("Compression complete", f"Saved to:\n{output_path}")
        except Exception as error:
            messagebox.showerror("Compression failed", str(error))
            self.status.set("Compression failed. See the error message for details.")

    def decompress_file(self):
        input_path = filedialog.askopenfilename(
            title="Choose a compressed file",
            filetypes=[("INF365 compressed files", "*.inf365")],
        )
        if not input_path:
            return

        default_output = f"{Path(input_path).stem}_decompressed.txt"
        output_path = filedialog.asksaveasfilename(
            title="Save decompressed text",
            defaultextension=".txt",
            initialdir=str(Path(input_path).parent),
            initialfile=default_output,
            filetypes=[("Text files", "*.txt")],
        )
        if not output_path:
            return

        try:
            with open(input_path, "rb") as source:
                header = ast.literal_eval(source.readline().decode("utf-8").strip())
            method = header.get("method")
            if method not in DECOMPRESSORS:
                raise ValueError(f"Unsupported compression method: {method!r}")

            DECOMPRESSORS[method](input_path, output_path)
            self._show_preview(output_path)
            output_size = os.path.getsize(output_path)
            self.metrics.set(f"Restored text size: {format_size(output_size)}   •   Method: {method}")
            self.status.set(f"Decompressed: {Path(output_path).name}")
            messagebox.showinfo("Decompression complete", f"Saved to:\n{output_path}")
        except Exception as error:
            messagebox.showerror("Decompression failed", str(error))
            self.status.set("Decompression failed. See the error message for details.")


def main():
    root = tk.Tk()
    CompressionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
