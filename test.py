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
