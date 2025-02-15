import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create a table for storing high scores."""
    try:
        sql_create_highscores_table = """CREATE TABLE IF NOT EXISTS highscores (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            nickname TEXT NOT NULL,
                                            score INTEGER NOT NULL
                                        );"""
        c = conn.cursor()
        c.execute(sql_create_highscores_table)
    except sqlite3.Error as e:
        print(e)

def insert_highscore(conn, nickname, score):
    """Insert a new high score into the highscores table."""
    sql = '''INSERT INTO highscores(nickname, score) VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (nickname, score))
    conn.commit()
    return cur.lastrowid

def get_highscores(conn, limit=5):
    """Query the top high scores."""
    cur = conn.cursor()
    cur.execute("SELECT nickname, score FROM highscores ORDER BY score DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    return rows