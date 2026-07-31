import sqlite3
from pathlib import Path

# Database Path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "employee.db"


def connect():
    return sqlite3.connect(DB_PATH)


def create_table():

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            designation TEXT NOT NULL,
            salary REAL NOT NULL,
            email TEXT,
            phone TEXT
        )
    """)

    connection.commit()
    connection.close()


# -------------------------
# Add Employee
# -------------------------
def add_employee(name, employee_id, department,
                 designation, salary, email, phone):

    connection = connect()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO employees(
                name,
                employee_id,
                department,
                designation,
                salary,
                email,
                phone
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            employee_id,
            department,
            designation,
            salary,
            email,
            phone
        ))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


# -------------------------
# View Employees
# -------------------------
def get_employees():

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    connection.close()

    return employees

def update_employee(
    id,
    name,
    employee_id,
    department,
    designation,
    salary,
    email,
    phone
):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE employees
        SET
            name=?,
            employee_id=?,
            department=?,
            designation=?,
            salary=?,
            email=?,
            phone=?
        WHERE id=?
    """, (
        name,
        employee_id,
        department,
        designation,
        salary,
        email,
        phone,
        id
    ))

    connection.commit()
    connection.close()
def delete_employee(id):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()
def search_employees(keyword):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE
            name LIKE ?
            OR employee_id LIKE ?
            OR department LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    employees = cursor.fetchall()

    connection.close()

    return employees
create_table()