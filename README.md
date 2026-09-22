# Book Data Pipeline & Analytics System

An end-to-end Python data processing pipeline that scrapes books from `books.toscrape.com`, manages them in SQLite using OOP, exposes them via a FastAPI REST microservice, and generates CSV data & Matplotlib scatter plot visualizations.

---

## 📁 Directory Structure

```text
Capstone/
├── venv/                 # Python virtual environment
├── database.py           # SQLite Database Manager (OOP CRUD architecture)
├── scraper.py            # Web Scraper engine (scrapes first 20 books)
├── main.py               # FastAPI REST Microservice & Uvicorn entry point
├── client.py             # Client script, Pandas DataFrame loading & Matplotlib Scatter Plot
├── books.db              # SQLite Database file
├── exported_books.csv    # Exported CSV dataset
├── price_vs_rating.png   # Generated Price vs. Rating scatter plot chart
├── requirements.txt      # Python package dependencies
└── .gitignore            # Git ignore rules
```

---

## 🚀 How to Run the Project

### Step 1: Clone Repository & Setup Virtual Environment

```bash
# Navigate to project directory
cd Capstone

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 2: Scrape Books & Populate SQLite Database

Run the web scraper to extract the first 20 books and store them into `books.db`:

```bash
python scraper.py
```

---

### Step 3: Start FastAPI Microservice

Start the REST API server on `http://127.0.0.1:8000`:

```bash
python main.py
```
> 📌 **Interactive API Documentation**: Open **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** in your browser.

---

### Step 4: Run Client Application & Generate Analytics

Open a **new terminal tab/window**, activate `venv`, and run:

```bash
source venv/bin/activate
python client.py
```

This will:
1. Fetch all books from `GET http://127.0.0.1:8000/books`.
2. Load and display the Pandas DataFrame in the console.
3. Export data to `exported_books.csv`.
4. Generate and save the scatter plot to `price_vs_rating.png`.

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/books` | Retrieve all stored books |
| **GET** | `/books/{id}` | Retrieve a single book by ID |
| **POST** | `/books` | Create a new book entry |
| **PUT** | `/books/{id}` | Update an existing book entry |
| **DELETE** | `/books/{id}` | Delete a book entry by ID |
