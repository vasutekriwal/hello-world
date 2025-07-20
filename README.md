# Simple Note-Taking App

This is a minimal web-based note-taking application built with Python and Flask. It lets you create, view, edit, and delete notes stored locally in an SQLite database.

## Prerequisites

* Python 3.8 or higher

## Setup

1. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:

   ```bash
   python app.py
   ```

4. Open your browser at <http://localhost:5000> and start taking notes!

## Project Structure

```
.
├── app.py            # Flask backend
├── requirements.txt  # Python dependencies
├── templates/        # Jinja2 HTML templates
│   ├── base.html
│   ├── form.html
│   ├── index.html
│   └── note.html
└── static/
    └── style.css     # Basic styling
```

Feel free to customize the styles, add user authentication, or extend the database schema to suit your needs.
