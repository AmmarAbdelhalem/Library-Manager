from Data.books import books as SEED_BOOKS
from Pages.dashboard import DashboardPage
from Pages.settings import SettingsPage
from Pages.library import LibraryPage
from Pages.profile import ProfilePage
from Pages.auth import AuthPage
from tkinter import ttk
import tkinter as tk
from Data import db

class App(tk.Frame):
    def __init__(self, master, current_user=None, on_logout=None):
        super().__init__(master)

        master.title("Library Management")
        master.geometry("1100x650")
        master.minsize(800, 500)

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self._on_logout = on_logout

        self.dashboard_page = DashboardPage(self.tabs, current_user)
        self.library_page = LibraryPage(self.tabs, current_user)
        self.profile_page = ProfilePage(self.tabs, current_user)
        self.settings_page = SettingsPage(self.tabs, on_logout=self._handle_logout)

        self.tabs.add(self.dashboard_page, text="Dashboard")
        self.tabs.add(self.library_page, text="Library")
        self.tabs.add(self.profile_page, text="Profile")
        self.tabs.add(self.settings_page, text="Settings")

    def _handle_logout(self):
        if self._on_logout:
            self._on_logout()

def _start_main_app(root, uid, username):
    for widget in root.winfo_children():
        widget.destroy()

    def on_logout():
        _show_auth_screen(root)

    app_frame = App(root, current_user=(uid, username), on_logout=on_logout)
    try:
        app_frame.library_page.set_profile_ref(app_frame.profile_page)
        app_frame.profile_page.set_library_ref(app_frame.library_page)
    except Exception:
        pass
    app_frame.pack(fill="both", expand=True)


def _show_auth_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

    def on_success(uid, username):
        _start_main_app(root, uid, username)

    AuthPage(root, on_success=on_success)


if __name__ == "__main__":
    if not db.db_exists():
        db.init_db(seed_books=SEED_BOOKS)

    root = tk.Tk()
    _show_auth_screen(root)
    root.mainloop()
