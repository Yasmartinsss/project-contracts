import sqlite3

def init_db():
    with sqlite3.connect("data/tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pendente'
        )
        ''')
        conn.commit()

if __name__ == "__main__":
    init_db()
