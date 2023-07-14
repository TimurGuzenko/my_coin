import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())
    
cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, course, logo) VALUES (?, ?, ?, ?)",
            ('First Post', 'Content for the first post', 'BTC', 'static\images\Bitcoin.svg.png')
            )

cur.execute("INSERT INTO posts (title, content, course, logo) VALUES (?, ?, ?, ?)",
            ('Second Post', 'Content for the second post', 'ETH', 'static\images\Ethereum-icon-purple.svg.png')
            )

connection.commit()
connection.close()