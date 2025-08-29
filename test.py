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
