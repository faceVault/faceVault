import sqlite3

conn = sqlite3.connect('vault.db')

conn.execute('CREATE TABLE IF NOT EXISTS User (UserID INTEGER PRIMARY KEY, Username TEXT, Email TEXT, FaceRef BLOB, Security1 TEXT, Security2 TEXT, Security3 TEXT)')


#conn.execute('CREATE TABLE IF NOT EXISTS Files (FileID INTEGER PRIMARY KEY, FileName TEXT, Extension TEXT, Created TEXT, FOREIGN KEY (FileID) REFERENCES User (FileID))')

conn.execute('CREATE TABLE IF NOT EXISTS Files (FileID INTEGER PRIMARY KEY, Owner TEXT, FileName TEXT, File BLOB)')

conn.commit()

print("Tables created successfully")

conn.close()
