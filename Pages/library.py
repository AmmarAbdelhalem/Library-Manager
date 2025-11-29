from tkinter import ttk, messagebox, simpledialog
from Data import db
import tkinter as tk

class LibraryPage(tk.Frame):
    def __init__(self, parent, current_user=None):
        super().__init__(parent)

        self.current_user = current_user

        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=6)

        tk.Label(search_frame, text="Search").pack(side="left")
        self.search_var = tk.StringVar()
        entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        ttk.Button(search_frame, text="Add books", command=self.add_books).pack(side="right")
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
        ttk.Button(btn_frame, text="Borrow", width=12, command=self.borrow).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Favorite", width=12, command=self.favorite).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Delete", width=12, command=self.delete).grid(row=0, column=3, padx=10)

        self.refresh_books()

        self.profile_page_ref = None

    def set_profile_ref(self, profile_frame):
        self.profile_page_ref = profile_frame

    def search_books(self, event=None):
        query = self.search_var.get().lower()

        for row in self.table.get_children():
            self.table.delete(row)

        rows = db.books_search(query) if query else db.books_all()
        for row in rows:
            self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
            
    def add_books(self):
        title = simpledialog.askstring("Add Book", "Enter book title:", parent=self)
        if not title:
            return

        author = simpledialog.askstring("Add Book", "Enter book author:", parent=self)
        if not author:
            return

        year = simpledialog.askinteger("Add Book", "Enter publication year:", parent=self, minvalue=0, maxvalue=2100)
        if year is None:
            return

        category = simpledialog.askstring("Add Book", "Enter book category:", parent=self)
        if not category:
            return

        db.book_add(title, author, year, category)
        messagebox.showinfo("Book Added", f"'{title}' by {author} added to library.")
        self.refresh_books()

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

    def borrow(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first.")
            return

        if not self.current_user:
            messagebox.showwarning("Not signed in", "Please sign in to borrow books.")
            return
        values = self.table.item(selected, "values")
        book_id = values[0]

        days = simpledialog.askinteger("Borrow days", "How many days would you like to borrow this book for?", parent=self, minvalue=1, initialvalue=14)
        if days is None:
            return

        db.borrow_book(self.current_user[0], book_id, days)
        messagebox.showinfo("Borrowed", f"You borrowed '{values[1]}' for {days} days.")
        try:
            if self.profile_page_ref:
                self.profile_page_ref.refresh_books()
        except Exception:
            pass

    def favorite(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first.")
            return
        values = self.table.item(selected, "values")
        if not values or len(values) < 2:
            messagebox.showwarning("Invalid selection", "Could not read selected book information.")
            return

        book_id = values[0]
        title = values[1]
        if not self.current_user:
            messagebox.showwarning("Not signed in", "Please sign in to add favorites.")
            return

        ok = db.favorites_add(self.current_user[0], book_id)
        if ok:
            messagebox.showinfo("Favorited", f"'{title}' was added to your favorites.")
            if self.profile_page_ref:
                try:
                    self.profile_page_ref.refresh_books()
                except Exception:
                    pass
        else:
            messagebox.showinfo("Favorited", f"'{title}' is already in your favorites.")

    def delete(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first.")
            return

        values = self.table.item(selected, "values")
        if not values or len(values) < 2:
            messagebox.showwarning("Invalid selection", "Could not read selected book.")
            return

        book_id = values[0]
        title = values[1]

        ok_delete = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{title}'?")
        if not ok_delete:
            return

        ok = db.book_delete(book_id)
        if ok:
            self.table.delete(selected)
            messagebox.showinfo("Deleted", f"'{title}' was removed from library.")
        else:
            messagebox.showwarning("Not found", "Could not delete the selected book.")

    def refresh_books(self):
        for row in self.table.get_children():
            self.table.delete(row)
        rows = db.books_all()
        for row in rows:
            self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))