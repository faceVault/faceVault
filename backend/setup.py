import sqlite3

#creates the two tables that hold our db

conn = sqlite3.connect('vault.db')

conn.execute('CREATE TABLE IF NOT EXISTS User (UserID INTEGER PRIMARY KEY, Username TEXT, Email TEXT, FaceRef BLOB, Security1 TEXT, Security2 TEXT, Security3 TEXT)')

conn.execute('CREATE TABLE IF NOT EXISTS Files (FileID INTEGER PRIMARY KEY, Owner TEXT, FileName TEXT, File BLOB)')

conn.commit()

print("Tables created successfully")

conn.close()
