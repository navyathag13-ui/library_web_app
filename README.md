# LibraryHub

A full-stack library management dashboard built with **Vue 3 + TypeScript** (frontend) and **Flask + SQLite** (backend).

Manage physical resources (books, magazines, DVDs, etc.), track checkouts and returns with borrower names and due dates, and monitor overdue items — all from a clean, responsive Material Design UI.

---

## Features

| Area | What's included |
|------|----------------|
| **Dashboard** | Live stat cards (total / available / checked-out / overdue), category breakdown bars, recent loan activity feed |
| **Resources** | Server-side search, filter by status/category, sort controls, paginated table, copy-count chip |
| **Checkout** | Per-resource checkout modal — borrower name + configurable due date (defaults to +14 days) |
| **Edit** | In-place edit modal for title, author, category, ISBN, description, and copy count |
| **Detail Drawer** | Right-side slide-over with full resource info + paginated loan history |
| **Loan History** | Dedicated history view with search, status filter, overdue date highlighting, pagination |
| **Overdue tracking** | Backend marks loans overdue on startup; frontend badge overrides with `isOverdue` flag |
| **Multi-copy** | `totalCopies` / `availableCopies` — a resource stays "available" as long as one copy is free |
| **Toasts** | Global snackbar (Pinia `ui` store) for success/error feedback on every action |

---

## Tech Stack

**Frontend**
- Vue 3 (Composition API, `<script setup lang="ts">`)
- TypeScript (strict mode)
- Pinia (state management)
- Vuetify 3 + Material Design Icons
- Vue Router 4
- Axios
- Vitest + Vue Test Utils + happy-dom (19 tests)

**Backend**
- Python 3.10+ / Flask 3
- Flask-SQLAlchemy (SQLite)
- Flask-CORS

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10 or newer |
| Node.js | 18 or newer |
| npm | 9 or newer |

---

## Quick Start

### 1 — Clone / navigate into the project

```bash
cd /path/to/Library_web_app
```

### 2 — Backend

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the API server (http://localhost:5000)
python backend/app.py
```

The database (`library.db`) is created automatically on first run.

### 3 — Frontend

Open a **second terminal** in the same directory:

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start the dev server (http://localhost:5173)
npm run dev
```

Open **http://localhost:5173** in your browser.

> The Vite dev server proxies all `/api/*` requests to Flask at port 5000, so no CORS setup is needed during development.

---

## Available Scripts (frontend)

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server with hot reload |
| `npm run build` | Type-check + production build → `dist/` |
| `npm run test` | Run Vitest test suite (19 tests) |
| `npm run test:watch` | Run tests in watch mode |

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/resources` | List resources (search, status, category, sortBy, sortOrder, page, per_page) |
| `POST` | `/api/resources` | Add a new resource |
| `PATCH` | `/api/resources/:id` | Edit resource fields |
| `POST` | `/api/resources/:id/checkout` | Check out — creates a Loan record |
| `POST` | `/api/resources/:id/return` | Return — closes the active Loan |
| `DELETE` | `/api/resources/:id` | Remove resource + all loan history |
| `GET` | `/api/loans` | List loans (search, status, page, per_page) |
| `GET` | `/api/stats` | Dashboard counts + category breakdown |
| `GET` | `/api/activity` | 20 most recent loan events |

---

## Project Structure

```
Library_web_app/
├── backend/
│   ├── app.py              # Flask app factory + overdue sync on startup
│   ├── models.py           # Resource + Loan SQLAlchemy models
│   ├── requirements.txt
│   └── routes/
│       ├── resources.py    # CRUD + checkout/return
│       ├── loans.py        # Loan listing
│       └── stats.py        # Dashboard stats + activity
└── frontend/
    ├── src/
    │   ├── api/            # Centralized Axios client
    │   ├── components/     # 12 reusable UI components
    │   ├── stores/         # Pinia stores (resources, loans, ui)
    │   ├── types/          # TypeScript interfaces
    │   ├── views/          # DashboardView, ResourcesView, HistoryView
    │   └── tests/          # Vitest specs (19 tests, 4 files)
    ├── package.json
    └── vite.config.ts
```

---

## Running Tests

```bash
cd frontend
npm run test
```

Expected output:

```
✓ src/tests/StatusBadge.spec.ts      (4 tests)
✓ src/tests/LoanStatusBadge.spec.ts  (7 tests)
✓ src/tests/StatsCard.spec.ts        (4 tests)
✓ src/tests/ConfirmDialog.spec.ts    (4 tests)

Test Files  4 passed (4)
     Tests  19 passed (19)
```
