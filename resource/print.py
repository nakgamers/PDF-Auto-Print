import os
import sys
import subprocess
import threading
import tkinter as tk

from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

import win32print

# =========================================================
# BASE DIRECTORY FIX (WORKS FOR EXE & PYTHON)
# =========================================================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================================
# PORTABLE SUMATRA PDF
# =========================================================
SUMATRA_PATH = os.path.join(BASE_DIR, "SumatraPDF.exe")

if not os.path.exists(SUMATRA_PATH):
    raise Exception("SumatraPDF.exe tidak ditemukan!")

# =========================================================
# MAIN APP
# =========================================================
class PrintApp:

    def __init__(self, root):

        self.root = root

        # =========================
        # WINDOW
        # =========================
        root.title("Nandz PDF Auto Print")
        root.geometry("900x650")
        root.configure(bg="#0f172a")

        # =========================
        # STYLE
        # =========================
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TProgressbar",
            thickness=18
        )

        # =========================
        # TITLE
        # =========================
        title = tk.Label(
            root,
            text="NANDZ PDF AUTO PRINT",
            font=("Segoe UI", 22, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            root,
            text="Automation PDF Batch Printing Tool",
            font=("Segoe UI", 10),
            fg="white",
            bg="#0f172a"
        )
        subtitle.pack()

        # =========================
        # FOLDER BUTTON
        # =========================
        self.folder_path = tk.StringVar()

        folder_btn = tk.Button(
            root,
            text="📁 Pilih Folder PDF",
            command=self.select_folder,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        folder_btn.pack(pady=20)

        self.folder_label = tk.Label(
            root,
            text="Belum memilih folder",
            fg="#cbd5e1",
            bg="#0f172a",
            font=("Segoe UI", 9)
        )
        self.folder_label.pack()

        # =========================
        # PRINTER DROPDOWN
        # =========================
        printer_frame = tk.Frame(root, bg="#0f172a")
        printer_frame.pack(pady=20)

        printer_label = tk.Label(
            printer_frame,
            text="🖨 Pilih Printer:",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#0f172a"
        )
        printer_label.pack(side="left", padx=5)

        self.printers = self.get_printers()

        self.selected_printer = tk.StringVar()

        if self.printers:
            self.selected_printer.set(self.printers[0])

        self.printer_dropdown = ttk.Combobox(
            printer_frame,
            textvariable=self.selected_printer,
            values=self.printers,
            width=50,
            state="readonly"
        )
        self.printer_dropdown.pack(side="left", padx=5)

        # =========================
        # PRINT BUTTON
        # =========================
        self.print_btn = tk.Button(
            root,
            text="🖨 PRINT SEMUA PDF",
            command=self.start_printing,
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        self.print_btn.pack(pady=10)

        # =========================
        # PROGRESS BAR
        # =========================
        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress.pack(pady=20)

        # =========================
        # LOG BOX
        # =========================
        self.log_box = ScrolledText(
            root,
            width=110,
            height=18,
            bg="#020617",
            fg="#38bdf8",
            insertbackground="white",
            font=("Consolas", 9)
        )
        self.log_box.pack(padx=20, pady=10)

        self.log("🚀 Nandz PDF Auto Print Started")

    # =========================================================
    # GET INSTALLED PRINTERS
    # =========================================================
    def get_printers(self):

        printers = []

        for printer in win32print.EnumPrinters(2):
            printers.append(printer[2])

        return printers

    # =========================================================
    # LOGGING
    # =========================================================
    def log(self, text):

        now = datetime.now().strftime("%H:%M:%S")

        self.log_box.insert(
            tk.END,
            f"[{now}] {text}\n"
        )

        self.log_box.see(tk.END)

    # =========================================================
    # SELECT FOLDER
    # =========================================================
    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.folder_path.set(folder)

            self.folder_label.config(
                text=folder
            )

            self.log(f"📂 Folder dipilih: {folder}")

    # =========================================================
    # START THREAD
    # =========================================================
    def start_printing(self):

        if not self.folder_path.get():

            messagebox.showwarning(
                "Warning",
                "Pilih folder PDF terlebih dahulu!"
            )

            return

        threading.Thread(
            target=self.print_all_pdfs,
            daemon=True
        ).start()

    # =========================================================
    # PRINT ALL PDF
    # =========================================================
    def print_all_pdfs(self):

        folder = self.folder_path.get()

        pdf_files = [
            f for f in os.listdir(folder)
            if f.lower().endswith(".pdf")
        ]

        total = len(pdf_files)

        if total == 0:

            messagebox.showinfo(
                "Info",
                "Tidak ada file PDF!"
            )

            return

        self.progress["maximum"] = total

        printer_name = self.selected_printer.get()

        self.log(f"🖨 Printer: {printer_name}")
        self.log(f"📄 Total PDF: {total}")

        self.print_btn.config(state="disabled")

        for index, pdf in enumerate(pdf_files, start=1):

            pdf_path = os.path.join(folder, pdf)

            try:

                self.log(f"🖨 Printing: {pdf}")

                subprocess.run([
                    SUMATRA_PATH,
                    "-print-to",
                    printer_name,
                    "-silent",
                    pdf_path
                ], check=True)

                self.log(f"✅ Success: {pdf}")

            except Exception as e:

                self.log(f"❌ Error: {pdf} | {e}")

            self.progress["value"] = index

            self.root.update_idletasks()

        self.log("🎉 PRINT SEMUA SELESAI!")

        messagebox.showinfo(
            "Selesai",
            "Semua PDF berhasil diproses!"
        )

        self.print_btn.config(state="normal")

# =========================================================
# RUN APP
# =========================================================
root = tk.Tk()

app = PrintApp(root)

root.mainloop()