import sqlite3
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__, template_folder="templates", static_folder="static")

def init_db():
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS Employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date TEXT NOT NULL
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL
    )""")
    
    cursor.executemany("INSERT OR IGNORE INTO Employees VALUES (?, ?, ?, ?, ?)", [
        (1, "Alice", "Sales", 50000, "2021-01-15"),
        (2, "Bob", "Engineering", 70000, "2020-06-10"),
        (3, "Charlie", "Marketing", 60000, "2022-03-20")
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO Departments VALUES (?, ?, ?)", [
        (1, "Sales", "Alice"),
        (2, "Engineering", "Bob"),
        (3, "Marketing", "Charlie")
    ])
    
    conn.commit()
    conn.close()

def process_query(user_query):
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    def clean_input(text):
        return re.sub(r'[^\w\s]', '', text).strip()

    if match := re.match(r"show me all employees in the (.+) department", user_query, re.I):
        department = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT Name FROM Employees WHERE Department = ?", (department,))
        result = [row[0] for row in cursor.fetchall()]
        if len(result) > 1:
            response = f"Employees in {department} Department are:\n" + "\n".join(result)
        else:
            response = f"Employee in {department} Department is:\n" + "\n".join(result) if result else f"No employees found in {department} department."

    elif match := re.match(r"who is the manager of the (.+) department", user_query, re.I):
        department = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT Manager FROM Departments WHERE Name = ?", (department,))
        result = cursor.fetchone()
        response = f"Manager of {department} Department: {result[0]}" if result else "Department not found."

    elif match := re.match(r"list all employees hired after (\d{4}-\d{2}-\d{2})", user_query, re.I):
        hire_date = match.group(1)
        cursor.execute("SELECT Name FROM Employees WHERE Hire_Date > ?", (hire_date,))
        result = [row[0] for row in cursor.fetchall()]
        if len(result) > 1:
            response = f"Employees hired after {hire_date} are:\n" + "\n".join(result)
        else:
            response = f"Employee hired after {hire_date} is:\n" + "\n".join(result) if result else f"No employees found hired after {hire_date}."

    elif match := re.match(r"what is the total salary expense for the (.+) department", user_query, re.I):
        department = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,))
        result = cursor.fetchone()[0]
        response = f"Total salary expense for {department} Department: ${result}" if result else "Department not found or no employees."

    elif match := re.match(r"list all departments", user_query, re.I):
        cursor.execute("SELECT Name FROM Departments")
        result = [row[0] for row in cursor.fetchall()]
        response = "Departments:\n" + "\n".join(result) if result else "No departments found."

    elif match := re.match(r"how many employees are there in the (.+) department", user_query, re.I):
        department = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT COUNT(*) FROM Employees WHERE Department = ?", (department,))
        result = cursor.fetchone()[0]
        response = f"There are {result} employees in {department} department." if result else "Department not found or no employees."

    elif match := re.match(r"which department does (.+) work in", user_query, re.I):
        employee = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT Department FROM Employees WHERE Name = ?", (employee,))
        result = cursor.fetchone()
        response = f"{employee} works in {result[0]} Department." if result else f"{employee} not found."

    elif match := re.match(r"list all employees with a salary above (\d+)", user_query, re.I):
        salary = int(match.group(1))
        cursor.execute("SELECT Name FROM Employees WHERE Salary > ?", (salary,))
        result = [row[0] for row in cursor.fetchall()]
        if len(result) > 1:
            response = f"Employees earning above ${salary} are:\n" + "\n".join(result)
        else:
            response = f"Employee earning above ${salary} is:\n" + "\n".join(result) if result else f"No employees earn more than ${salary}."

    elif match := re.match(r"when was (.+) hired", user_query, re.I):
        employee = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT Hire_Date FROM Employees WHERE Name = ?", (employee,))
        result = cursor.fetchone()
        response = f"{employee} was hired on {result[0]}" if result else f"{employee} not found."

    elif match := re.match(r"what department does (.+) work in", user_query, re.I):
        employee = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT Department FROM Employees WHERE Name = ?", (employee,))
        result = cursor.fetchone()
        response = f"{employee} works in {result[0]} Department." if result else f"{employee} not found."

    elif match := re.match(r"who earns more than (\d+)", user_query, re.I):
        salary = int(match.group(1))
        cursor.execute("SELECT Name FROM Employees WHERE Salary > ?", (salary,))
        result = [row[0] for row in cursor.fetchall()]
        if len(result) > 1:
            response = f"Employees earning more than ${salary} are:\n" + "\n".join(result)
        else:
            response = f"Employee earning more than ${salary} is:\n" + "\n".join(result) if result else f"No employees earn more than ${salary}."

    elif match := re.match(r"show all employees in the (.+) department with hire dates", user_query, re.I):
        department = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT Name, Hire_Date FROM Employees WHERE Department = ?", (department,))
        result = cursor.fetchall()
        if len(result) > 1:
            response = f"Employees in {department} Department with Hire Dates:\n"
            response += "\n".join([f"{name} - {hire_date}" for name, hire_date in result])
        else:
            response = f"Employee in {department} Department with Hire Date:\n"
            response += "\n".join([f"{name} - {hire_date}" for name, hire_date in result]) if result else f"No employees found in {department} department."

    elif match := re.match(r"what is the salary of (.+)", user_query, re.I):
        employee = clean_input(match.group(1)).capitalize()
        cursor.execute("SELECT Salary FROM Employees WHERE Name = ?", (employee,))
        result = cursor.fetchone()
        response = f"{employee}'s salary is ${result[0]}" if result else f"{employee} not found."

    else:
        response = "Sorry, I didn't understand that query. Please try again with a valid query."

    conn.close()
    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "").strip()
    response = process_query(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)