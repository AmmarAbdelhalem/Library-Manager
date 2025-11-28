import tkinter as tk

class SettingsPage(tk.Frame):
    def __init__(self, parent, on_logout=None):
        super().__init__(parent)
        self.on_logout = on_logout

        tk.Label(self, text="Settings", font=("Arial", 28)).pack(pady=20)
        tk.Button(self, text="Log Out", font=("Arial", 14), width=15, command=self._logout).pack(pady=20)

    def _logout(self):
        if self.on_logout:
            self.on_logout()