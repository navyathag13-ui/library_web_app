# LibraryHub — Library Management Web App

A simple, clean web application for managing library books.
Built with **Python · Flask · SQLite · HTML · CSS**

---

## What This App Does

LibraryHub lets you manage a collection of library books through a web browser.

You can:
- View all books in a searchable, filterable table
- Add new books with title, author, and genre
- Borrow a book (marks it as borrowed with today's date)
- Return a book (marks it as available again)
- Remove a book from the library
- See live counts of total, available, and borrowed books

---

## Tools Used

| Tool | What it does |
|------|--------------|
| Python | Main programming language |
| Flask | Web framework — handles pages and requests |
| Flask-SQLAlchemy | Makes working with the database easy |
| SQLite | Stores all the book data in a file |
| Jinja2 (HTML templates) | Generates web pages dynamically |
| CSS | Styles the app to look clean and professional |

---

## Features

**Core features**
- View all books in a table
- Add a book (title, author, genre)
- Borrow a book (status changes to Borrowed)
- Return a book (status changes to Available)
- Remove a book (only if not currently borrowed)

**Extra features**
- Search books by title, author, or genre
- Filter by status (Available / Borrowed / All)
- See borrow date and return date for each book
- Stats bar shows total, available, and borrowed counts
- Flash messages for success and error feedback
- Duplicate book protection (same title + author blocked)
- Prevents removing a book that is currently borrowed

---

## Project Structure

```
Library_web_app/
│
├── app.py                  ← Main Flask app (routes + database model)
├── requirements.txt        ← Python packages needed
├── .gitignore              ← Files not to commit to Git
├── README.md               ← This file
│
├── templates/
│   ├── base.html           ← Shared layout (navbar, footer)
│   ├── index.html          ← Home page — shows all books
│   └── add_book.html       ← Form to add a new book
│
└── static/
    └── style.css           ← All the styling
```

---

## How to Run (Step-by-Step)

### Step 1 — Make sure Python is installed

Open your terminal and type:
```bash
python3 --version
```
You should see something like `Python 3.10.x`. If not, download Python from [python.org](https://www.python.org).

---

### Step 2 — Go to the project folder

```bash
cd path/to/Library_web_app
```

---

### Step 3 — Create a virtual environment

A virtual environment keeps your project packages separate from other projects.

```bash
python3 -m venv .venv
```

This creates a folder called `.venv`.

---

### Step 4 — Activate the virtual environment

**On Mac/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

You will see `(.venv)` at the start of your terminal line.

---

### Step 5 — Install the required packages

```bash
pip install -r requirements.txt
```

This installs Flask and Flask-SQLAlchemy.

---

### Step 6 — Run the app

```bash
python app.py
```

You will see output like this:
```
 * Running on http://127.0.0.1:5000
```

---

### Step 7 — Open the app in your browser

Go to: **http://127.0.0.1:5000**

The database (`library.db`) is created automatically the first time you run the app.

---

### Step 8 — Try the features

1. Click **+ Add Book** to add a few books
2. Click **Borrow** next to any available book
3. Click **Return** to return a borrowed book
4. Use the search bar to search by title, author, or genre
5. Use the dropdown to filter by Available or Borrowed
6. Click **Remove** to delete an available book

---

## Screenshots

> Add screenshots here after running the app!

| Home Page | Add Book Form |
|-----------|---------------|
| *(screenshot)* | *(screenshot)* |

---

## Future Improvements

- Add user login so each member has their own borrowing history
- Add a due date and overdue warning system
- Add pagination when the book list gets very long
- Add the ability to edit book details after adding
- Deploy the app online using Render or Railway

---

## Database

The app uses a single SQLite database file called `library.db` (created automatically).

**Books table:**

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Auto-generated unique ID |
| title | Text | Book title (required) |
| author | Text | Author name (required) |
| genre | Text | Genre (default: General) |
| status | Text | 'available' or 'borrowed' |
| borrow_date | Text | Date the book was borrowed |
| return_date | Text | Date the book was returned |
| date_added | Text | Date the book was added |
