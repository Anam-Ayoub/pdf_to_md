# PDF to Markdown

A modern, simple cross-platform desktop application powered by Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). Select any PDF, click convert, and it produces a clean `.md` document in the same directory.

---

## Features

- **Modern Desktop UI**: Dark/Light mode support matching your system theme, rounded controls, and clean typography.
- **Background Multithreading**: Thread-safe background execution so the UI never locks up during heavy document parsing.
- **Progress Feedback**: Real-time progress bar and status indicator.
- **Convenient Output Access**: Quick "Open Folder" button enabled directly upon conversion.
- **System App List Integration**: Includes an installer script to register the app in your desktop launcher (GNOME, KDE, etc.) with its icon.

---

## Quick Start (Development)

Activate the Python 3.12 virtual environment and run the script:

```bash
source venv/bin/activate
python pdf_to_md.py
```

---

## Install to System App List (Linux)

To install the app so you can launch it directly from your PC's application grid / search launcher:

```bash
./install.sh
```

To remove it later:

```bash
./uninstall.sh
```

---

## Building Standalone Packages (Cross-Platform)

### Linux
The project includes a pre-configured PyInstaller build:

```bash
source venv/bin/activate
pyinstaller --noconfirm --onedir --windowed --name "pdf-to-md" \
  --add-data "assets:assets" \
  --collect-all magika \
  --collect-all markitdown \
  --collect-all pdfminer \
  --collect-all onnxruntime \
  --collect-all customtkinter \
  pdf_to_md.py
```
The output is generated in `dist/pdf-to-md/`.

### Windows
On a Windows machine with Python 3.12:
```cmd
pip install -r requirements.txt
pyinstaller --noconfirm --onedir --windowed --name "PDFtoMarkdown" ^
  --add-data "assets;assets" ^
  --collect-all magika ^
  --collect-all markitdown ^
  --collect-all pdfminer ^
  --collect-all onnxruntime ^
  --collect-all customtkinter ^
  pdf_to_md.py
```
*(Optional: Use Inno Setup with the generated `dist/PDFtoMarkdown/` folder to produce a single `Setup.exe` that adds a Start Menu shortcut.)*

### macOS
On macOS with Python 3.12:
```bash
pyinstaller --noconfirm --windowed --name "PDF to Markdown" --add-data "assets:assets" pdf_to_md.py
```
Generates a `.app` bundle that can be dropped into `/Applications`.

---

## Architecture & Requirements

- **Python 3.12 Strictly Required:** `markitdown` relies on `magika`, which depends on `onnxruntime`. Pre-compiled wheels for newer Python versions (such as 3.15) are not yet available on all platforms.
- **Text Layer Prerequisite:** The PDF engine extracts digital text and structured tables. Scanned, image-only PDFs without an OCR engine will produce an empty markdown document.
