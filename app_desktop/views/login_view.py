import tkinter as tk
from tkinter import ttk, messagebox
from app_desktop.database.connection import Database
from PIL import Image, ImageTk
import urllib.request
import io

class LoginFrame(ttk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.db = Database()

        self.pack_propagate(False)
        self.config(width=600, height=400)
        self.configure(padding=20)
        self.center_frame = ttk.Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 12))
        style.configure("TEntry", font=("Segoe UI", 12))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#007ACC")

        style.configure("Green.TButton",
                        background="#4CAF50",
                        foreground="white",
                        font=("Segoe UI", 12, "bold"),
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor='none')
        style.map("Green.TButton",
                  background=[("active", "#45a049"), ("!disabled", "#4CAF50")],
                  foreground=[("disabled", "gray")])

        image_url = "https://cdn-icons-png.flaticon.com/512/295/295128.png"
        try:
            with urllib.request.urlopen(image_url) as u:
                raw_data = u.read()
            try:
                resample_mode = Image.Resampling.LANCZOS
            except AttributeError:
                resample_mode = Image.ANTIALIAS
            im = Image.open(io.BytesIO(raw_data)).resize((100, 100), resample_mode)
            self.photo = ImageTk.PhotoImage(im)
        except Exception as e:
            print(f"Gagal load gambar: {e}")
            self.photo = None

        self.center_frame = ttk.Frame(self, padding=30, relief=tk.RIDGE, borderwidth=2)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        if self.photo:
            image_label = ttk.Label(self.center_frame, image=self.photo)
            image_label.pack(pady=(0, 15))

        # Header
        header = ttk.Label(self.center_frame, text="SIkost VibeHouse", style="Header.TLabel")
        header.pack(pady=(0, 15))

        # Form frame username & password
        form_frame = ttk.Frame(self.center_frame)
        form_frame.pack()

        ttk.Label(form_frame, text="👤 Username:").grid(row=0, column=0, sticky=tk.W, pady=6, padx=5)
        self.entry_user = ttk.Entry(form_frame, width=30)
        self.entry_user.grid(row=0, column=1, pady=6, padx=5)

        ttk.Label(form_frame, text="🔒 Password:").grid(row=1, column=0, sticky=tk.W, pady=6, padx=5)
        self.entry_pass = ttk.Entry(form_frame, show="*", width=30)
        self.entry_pass.grid(row=1, column=1, pady=6, padx=5)

        # Binding Enter key di kolom password supaya bisa langsung login
        self.entry_pass.bind("<Return>", self.on_enter_pressed)

        # Tombol login
        login_btn = ttk.Button(form_frame, text="🚀 Login", command=self.login, style="Green.TButton")
        login_btn.grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

    def on_enter_pressed(self, event):
        if self.entry_pass.get().strip():
            self.login()

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        user_data = self.db.cek_login(username, password)
        if user_data:
            self.on_login_success(user_data)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")