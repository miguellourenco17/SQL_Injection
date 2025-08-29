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

def safe_login(conn, username, password):
    # ✅ Compliant: parameterized query
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    return cur.fetchall()


# vulnerable_sqli_sonar.py
import sqlite3
import sys

def vulnerable_query(conn, user_id):
    cursor = conn.cursor()
    # ❌ Noncompliant: SQL injection via string concatenation
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)  # SonarQube should flag this as a hotspot
    return cursor.fetchall()

if __name__ == "__main__":
    # Setup in-memory DB
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    c.execute("INSERT INTO users (username) VALUES ('alice')")
    c.execute("INSERT INTO users (username) VALUES ('bob')")
    conn.commit()

    if len(sys.argv) < 2:
        print("Usage: python vulnerable_sqli_sonar.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]   # tainted source
    results = vulnerable_query(conn, user_id)
    print("Query results:", results)
