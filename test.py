# vulnerable_sqli_example.py
import sqlite3

def get_user_input():
    username = input("Username: ")          # tainted source
    password = input("Password: ")          # tainted source
    return username, password

def vulnerable_login(conn, username, password):
    # ❌ Noncompliant: SQL injection (unsafely building the query with user input)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing (vulnerable):", query)  # just to illustrate the bad query
    cur = conn.cursor()
    cur.execute(query)                       # Sonar should flag this
    return cur.fetchall()

if __name__ == "__main__":
    # Minimal setup so the script runs end-to-end
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()

    u, p = get_user_input()
    rows = vulnerable_login(conn, u, p)
    print("Result rows:", rows)
