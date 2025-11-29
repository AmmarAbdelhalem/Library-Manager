from tkinter import ttk, messagebox, simpledialog
import tkinter as tk
from datetime import datetime
from Data import db

class ProfilePage(tk.Frame):
    def __init__(self, parent, current_user=None):
        super().__init__(parent)

        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=6)

        tk.Label(search_frame, text="Search").pack(side="left")
        self.search_var = tk.StringVar()
        entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=10)
        entry.bind("<KeyRelease>", self.search_books)

        columns = ("id", "title", "author", "year", "category")
        self.table = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            if col == "id":
                self.table.heading(col, text="")
                self.table.column(col, anchor="w", width=0, stretch=False)
            else:
                self.table.heading(col, text=col.capitalize())
                self.table.column(col, anchor="w", width=170)

        self.table.column("year", width=70)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Details", width=12, command=self.details).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Borrowed books", width=15, command=self.open_borrowed_window).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Unfavorite", width=12, command=self.unfavorite).grid(row=0, column=2, padx=10)

        self.current_user = current_user
        self.borrowed_rows = []
        self.favorites_rows = []
        self.library_page_ref = None
        self.refresh_books()

    def set_library_ref(self, lib_frame):
        self.library_page_ref = lib_frame

    def search_books(self, event=None):
        query = self.search_var.get().lower()

        for row in self.table.get_children():
            self.table.delete(row)

        if self.current_user:
            all_rows = self.borrowed_rows + self.favorites_rows
            rows = [r for r in all_rows if any(query in str(field).lower() for field in r)]
            for row in rows:
                self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
        else:
            rows = db.books_search(query) if query else db.books_all()
            for row in rows:
                self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

    def details(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first.")
            return

        data = self.table.item(selected, "values")

        messagebox.showinfo(
            "Book Details",
            f"Title: {data[1]}\nAuthor: {data[2]}\nYear: {data[3]}\nCategory: {data[4]}"
        )

    def refresh_books(self):
        for row in self.table.get_children():
            self.table.delete(row)

        if self.current_user:
            self.favorites_rows = db.favorites_by_user(self.current_user[0])
            for row in self.favorites_rows:
                self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
        else:
            rows = db.books_all()
            for row in rows:
                self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

    def open_borrowed_window(self):
        if not self.current_user:
            messagebox.showwarning("Not signed in", "Sign in to see borrowed books.")
            return

        top = tk.Toplevel(self)
        top.title("Borrowed Books")
        top.geometry("800x400")

        cols = ("id", "title", "author", "year", "category", "borrowed_at", "due_date")
        tree = ttk.Treeview(top, columns=cols, show="headings")
        for c in cols:
            if c == "id":
                tree.heading(c, text="")
                tree.column(c, width=0, stretch=False)
            else:
                tree.heading(c, text=c.replace("_", " ").title())
                tree.column(c, width=120)

        tree.pack(fill="both", expand=True, padx=8, pady=8)

        btnf = tk.Frame(top)
        btnf.pack(fill="x", pady=4)
        ttk.Button(btnf, text="Details", command=lambda: self._bb_details(tree)).grid(row=0, column=0, padx=6)
        ttk.Button(btnf, text="Due date", command=lambda: self._bb_due(tree)).grid(row=0, column=1, padx=6)
        ttk.Button(btnf, text="Return", command=lambda: self._bb_return(tree)).grid(row=0, column=2, padx=6)

        rows = db.borrowed_by_user(self.current_user[0])
        for r in rows:
            if r[7] is None:
                tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

        top.transient(self)
        top.grab_set()

    def _bb_details(self, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a borrowed book first.")
            return
        v = tree.item(sel, "values")
        messagebox.showinfo("Details", f"Title: {v[1]}\nAuthor: {v[2]}\nYear: {v[3]}\nCategory: {v[4]}\nBorrowed at: {v[5]}")

    def _bb_due(self, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a borrowed book first.")
            return
        v = tree.item(sel, "values")
        due = v[6]
        if not due:
            messagebox.showinfo("Due", "No due date recorded.")
            return
        try:
            dt = datetime.strptime(due, "%Y-%m-%d %H:%M:%S")
        except Exception:
            messagebox.showinfo("Due", f"Due: {due}")
            return
        days_left = (dt - datetime.now()).days
        if days_left < 0:
            messagebox.showinfo("Due", f"The book is overdue by {-days_left} days.")
        else:
            messagebox.showinfo("Due", f"{days_left} days left until due date ({due}).")

    def _bb_return(self, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a borrowed book first.")
            return
        v = tree.item(sel, "values")
        book_id = v[0]
        ok = db.return_book(self.current_user[0], book_id)
        if ok:
            messagebox.showinfo("Returned", f"You returned '{v[1]}'.")
            tree.delete(sel)
            self.refresh_books()
            if self.library_page_ref:
                try:
                    self.library_page_ref.refresh_books()
                except Exception:
                    pass
        else:
            messagebox.showwarning("Return failed", "Could not return that book.")

    def unfavorite(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first.")
            return

        if not self.current_user:
            messagebox.showwarning("Not signed in", "Sign in to manage favorites.")
            return

        values = self.table.item(selected, "values")
        if not values or len(values) < 2:
            messagebox.showwarning("Invalid selection", "Could not read selected book.")
            return

        book_id = values[0]
        title = values[1]

        ok = db.favorites_remove(self.current_user[0], book_id)
        if ok:
            self.table.delete(selected)
            messagebox.showinfo("Removed", f"'{title}' was removed from your favorites.")
            self.refresh_books()
        else:
            messagebox.showwarning("Not found", "This book is not in your favorites.")