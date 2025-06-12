import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import pandas as pd
from app_desktop.models.fasilitas import Fasilitas
from app_desktop.controllers.fasilitas_controller import FasilitasController

class FasilitasApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg_color = "#f0f4f8"
        self.fg_color = "#2c3e50"
        self.entry_bg = "#ffffff"
        self.button_bg = "#3498db"
        self.button_hover = "#2980b9"
        self.header_bg = "#3498db"
        self.header_fg = "white"

        self.configure(bg=self.bg_color)
        self.controller = FasilitasController()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="white",
                        foreground=self.fg_color,
                        rowheight=25,
                        fieldbackground="white",
                        font=('Segoe UI', 10))
        style.map("Treeview", background=[('selected', '#2980b9')], foreground=[('selected', 'white')])

        style.configure("Treeview.Heading",
                        background=self.header_bg,
                        foreground=self.header_fg,
                        font=('Segoe UI', 10, 'bold'))

        judul = tk.Label(self, text="Manajemen Fasilitas", font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.fg_color)
        judul.pack(pady=(10, 15))

        frame_input = tk.LabelFrame(self, text="Form Fasilitas", font=("Segoe UI", 12, "bold"), bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill=tk.X)

        labels = ["Kode Fasilitas", "Nama", "Status"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            lbl = tk.Label(frame_input, text=label_text, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.fg_color)
            lbl.grid(row=i, column=0, sticky="w", pady=6)

            key = label_text.lower().replace(" ", "_")

            if key == "status":
                self.status_var = tk.StringVar()  # Tambahkan kurung
                status_frame = tk.Frame(frame_input, bg=self.entry_bg)
                status_frame.grid(row=i, column=1, pady=6, padx=(5, 0), sticky="w")

                rb_a = tk.Radiobutton(status_frame, text="Aktif", variable=self.status_var, value="aktif",
                                      bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_n = tk.Radiobutton(status_frame, text="Non-Aktif", variable=self.status_var, value="nonaktif",
                                      bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_a.pack(side="left", padx=5)
                rb_n.pack(side="left", padx=5)

                self.entries[key] = self.status_var  # Simpan variabel status
            else:
                ent = ttk.Entry(frame_input, width=40)
                ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[key] = ent  # FIX: simpan entry ke dict

        frame_buttons = tk.Frame(frame_input, bg=self.entry_bg)
        frame_buttons.grid(row=0, column=2, rowspan=5, padx=15)

        self.btn_add = tk.Button(frame_buttons, text="Tambah", command=self.tambah_fasilitas, fg="white", bg="#4CAF50")
        self.btn_update = tk.Button(frame_buttons, text="Update", command=self.update_fasilitas, fg="white", bg="#2196F3")
        self.btn_delete = tk.Button(frame_buttons, text="Hapus", command=self.hapus_fasilitas, fg="white", bg="#f44336")
        self.btn_clear = tk.Button(frame_buttons, text="Clear", command=self.clear_form, fg="white", bg="#9E9E9E")

        self.btn_add.pack(fill='x', pady=4)
        self.btn_update.pack(fill='x', pady=4)
        self.btn_delete.pack(fill='x', pady=4)
        self.btn_clear.pack(fill='x', pady=4)

        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5, 10))

        lbl_search = tk.Label(frame_search, text="🔍 Cari Fasilitas:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color)
        lbl_search.pack(side='left', padx=(0, 5))

        self.entry_search = ttk.Entry(frame_search, width=30)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_search.bind("<KeyRelease>", self.cari_fasilitas)

        btn_reset = ttk.Button(frame_search, text="Reset", command=self.load_data)
        btn_reset.pack(side='left')

        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kd_fasilitas", "nama", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        header_names = ["Kode Fasilitas", "Nama", "Status"]
        for col, header in zip(columns, header_names):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=120, anchor='center')

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.generate_kode_otomatis()
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        fasilitas_list = self.controller.fetch_fasilitas()
        for fasilitas in fasilitas_list:
            self.tree.insert('', 'end', values=(
                fasilitas.kd_fasilitas,
                fasilitas.nama,
                fasilitas.status
            ))

    def tambah_fasilitas(self):
        kd = self.entries['kode_fasilitas'].get()
        nama = self.entries['nama'].get().strip()
        status = self.entries['status'].get()

        if not nama:
            messagebox.showwarning("Peringatan", "Nama fasilitas wajib diisi!")
            return
        elif not status:
            messagebox.showwarning("Peringatan", "Pilih status fasilitas!")

        fasilitas = Fasilitas(kd, nama, status,)
        self.controller.tambah_fasilitas(fasilitas)
        messagebox.showinfo("Sukses", f"Berhasil menambahkan fasilitas {nama}.")
        self.load_data()
        self.clear_form()

    def update_fasilitas(self):
        kd = self.entries['kode_fasilitas'].get()
        nama = self.entries['nama'].get().strip()
        status = self.entries['status'].get()

        if not kd:
            messagebox.showwarning("Peringatan", "Pilih fasilitas yang akan diupdate!")
            return

        fasilitas = Fasilitas(kd, nama, status)
        self.controller.update_fasilitas(fasilitas)
        messagebox.showinfo("Sukses", f"Fasilitas {nama} berhasil diupdate.")
        self.load_data()
        self.clear_form()

    def hapus_fasilitas(self):
        kd = self.entries['kode_fasilitas'].get()
        nama = self.entries['nama'].get().strip()
        if not kd:
            messagebox.showwarning("Peringatan", "Pilih fasilitas yang akan dihapus!")
            return
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus fasilitas {nama} ?")
        if confirm:
            self.controller.hapus_fasilitas(kd)
            messagebox.showinfo("Sukses", "Data fasilitas berhasil dihapus.")
            self.load_data()
            self.clear_form()

    def clear_form(self):
        self.entries['kode_fasilitas'].config(state='normal')
        for key, widget in self.entries.items():
            if isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, tk.StringVar):
                widget.set('')
            else:
                widget.delete(0, 'end')
        self.tree.selection_remove(self.tree.selection())
        self.generate_kode_otomatis()

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.entries['kode_fasilitas'].config(state='normal')
            self.entries['kode_fasilitas'].delete(0, 'end')
            self.entries['kode_fasilitas'].insert(0, values[0])
            self.entries['kode_fasilitas'].config(state='disabled')

            self.entries['nama'].delete(0, 'end')
            self.entries['nama'].insert(0, values[1])

            self.entries['status'].set(values[2])

    def cari_fasilitas(self, event):
        keyword = self.entry_search.get().strip()
        if keyword == "":
            fasilitas_list = self.controller.fetch_fasilitas()
        else:
            fasilitas_list = self.controller.cari_fasilitas(keyword)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for fasilitas in fasilitas_list:
            self.tree.insert('', 'end', values=(
                fasilitas.kd_fasilitas,
                fasilitas.nama,
                fasilitas.status
            ))

    def generate_kode_otomatis(self):
        kd_baru = self.controller.generate_kd_fasilitas()
        self.entries['kode_fasilitas'].config(state='normal')
        self.entries['kode_fasilitas'].delete(0, 'end')
        self.entries['kode_fasilitas'].insert(0, kd_baru)
        self.entries['kode_fasilitas'].config(state='disabled')