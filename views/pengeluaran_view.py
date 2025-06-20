from tkinter import filedialog
import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.pengeluaran import Pengeluaran
from controllers.pengeluaran_controller import PengeluaranController

class PengeluaranApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg_color = "#eef5f9"
        self.fg_color = "#2d3436"
        self.entry_bg = "#ffffff"
        self.button_bg = "#0984e3"
        self.button_hover = "#74b9ff"
        self.header_bg = "#0984e3"
        self.header_fg = "white"

        self.configure(bg=self.bg_color)
        self.controller = PengeluaranController()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="white",
                        foreground=self.fg_color,
                        rowheight=25,
                        fieldbackground="white",
                        font=('Segoe UI', 10))
        style.map("Treeview",
                  background=[('selected', self.button_bg)],
                  foreground=[('selected', 'white')])
        style.configure("Treeview.Heading",
                        background=self.header_bg,
                        foreground=self.header_fg,
                        font=('Segoe UI', 10, 'bold'))

        judul = tk.Label(self, text="Manajemen Pengeluaran", font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.fg_color)
        judul.pack(pady=(10, 15))

        frame_input = tk.LabelFrame(self, text="Form Pengeluaran", font=("Segoe UI", 12, "bold"), bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill="x")

        labels = ["Kode Pengeluaran", "Tanggal", "Kategori", "Deskripsi", "Jumlah", "Dibuat Oleh", "Bukti"]
        self.entries = {}
        kategori_display = ["Pilih Kategori", "Peralatan", "Kebersihan", "Keamanan", "Internet", "Gaji", "Darurat"]

        for i, label_text in enumerate(labels):
            label = tk.Label(frame_input, text=label_text, font=("Segoe UI", 10), bg=self.entry_bg, anchor="w")
            label.grid(row=i, column=0, sticky="w", pady=7, padx=10)

            if label_text == "Tanggal":
                entry = DateEntry(frame_input, date_pattern="yyyy-mm-dd", state="readonly")
            elif label_text == "Kategori":
                entry = ttk.Combobox(frame_input, values=kategori_display, state="readonly")
                entry.set("Pilih Kategori")
            elif label_text == "Bukti":
                bukti_frame = tk.Frame(frame_input, bg=self.entry_bg)
                entry = tk.Label(bukti_frame, text="Belum ada file", bg=self.entry_bg)
                entry.pack(side="left", padx=(0, 10))
                btn_upload = tk.Button(bukti_frame, text="Pilih File", command=self.upload_file)
                btn_upload.pack(side="left")
                bukti_frame.grid(row=i, column=1, sticky="w", pady=5)
                self.entries[label_text.lower().replace(" ", "_")] = entry
                continue
            else:
                entry = tk.Entry(frame_input)

            entry.grid(row=i, column=1, sticky="ew", pady=5)
            self.entries[label_text.lower().replace(" ", "_")] = entry

        frame_input.columnconfigure(1, weight=1)

        frame_btn = tk.Frame(self, bg=self.bg_color)
        frame_btn.pack(fill="x", pady=(0, 10), padx=(0, 17))
        frame_btn.grid_columnconfigure(0, weight=1)

        self.btn_add = tk.Button(
            frame_btn, text="Tambah", bg="#27ae60", fg="white", activebackground="#2ecc71",
            font=("Segoe UI", 10, "bold"), command=self.tambah_pengeluaran
        )
        self.btn_update = tk.Button(
            frame_btn, text="Update", bg="#2980b9", fg="white", activebackground="#3498db",
            font=("Segoe UI", 10, "bold"), command=self.update_pengeluaran
        )
        self.btn_hapus = tk.Button(
            frame_btn, text="Hapus", bg="#e74c3c", fg="white", activebackground="#3498db",
            font=("Segoe UI", 10, "bold"), command=self.hapus_pengeluaran
        )
        self.btn_clear = tk.Button(
            frame_btn, text="Clear", bg="#7f8c8d", fg="white", activebackground="#95a5a6",
            font=("Segoe UI", 10, "bold"), command=self.clear_form
        )

        self.btn_add.grid(row=0, column=1, padx=5)
        self.btn_update.grid(row=0, column=2, padx=5)
        self.btn_hapus.grid(row=0, column=3, padx=5)
        self.btn_clear.grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self, columns=("kd", "tgl", "kategori", "desc", "jumlah", "by", "bukti"), show='headings')
        self.tree.pack(padx=20, pady=(0, 10), fill="both", expand=True)

        headings = ["Kode", "Tanggal", "Kategori", "Deskripsi", "Jumlah", "Dibuat Oleh", "Bukti"]
        for i, col in enumerate(self.tree["columns"]):
            self.tree.heading(col, text=headings[i])
            self.tree.column(col, width=100, anchor="center")
        self.preview_label = tk.Label(self, bg=self.bg_color)
        self.preview_label.pack(pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.generate_kode_otomatis()
        self.load_data()

    def generate_kode_otomatis(self):
        kode = self.controller.generate_kode_pengeluaran()
        self.entries['kode_pengeluaran'].insert(0, kode)
        self.entries['kode_pengeluaran'].config(state='disabled')

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Bukti Foto",
            filetypes=[("Gambar", "*.jpg *.jpeg *.png *.bmp")]
        )

        if file_path:
            from datetime import datetime
            import uuid

            ext = os.path.splitext(file_path)[1]
            new_filename = f"{uuid.uuid4().hex}{ext}"

            date_folder = datetime.now().strftime("%Y-%m-%d")
            dest_dir = os.path.join("image", "uploads", date_folder)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, new_filename)
            try:
                shutil.copy(file_path, dest_path)
                relative_path = os.path.relpath(dest_path, start="image")
                saved_path = os.path.join("image", relative_path)
                self.entries['bukti'].config(text=saved_path)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengupload file: {e}")

    def tambah_pengeluaran(self):
        data = {key: widget.get() if isinstance(widget, (tk.Entry, ttk.Combobox, DateEntry)) else widget.cget("text")
                for key, widget in self.entries.items()}
        if not data['tanggal'] or data['kategori'] == "Pilih Kategori" or not data['deskripsi'] or not data['jumlah'] or not data['dibuat_oleh'] or data['bukti'] == "Belum ada file":
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi dan kategori harus dipilih!")
            return
        try:
            data['jumlah'] = int(data['jumlah'])
        except ValueError:
            messagebox.showwarning("Peringatan", "Jumlah harus berupa angka!")
            return

        data['kd_pengeluaran'] = data.pop('kode_pengeluaran')
        pengeluaran = Pengeluaran(**data)
        self.controller.tambah_pengeluaran(pengeluaran)
        messagebox.showinfo("Sukses", "Pengeluaran berhasil ditambahkan.")
        self.load_data()
        self.clear_form()

    def update_pengeluaran(self):
        data = {key: widget.get() if isinstance(widget, (tk.Entry, ttk.Combobox, DateEntry)) else widget.cget("text")
                for key, widget in self.entries.items()}

        if not data['kd_pengeluaran']:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diupdate!")
            return

        if not data['tanggal'] or data['kategori'] == "Pilih Kategori" or not data['deskripsi'] or not data['jumlah'] or not data['dibuat_oleh'] or data['bukti'] == "Belum ada file":
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi dan kategori harus dipilih!")
            return

        try:
            data['jumlah'] = int(data['jumlah'])
        except ValueError:
            messagebox.showwarning("Peringatan", "Jumlah harus berupa angka!")
            return

        data['kd_pengeluaran'] = data.pop('kode_pengeluaran')
        pengeluaran = Pengeluaran(**data)
        self.controller.update_pengeluaran(pengeluaran)
        messagebox.showinfo("Sukses", "Pengeluaran berhasil diupdate.")
        self.load_data()
        self.clear_form()

    def hapus_pengeluaran(self):
        kd = self.entries['kode_pengeluaran'].get().strip()
        kategori = self.entries['kategori'].get().strip()
        if not kd:
            messagebox.showwarning("Peringatan", "Pilih pengeluaran yang akan dihapus!")
            return

        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus pengeluaran {kategori}?")
        if confirm:
            bukti_path = self.entries['bukti'].cget("text")
            if os.path.exists(bukti_path) and os.path.isfile(bukti_path):
                try:
                    os.remove(bukti_path)
                    print(f"Bukti gambar {bukti_path} berhasil dihapus.")
                except Exception as e:
                    print(f"Gagal menghapus file bukti: {e}")
            self.controller.hapus_pengeluaran(kd)
            messagebox.showinfo("Sukses", f"Pengeluaran {kategori} berhasil dihapus.")
            self.load_data()
            self.clear_form()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for pengeluaran in self.controller.fetch_pengeluaran():
            self.tree.insert('', 'end', values=(
                pengeluaran.kd_pengeluaran,
                pengeluaran.tanggal,
                pengeluaran.kategori,
                pengeluaran.deskripsi,
                pengeluaran.jumlah,
                pengeluaran.dibuat_oleh,
                pengeluaran.bukti
            ))

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            keys = ['kode_pengeluaran', 'tanggal', 'kategori', 'deskripsi', 'jumlah', 'dibuat_oleh', 'bukti']
            for key, value in zip(keys, values):
                widget = self.entries[key]
                if isinstance(widget, (tk.Entry, DateEntry)):
                    widget.config(state='normal')
                    widget.delete(0, 'end')
                    widget.insert(0, value)
                    if key == 'kode_pengeluaran':
                        widget.config(state='disabled')
                elif isinstance(widget, ttk.Combobox):
                    widget.set(value.capitalize())
                elif isinstance(widget, tk.Label):
                    if key == 'bukti' and value != "Belum ada file":
                        widget.config(text="")
                        from PIL import Image, ImageTk
                        try:
                            img = Image.open(value)
                            img.thumbnail((100, 100))
                            img = ImageTk.PhotoImage(img)
                            widget.config(image=img)
                            widget.image = img
                        except Exception as e:
                            widget.config(text="Gagal load gambar", image='', compound='center')
                    else:
                        widget.config(text=value, image='')
                        widget.image = None

    def clear_form(self):
        self.entries['kode_pengeluaran'].config(state='normal')

        for key, ent in self.entries.items():
            if isinstance(ent, (ttk.Entry, tk.Entry, DateEntry)):
                ent.delete(0, 'end')
            elif isinstance(ent, ttk.Combobox):
                ent.set("Pilih Kategori")
            elif isinstance(ent, tk.Label) and key == 'bukti':
                ent.config(text="Belum ada file", image='')
                ent.image = None

        self.tree.selection_remove(self.tree.selection())
        self.generate_kode_otomatis()
        self.entries['kode_pengeluaran'].config(state='disabled')