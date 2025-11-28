# Library Manager

A simple yet powerful desktop application for managing your personal library built with Python and Tkinter.

## Features

- **User Authentication**: Register and login with secure password hashing
- **Book Management**: View, search, and manage books in your library
- **Borrowing System**: Borrow books with customizable due dates
- **Favorites**: Mark books as favorites for easy access
- **Due Date Tracking**: Keep track of borrowed books and their due dates
- **Return Books**: Track returned books and manage your borrowing history

## Requirements

- Python 3.7 or higher
- Tkinter (usually comes with Python)
- SQLite3 (included with Python)

## Installation

### 1. Clone or Download the Repository

```bash
git clone https://github.com/AmmarAbdelhalem/Library-Manager.git
cd "Library-Manager"
```

### 2. Verify Python Installation

Make sure Python 3.7+ is installed:

```bash
python --version
```

### 3. No External Dependencies Required

This project uses only Python standard library modules:
- `tkinter` - GUI framework
- `sqlite3` - Database
- `hashlib` - Password hashing
- `datetime` - Date/time operations
- `typing` - Type hints
- `os` - File operations

## Running the Application

```bash
cd "Library-Manager"
python main.py
```

## First Launch

1. Run `python main.py`
2. You'll see the authentication screen
3. Click **Register** to create a new account
4. Enter username and password
5. You'll be logged in and see the main application

## Project Structure

```
Lib Manager/
├── main.py                 # Application entry point
├── README.md               # This file
├── Data/
│   ├── __init__.py         # Package initializer
│   ├── db.py               # Database functions
│   └── books.py            # Sample books seed data
├── Pages/
│   ├── __init__.py         # Package initializer
│   ├── auth.py             # Login/Register page
│   ├── dashboard.py        # Welcome/Dashboard page
│   ├── library.py          # Books library page
│   ├── profile.py          # User profile page
│   └── settings.py         # Settings page
└── library.db              # SQLite database (created on first run)
```

## Usage Guide

### Dashboard Tab
- Welcome message with your username

### Library Tab
- **Search Box**: Search books by title, author, or category
- **Details**: View full details of a selected book
- **Borrow**: Borrow a book (you'll be asked for the number of days)
- **Favorite**: Add a book to your favorites
- **Delete**: Remove a book from the library

### Profile Tab
- **View Your Books**: See all your borrowed books and favorites in one place
- **Borrowed Books**: Open a window showing all active borrowed books
  - See the due date for each book
  - Get notified if a book is overdue
  - Return a book when finished
- **Unfavorite**: Remove a book from your favorites
- **Details**: View details of any book in your collection

### Settings Tab
- **Log Out**: Sign out and return to the login screen

## Database

The application uses SQLite3, which stores data in `library.db`. This file is automatically created on first launch.

### Tables:
- **users**: User accounts and password hashes
- **books**: Book catalog with title, author, year, category, description
- **borrows**: Borrow records with due dates and return tracking
- **favorites**: User's favorite books

## Features Explained

### Borrowing System
- Borrow any book from the library
- Specify how many days you want to borrow it (default 14 days)
- Due date is automatically calculated
- View active borrows in your Profile → Borrowed Books window
- Return books when finished

### Favorites
- Add books to favorites for quick access
- View all favorites in your Profile tab
- Remove from favorites at any time

### Search
- Real-time search across all books
- Search by title, author, or category

### Password Security
- Passwords are hashed using SHA-256
- Original passwords are never stored

## Troubleshooting

### "No module named 'tkinter'"
- **Windows**: Tkinter should be included with Python. Reinstall Python and check "tcl/tk and IDLE" during installation
- **Linux**: Install tkinter: `sudo apt-get install python3-tk`
- **macOS**: Should be included, or install via Homebrew: `brew install python-tk`

### Database issues
- Delete `library.db` to start fresh
- The database will be recreated on next launch with sample books

### Application won't start
- Ensure Python 3.7+ is installed
- Check that all files are in the correct directories
- Try running from PowerShell/Terminal directly

## Default Sample Books

The application comes pre-loaded with 100+ classic and popular books across various categories including:
- Programming
- Fiction
- Fantasy
- Self-help
- Classic Literature
- Science Fiction
- And more!

## License

This project is provided as-is for personal use.

## Author

Created with Python and Tkinter

---

**Enjoy managing your library!**
