import sys
import os
import subprocess
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from markitdown import MarkItDown

# Set modern appearance: matches system light/dark mode
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class PDFToMarkdownApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("PDF to Markdown")
        self.root.geometry("560x340")
        self.root.minsize(520, 320)

        # Center on screen
        self._center_window(560, 340)

        # State
        self.selected_path: Path | None = None
        self.last_output_path: Path | None = None
        self.is_processing = False

        # Load icon if available
        self._load_icon()

        # Build UI
        self._build_ui()

    def _center_window(self, width: int, height: int):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _load_icon(self):
        icon_path = Path(__file__).parent / "assets" / "icon.png"
        if icon_path.exists():
            try:
                icon_img = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(False, icon_img)
            except Exception:
                pass

    def _build_ui(self):
        # Main padding container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=24, pady=20)

        # Header
        lbl_title = ctk.CTkLabel(
            main_frame,
            text="PDF to Markdown",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_title.pack(anchor="w", pady=(0, 2))

        lbl_sub = ctk.CTkLabel(
            main_frame,
            text="Extract clean Markdown documents powered by Microsoft MarkItDown",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        lbl_sub.pack(anchor="w", pady=(0, 18))

        # File selection card
        file_card = ctk.CTkFrame(main_frame, corner_radius=10)
        file_card.pack(fill="x", pady=(0, 16), padx=2)

        file_inner = ctk.CTkFrame(file_card, fg_color="transparent")
        file_inner.pack(fill="x", padx=12, pady=12)

        self.file_var = tk.StringVar(value="")
        self.entry_file = ctk.CTkEntry(
            file_inner,
            textvariable=self.file_var,
            placeholder_text="No PDF file selected...",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            state="readonly"
        )
        self.entry_file.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_browse = ctk.CTkButton(
            file_inner,
            text="Choose PDF...",
            height=38,
            width=120,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.choose_pdf
        )
        self.btn_browse.pack(side="right")

        # Action buttons row
        action_row = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_row.pack(fill="x", pady=(0, 14))

        self.btn_convert = ctk.CTkButton(
            action_row,
            text="Convert to Markdown",
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.process_pdf
        )
        self.btn_convert.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_open_folder = ctk.CTkButton(
            action_row,
            text="Open Folder",
            height=42,
            width=120,
            corner_radius=8,
            state="disabled",
            fg_color="transparent",
            border_width=1,
            font=ctk.CTkFont(size=12),
            command=self.open_output_folder
        )
        self.btn_open_folder.pack(side="right")

        # Progress bar
        self.progress = ctk.CTkProgressBar(main_frame, height=6, corner_radius=3)
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress.set(0)

        # Status text
        self.status_var = tk.StringVar(value="Ready. Choose a PDF file to begin.")
        self.lbl_status = ctk.CTkLabel(
            main_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
            anchor="w",
            wraplength=510
        )
        self.lbl_status.pack(fill="x")

    def choose_pdf(self):
        if self.is_processing:
            return

        initial_dir = self.selected_path.parent if self.selected_path else Path.home()
        file_path_str = filedialog.askopenfilename(
            title="Select a PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialdir=str(initial_dir)
        )
        if file_path_str:
            self.selected_path = Path(file_path_str)
            self.file_var.set(str(self.selected_path))
            self.status_var.set(f"Selected: {self.selected_path.name}")
            self.lbl_status.configure(text_color=("gray30", "gray80"))

    def process_pdf(self):
        if self.is_processing:
            return

        # If user hasn't picked a file yet, open file picker directly
        if not self.selected_path or not self.selected_path.exists():
            self.choose_pdf()
            if not self.selected_path or not self.selected_path.exists():
                return

        # Start background processing thread
        self._set_ui_processing_state(True)
        threading.Thread(target=self._convert_worker, daemon=True).start()

    def _convert_worker(self):
        try:
            target_path = self.selected_path
            self._update_status(f"Converting: {target_path.name} ...", ("#2563eb", "#38bdf8"))

            md = MarkItDown()
            result = md.convert(str(target_path))

            out_path = target_path.with_suffix(".md")
            out_path.write_text(result.text_content, encoding="utf-8")

            self.last_output_path = out_path
            success_msg = f"Done! Saved: {out_path.name}"
            self.root.after(0, lambda: self._on_conversion_success(success_msg))

        except Exception as e:
            err_msg = str(e)
            self.root.after(0, lambda: self._on_conversion_error(err_msg))

    def _on_conversion_success(self, message: str):
        self._set_ui_processing_state(False)
        self.status_var.set(message)
        self.lbl_status.configure(text_color=("#16a34a", "#4ade80"))  # Green
        self.progress.set(1.0)
        self.btn_open_folder.configure(state="normal")

    def _on_conversion_error(self, err_text: str):
        self._set_ui_processing_state(False)
        self.status_var.set("Conversion failed. See alert for details.")
        self.lbl_status.configure(text_color=("#dc2626", "#f87171"))  # Red
        self.progress.set(0)
        messagebox.showerror("Conversion Failed", f"An error occurred:\n{err_text}")

    def _update_status(self, text: str, text_color):
        def _apply():
            self.status_var.set(text)
            self.lbl_status.configure(text_color=text_color)
        self.root.after(0, _apply)

    def _set_ui_processing_state(self, processing: bool):
        def _apply():
            self.is_processing = processing
            if processing:
                self.btn_convert.configure(state="disabled", text="Converting...")
                self.btn_browse.configure(state="disabled")
                self.btn_open_folder.configure(state="disabled")
                self.progress.configure(mode="indeterminate")
                self.progress.start()
            else:
                self.btn_convert.configure(state="normal", text="Convert to Markdown")
                self.btn_browse.configure(state="normal")
                self.progress.stop()
                self.progress.configure(mode="determinate")

        if threading.current_thread() is threading.main_thread():
            _apply()
        else:
            self.root.after(0, _apply)

    def open_output_folder(self):
        if not self.last_output_path or not self.last_output_path.exists():
            return
        folder = self.last_output_path.parent
        try:
            if sys.platform == "win32":
                os.startfile(str(folder))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except Exception as e:
            messagebox.showwarning("Notice", f"Could not open directory:\n{e}")


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

    root = ctk.CTk()
    app = PDFToMarkdownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
