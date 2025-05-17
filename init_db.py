import sqlite3

def init_db():
    conn = sqlite3.connect('init_db.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')

    # Create user_profiles table
    # Create user_profiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        username TEXT PRIMARY KEY,
        gre_score INTEGER,
        preferred_universities TEXT,
        progress TEXT,
        notes TEXT
    )
''')


    # Create gre_attempts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gre_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER,
            date TEXT
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    gre_score INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
 )
    ''')


    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
