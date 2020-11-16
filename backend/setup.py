import sqlite3

conn = sqlite3.connect('vault.db')

conn.execute('CREATE TABLE IF NOT EXISTS User (UserID INTEGER PRIMARY KEY, FullName TEXT, Email TEXT, FaceRef BLOB)')


conn.execute('CREATE TABLE IF NOT EXISTS Files (FileID INTEGER PRIMARY KEY, FileName TEXT, Extension TEXT, Created TEXT, FOREIGN KEY (FileID) REFERENCES User (FileID))')

conn.commit()

print("Tables created successfully")

conn.close()
