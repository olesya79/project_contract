import sqlite3 as sq

# Создание соединения с базой данных
with sq.connect('cont_proj.db') as con:
    cur = con.cursor()

# Создание таблицы для хранения информации о договорах
cur.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        created_date TEXT,
        sign_date TEXT,
        status TEXT DEFAULT 'Черновик',
        numer_proj INTEGER,
        FOREIGN KEY (numer_proj) REFERENCES projects (id)
    )
""")

# Создание таблицы для хранения информации о проектах
cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        created_date TEXT
    )
""")



