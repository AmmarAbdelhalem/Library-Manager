import tkinter as tk


class DashboardPage(tk.Frame):
    def __init__(self, parent, current_user=None):
        super().__init__(parent)

        self.pack_propagate(False)

        center_frame = tk.Frame(self)
        center_frame.pack(expand=True, fill="both")

        if current_user:
            username = current_user[1]
            welcome_text = f"Welcome, {username}"
        else:
            welcome_text = "Welcome to your Library"

        tk.Label(
            center_frame, text=welcome_text, font=("Arial", 30, "bold"), fg="#333333"
        ).pack(pady=40)
