import sqlite3

def run_query(user_input):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cur.execute("INSERT INTO users VALUES (1, 'admin')")

    # ❌ Vulnerable: SQL Injection (string concatenation with tainted input)
    query = "SELECT * FROM users WHERE id = " + user_input
    cur.execute(query)   # This is the sink Sonar looks for
    return cur.fetchall()

if __name__ == "__main__":
    user_input = input("Enter user id: ")  # tainted source
    print(run_query(user_input))


# vulnerable_mysql.py
import MySQLdb
import sys

def vulnerable_query(user_input):
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="testdb")
    cursor = db.cursor()
    
    # ❌ Noncompliant: SQL Injection
    query = "SELECT * FROM users WHERE id = " + user_input
    cursor.execute(query)  # SonarQube should flag this
    for row in cursor.fetchall():
        print(row)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_mysql.py <id>")
        sys.exit(1)

    vulnerable_query(sys.argv[1])  # tainted input


import sqlite3

def vulnerable_login(username, password):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
    cur.execute("INSERT INTO users VALUES (1, 'admin', 'admin123')")
    conn.commit()

    # ❌ VULNERABLE: user input directly injected into the SQL string
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    print("Executing:", query)
    cur.execute(query)   # SQL injection risk
    return cur.fetchall()


if __name__ == "__main__":
    # attacker could input: admin' -- 
    uname = input("Enter username: ")
    pwd = input("Enter password: ")

    rows = vulnerable_login(uname, pwd)
    print("Results:", rows)
