# PDF to Markdown

A minimalist, cross-platform desktop application that converts PDF documents into clean, structured Markdown files using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) engine and [pywebview](https://pywebview.flowrl.com/).

---

## Highlights

- **Warm Minimalist Aesthetic**: A warm off-white/beige palette (`#f7f5f0`), clean typography, and matte-black buttons.
- **Modern Webview Architecture**: Uses `pywebview` backed by the native Qt6 WebEngine—all HTML, CSS, and JS assets run 100% offline with zero external network dependencies.
- **Smart File Picker**: Launches directly in your user's Home directory and filters strictly for `.pdf` files.
- **Deep Text & Table Extraction**: Uses Microsoft MarkItDown (powered by `pdfminer`, `pdfplumber`, `pypdfium2`, and `magika`) to extract clean text and structured tables into Markdown.
- **Live Progress Indicator**: Smooth indeterminate progress bar and real-time status feedback during processing.
- **Quick Folder Access**: Automatically enables an **Open Folder** button upon completion so you can jump straight to your generated `.md` file.
- **Desktop Launcher Ready**: Includes a 1-command installer script for Linux (`install.sh`) to register the application into your system's application grid (GNOME, KDE) with its custom app icon.

---

## Project Structure

```text
pdf_to_md/
├── pdf_to_md_webview.py   # Application backend and pywebview bridge
├── ui/
│   └── index.html         # Modern, self-contained minimalist web UI
├── assets/
│   └── icon.png           # High-resolution application icon
├── install.sh             # Linux system installer (desktop entry & launcher)
├── uninstall.sh           # Uninstaller script
├── requirements.txt       # Frozen Python dependencies
├── pdf-to-md.spec         # PyInstaller build specification
└── markitdown_source/     # Cloned Microsoft MarkItDown source package
```

---

## Prerequisites

- **Operating System**: Linux (Fedora, Ubuntu, Arch, etc.), Windows 10/11, or macOS.
- **Python Version**: **Python 3.12** is required.  
  *(Note: Microsoft's MarkItDown relies on `magika` and `onnxruntime`, which have strict precompiled wheel compatibility pinned to Python 3.12).*

---

## Getting Started

### 1. Clone & Set Up Virtual Environment

```bash
# Clone the repository
git clone https://github.com/your-username/pdf-to-md.git
cd pdf-to-md

# Create and activate Python 3.12 virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run in Development Mode

```bash
source venv/bin/activate
python pdf_to_md_webview.py
```

---

## Linux System Installation (App List & Launcher)

To install the app on Linux so that it appears in your system application menu (GNOME App Grid, KDE Launcher, etc.) and is executable from anywhere in the terminal:

```bash
./install.sh
```

Once installed, you can:
- Press `Super` (Windows key) and launch **PDF to Markdown** from your applications.
- Run `pdf-to-md` directly from any terminal.

To uninstall:
```bash
./uninstall.sh
```

---

## Building Standalone Executables (PyInstaller)

You can package the application into a standalone distribution that runs on computers without requiring Python.

### Linux
```bash
source venv/bin/activate
pyinstaller --noconfirm --onedir --windowed --name "pdf-to-md" \
  --add-data "ui:ui" \
  --add-data "assets:assets" \
  --collect-all magika \
  --collect-all markitdown \
  --collect-all pdfminer \
  --collect-all onnxruntime \
  --collect-all webview \
  --collect-all PyQt6 \
  pdf_to_md_webview.py
```
The output is generated in `dist/pdf-to-md/`.

### Windows
On a Windows machine running Python 3.12:
```cmd
pip install -r requirements.txt
pyinstaller --noconfirm --onedir --windowed --name "PDFtoMarkdown" ^
  --add-data "ui;ui" ^
  --add-data "assets;assets" ^
  --collect-all magika ^
  --collect-all markitdown ^
  --collect-all pdfminer ^
  --collect-all onnxruntime ^
  --collect-all webview ^
  --collect-all PyQt6 ^
  pdf_to_md_webview.py
```
*(Optional: Use Inno Setup with the generated `dist/PDFtoMarkdown/` directory to create a single `Setup.exe` with a Start Menu shortcut).*

### macOS
On macOS running Python 3.12:
```bash
pip install -r requirements.txt
pyinstaller --noconfirm --windowed --name "PDF to Markdown" \
  --add-data "ui:ui" \
  --add-data "assets:assets" \
  --collect-all magika \
  --collect-all markitdown \
  --collect-all pdfminer \
  --collect-all onnxruntime \
  --collect-all webview \
  --collect-all PyQt6 \
  pdf_to_md_webview.py
```
Generates a `.app` bundle ready to drag into `/Applications`.

---

## Architecture & Technical Notes

1. **Webview Bridge (`pywebview` + Qt6)**:
   The UI communicates with the Python backend via `window.pywebview.api`. File dialogs, file conversions, and folder opening are handled asynchronously through exposed Python methods.
2. **Wayland Compatibility**:
   Qt logging rules are automatically configured on startup (`QT_LOGGING_RULES="qt.qpa.wayland*=false"`) to suppress verbose Wayland text-input debug warnings on modern Linux desktop environments.
3. **Extractable Text Layer**:
   MarkItDown extracts text, formatted headings, and tables from digitally generated PDFs. Scanned, image-only documents require an OCR backend to extract text.

---

## License

This project is open-source under the [MIT License](LICENSE).
Microsoft MarkItDown is licensed under the [MIT License](https://github.com/microsoft/markitdown/blob/main/LICENSE).
