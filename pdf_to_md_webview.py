import sys
import os
import subprocess
from pathlib import Path

# Silence verbose Qt / Wayland chatter in terminal
os.environ.setdefault("QT_LOGGING_RULES", "qt.qpa.wayland*=false;*.debug=false;qt.webenginecontext=false")

import webview
from markitdown import MarkItDown


class BridgeApi:
    def __init__(self):
        self._window = None
        self.last_output_path = None

    def set_window(self, window):
        self._window = window

    def select_file(self):
        if not self._window:
            return None

        # Start from user's home directory and strictly show PDF files only
        home_dir = str(Path.home())
        dialog_mode = getattr(webview.FileDialog, "OPEN", webview.OPEN_DIALOG)

        result = self._window.create_file_dialog(
            dialog_mode,
            directory=home_dir,
            file_types=('PDF Files (*.pdf)',)
        )

        if result and len(result) > 0:
            file_path = Path(result[0])
            if file_path.exists():
                return {
                    "path": str(file_path),
                    "name": file_path.name,
                    "size": file_path.stat().st_size
                }
        return None

    def convert_pdf(self, file_path_str):
        try:
            target_path = Path(file_path_str)
            if not target_path.exists():
                return {"success": False, "error": f"File does not exist: {file_path_str}"}

            md = MarkItDown()
            result = md.convert(str(target_path))

            out_path = target_path.with_suffix(".md")
            out_path.write_text(result.text_content, encoding="utf-8")
            self.last_output_path = out_path

            return {
                "success": True,
                "output_name": out_path.name,
                "output_path": str(out_path),
                "chars": len(result.text_content)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_folder(self, file_path_str=None):
        target = Path(file_path_str) if file_path_str else self.last_output_path
        if not target or not target.exists():
            return False

        folder = target.parent if target.is_file() else target
        try:
            if sys.platform == "win32":
                os.startfile(str(folder))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
            return True
        except Exception:
            return False


def get_resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    else:
        base_dir = Path(__file__).parent
    return base_dir / relative_path


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--convert":
        target = Path(sys.argv[2])
        if not target.exists():
            print(f"File not found: {target}")
            sys.exit(1)
        print(f"Converting {target} ...")
        md = MarkItDown()
        res = md.convert(str(target))
        out = target.with_suffix(".md")
        out.write_text(res.text_content, encoding="utf-8")
        print(f"Successfully converted to {out} (length: {len(res.text_content)} characters)")
        return

    api = BridgeApi()
    html_path = get_resource_path("ui/index.html")

    window = webview.create_window(
        title="PDF to Markdown",
        url=str(html_path.resolve()),
        js_api=api,
        width=540,
        height=400,
        resizable=False,
        text_select=False,
        background_color="#f7f5f0"
    )
    api.set_window(window)
    webview.start(gui="qt")


if __name__ == "__main__":
    main()
