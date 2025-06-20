import tkinter as tk
from PIL import Image, ImageTk
import datetime
import requests
from io import BytesIO

class Navbar(tk.Frame):
    def __init__(self, master, user_data, on_dashboard_click, on_logout_click, on_profile_click, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.user_data = user_data

        self.configure(bg="#5DADE2", height=50)

        left_frame = tk.Frame(self, bg="#5DADE2")
        left_frame.pack(side="left", padx=20, pady=10)

        hamburger = tk.Label(left_frame, text="≡", bg="#5DADE2", fg="white", font=("Segoe UI", 16, "bold"))
        hamburger.pack(side="left", padx=(0, 10))

        right_frame = tk.Frame(self, bg="#5DADE2")
        right_frame.pack(side="right", pady=10, padx=15)

        url = "https://cdn-icons-png.flaticon.com/512/149/149071.png"  # Ganti jika mau icon lain
        response = requests.get(url)
        img_data = BytesIO(response.content)

        self.profile_icon = Image.open(img_data)
        self.profile_icon = self.profile_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.profile_photo = ImageTk.PhotoImage(self.profile_icon)

        profile_btn = tk.Menubutton(
            right_frame, image=self.profile_photo,
            bg="#5DADE2", relief="flat", cursor="hand2",
            activebackground="#3498db", bd=0
        )
        profile_btn.menu = tk.Menu(profile_btn, tearoff=0, bg="white", fg="black", font=("Segoe UI", 10))
        profile_btn["menu"] = profile_btn.menu
        profile_btn.menu.add_command(label="Profil", command=on_profile_click)
        profile_btn.menu.add_command(label="Logout", command=on_logout_click)
        profile_btn.pack(side="right", padx=(0, 5))

        self.time_label = tk.Label(right_frame, bg="#5DADE2", fg="white", font=("Segoe UI", 11, "bold"))
        self.time_label.pack(side="right", padx=(0, 10))
        self.update_time()

    def update_time(self):
        hari_indo = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }
        now = datetime.datetime.now()
        hari = hari_indo[now.strftime("%A")]
        tanggal = now.strftime("%d-%m-%Y")
        formatted_time = f"{hari}, {tanggal}"
        self.time_label.config(text=formatted_time)
        self.after(1000, self.update_time)