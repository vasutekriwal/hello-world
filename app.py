from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = 'notes.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enable name-based access to columns
    return conn


def init_db():
    """Initialize the SQLite database with a simple notes table if it doesn't exist."""
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute(
            """
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created TIMESTAMP NOT NULL
            );
            """
        )
        conn.commit()
        conn.close()


# Initialize database on first run
init_db()


@app.route('/')
def index():
    """List all notes."""
    conn = get_db_connection()
    notes = conn.execute(
        'SELECT id, title, created FROM notes ORDER BY created DESC'
    ).fetchall()
    conn.close()
    return render_template('index.html', notes=notes)


@app.route('/note/<int:note_id>')
def note_detail(note_id):
    """Display a single note."""
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ?;', (note_id,)).fetchone()
    conn.close()
    if note is None:
        return 'Note not found', 404
    return render_template('note.html', note=note)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new note."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            return 'Title is required', 400
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO notes (title, content, created) VALUES (?, ?, ?);',
            (title, content, datetime.utcnow()),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # GET request
    return render_template('form.html', action='Create', note=None)


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    """Edit an existing note."""
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ?;', (note_id,)).fetchone()
    if note is None:
        conn.close()
        return 'Note not found', 404

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn.execute(
            'UPDATE notes SET title = ?, content = ? WHERE id = ?;',
            (title, content, note_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('note_detail', note_id=note_id))

    conn.close()
    return render_template('form.html', action='Edit', note=note)


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete(note_id):
    """Delete a note."""
    conn = get_db_connection()
    conn.execute('DELETE FROM notes WHERE id = ?;', (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Listen on all interfaces so the app is reachable from outside containers.
    app.run(debug=True, host='0.0.0.0', port=5000)