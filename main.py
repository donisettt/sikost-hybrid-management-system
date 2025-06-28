import tkinter as tk
from views.login_view import LoginFrame
from views.dashboard import DashboardApp

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SIkost VibeHouse")
        self.root.geometry("900x600")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.login_frame = LoginFrame(self.root, self.show_main_menu)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_main_menu(self, user_data):
        self.login_frame.pack_forget()
        self.dashboard = DashboardApp(self.root, self.show_login, user_data, self.on_profile_click)
        self.dashboard.pack(fill=tk.BOTH, expand=True)

    def on_profile_click(self):
        print("Profile diklik dari sidebar atau navbar.")

    def show_login(self):
        self.dashboard.destroy()
        self.login_frame = LoginFrame(self.root, self.show_main_menu)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def on_close(self):
        try:
            if hasattr(self, 'dashboard') and hasattr(self.dashboard, 'after_id'):
                self.root.after_cancel(self.dashboard.after_id)
            if hasattr(self, 'login_frame') and hasattr(self.login_frame, 'after_id'):
                self.root.after_cancel(self.login_frame.after_id)
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")
    app = App(root)
    root.mainloop()
