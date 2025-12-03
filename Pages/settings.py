import tkinter as tk
from tkinter import ttk


class SettingsPage(tk.Frame):
    def __init__(self, parent, on_logout=None):
        super().__init__(parent)
        self.on_logout = on_logout
        ttk.Button(self, text="Log Out", width=15, command=self._logout).pack(pady=20)

    def _logout(self):
        if self.on_logout:
            self.on_logout()
