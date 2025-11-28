import tkinter as tk
from tkinter import ttk, messagebox
from Data import db


class AuthPage(tk.Frame):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success

        self.parent.title("Library Manager — Sign in")
        self.parent.geometry("420x220")
        self.parent.resizable(False, False)

        tk.Label(self, text="Welcome — please sign in", font=("Arial", 16)).pack(pady=(10, 8))

        frm = tk.Frame(self)
        frm.pack(padx=16, pady=8, fill="x")

        tk.Label(frm, text="Username:").grid(row=0, column=0, sticky="w")
        self.username = tk.StringVar()
        tk.Entry(frm, textvariable=self.username).grid(row=0, column=1, sticky="ew")

        tk.Label(frm, text="Password:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.password = tk.StringVar()
        tk.Entry(frm, textvariable=self.password, show="•").grid(row=1, column=1, sticky="ew", pady=(8, 0))

        frm.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=12)

        ttk.Button(btn_frame, text="Sign in", command=self.try_signin).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="Register", command=self.try_register).grid(row=0, column=1, padx=6)

        self.pack(fill="both", expand=True)

    def try_signin(self):
        uname = self.username.get().strip()
        pwd = self.password.get()
        if not uname or not pwd:
            messagebox.showwarning("Missing", "Please enter username and password.")
            return

        uid = db.user_verify(uname, pwd)
        if uid:
            messagebox.showinfo("Welcome", f"Signed in as {uname}.")
            self.on_success(uid, uname)
        else:
            messagebox.showwarning("Invalid", "Wrong username or password.")

    def try_register(self):
        uname = self.username.get().strip()
        pwd = self.password.get()
        if not uname or not pwd:
            messagebox.showwarning("Missing", "Please enter username and password to register.")
            return

        uid = db.user_create(uname, pwd)
        if uid:
            messagebox.showinfo("Registered", "Account created — now signed in.")
            self.on_success(uid, uname)
        else:
            messagebox.showwarning("Taken", "Username already exists. Try another.")