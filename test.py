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
