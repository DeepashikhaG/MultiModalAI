from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Optional

import psycopg2
from psycopg2.extensions import connection as PGConnection
from psycopg2.extras import RealDictCursor


# =====================================
# MODEL
# =====================================

@dataclass
class Employee:
    employee_id: int
    name: str
    join_year: int
    salary: float
    department: str


# =====================================
# CONNECTION
# =====================================

def _get_default_dsn():
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    db = os.getenv("PGDATABASE", "company_db")
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "serene123")

    return f"host={host} port={port} dbname={db} user={user} password={password}"


def connect_db(dsn: Optional[str] = None) -> PGConnection:
    if dsn is None:
        dsn = _get_default_dsn()
    return psycopg2.connect(dsn)


# =====================================
# TABLE
# =====================================

def create_employee_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS employees(
        employee_id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        join_year INT NOT NULL,
        salary NUMERIC(12,2) NOT NULL,
        department TEXT NOT NULL
    );
    """

    with conn, conn.cursor() as cur:
        cur.execute(sql)


# =====================================
# INSERT
# =====================================

def insert_employee(conn, name, join_year, salary, department):
    sql = """
    INSERT INTO employees(name, join_year, salary, department)
    VALUES(%s,%s,%s,%s)
    ON CONFLICT(name) DO NOTHING;
    """

    with conn, conn.cursor() as cur:
        cur.execute(sql, (name, join_year, salary, department))


# =====================================
# SEED DATA
# =====================================

SEED_EMPLOYEES = [
    ('Aarav Sharma', 2018, 85000.0, 'Engineering'),
    ('Diya Verma', 2020, 65000.0, 'Sales'),
    ('Rohan Gupta', 2017, 92000.0, 'Engineering'),
    ('Isha Mehta', 2019, 72000.0, 'Marketing'),
    ('Kabir Singh', 2016, 98000.0, 'Engineering'),
    ('Ananya Das', 2021, 58000.0, 'Human Resources'),
    ('Vivaan Nair', 2015, 105000.0, 'Engineering'),
    ('Meera Iyer', 2018, 77000.0, 'Finance'),
    ('Arjun Patel', 2022, 60000.0, 'Sales'),
    ('Sneha Reddy', 2019, 69000.0, 'Marketing'),
    ('Rahul Mishra', 2017, 88000.0, 'Engineering'),
    ('Pooja Kulkarni', 2020, 64000.0, 'Human Resources'),
    ('Karan Kapoor', 2016, 97000.0, 'Engineering'),
    ('Neha Choudhary', 2018, 75000.0, 'Finance'),
    ('Aditya Jain', 2021, 61000.0, 'Sales'),
    ('Simran Kaur', 2019, 70000.0, 'Marketing'),
    ('Nikhil Bansal', 2015, 102000.0, 'Engineering'),
    ('Ritika Sinha', 2020, 66000.0, 'Finance'),
    ('Siddharth Roy', 2017, 91000.0, 'Engineering'),
    ('Priya Pillai', 2018, 78000.0, 'Human Resources'),
    ('Harsh Vardhan', 2016, 96000.0, 'Engineering'),
    ('Tanvi Deshpande', 2021, 59000.0, 'Sales'),
    ('Manish Tiwari', 2015, 103000.0, 'Engineering'),
    ('Kavya Nair', 2019, 71000.0, 'Marketing'),
    ('Amit Yadav', 2018, 83000.0, 'Engineering'),
    ('Shreya Bose', 2020, 67000.0, 'Finance'),
    ('Deepak Joshi', 2017, 90000.0, 'Engineering'),
    ('Ankit Agarwal', 2016, 94000.0, 'Engineering'),
    ('Riya Shah', 2022, 62000.0, 'Sales'),
    ('Varun Malhotra', 2015, 101000.0, 'Engineering'),
    ('Divya Menon', 2019, 73000.0, 'Marketing'),
    ('Gaurav Khanna', 2018, 86000.0, 'Engineering'),
    ('Sonal Arora', 2021, 60000.0, 'Human Resources'),
    ('Yash Gupta', 2020, 65000.0, 'Sales'),
    ('Anjali Srivastava', 2017, 89000.0, 'Finance'),
    ('Ritesh Pandey', 2016, 97000.0, 'Engineering'),
    ('Nisha Patil', 2018, 76000.0, 'Marketing'),
    ('Akash Chauhan', 2022, 61000.0, 'Sales'),
    ('Komal Jain', 2019, 72000.0, 'Human Resources'),
    ('Vikas Soni', 2015, 104000.0, 'Engineering'),
    ('Preeti Saxena', 2020, 68000.0, 'Finance'),
    ('Mohit Verma', 2017, 91000.0, 'Engineering'),
    ('Neeraj Kumar', 2016, 95000.0, 'Engineering'),
    ('Swati Kapoor', 2018, 79000.0, 'Marketing'),
    ('Abhishek Das', 2021, 60000.0, 'Sales'),
    ('Aishwarya Rai', 2019, 71000.0, 'Finance'),
    ('Rohit Sharma', 2015, 105000.0, 'Engineering'),
    ('Payal Singh', 2020, 66000.0, 'Human Resources'),
    ('Kunal Mehta', 2017, 89000.0, 'Engineering'),
    ('Neha Arora', 2018, 74000.0, 'Marketing'),
    ('Saurabh Jain', 2016, 96000.0, 'Engineering'),
    ('Pallavi Gupta', 2021, 62000.0, 'Sales'),
    ('Ajay Kumar', 2015, 102000.0, 'Engineering'),
    ('Shivani Mishra', 2019, 73000.0, 'Finance'),
    ('Rahul Verma', 2018, 85000.0, 'Engineering'),
    ('Ruchi Tandon', 2020, 67000.0, 'Marketing'),
    ('Alok Singh', 2017, 90000.0, 'Engineering'),
    ('Nikita Sharma', 2022, 61000.0, 'Human Resources'),
    ('Vivek Pandey', 2016, 95000.0, 'Engineering'),
    ('Snehal Patil', 2019, 72000.0, 'Finance'),
    ('Tarun Gupta', 2015, 103000.0, 'Engineering'),
    ('Poonam Yadav', 2020, 65000.0, 'Sales'),
    ('Rakesh Singh', 2017, 88000.0, 'Engineering'),
    ('Madhuri Dixit', 2018, 77000.0, 'Marketing'),
    ('Arvind Kumar', 2016, 94000.0, 'Engineering'),
    ('Geeta Sharma', 2021, 60000.0, 'Human Resources'),
    ('Naveen Joshi', 2019, 72000.0, 'Finance'),
    ('Chirag Shah', 2015, 101000.0, 'Engineering'),
    ('Sakshi Gupta', 2020, 66000.0, 'Marketing'),
    ('Dev Patel', 2017, 90000.0, 'Engineering'),
    ('Aditi Sharma', 2019, 72000.0, 'Marketing'),
    ('Rahul Khanna', 2017, 88000.0, 'Engineering'),
    ('Neha Gupta', 2020, 65000.0, 'Finance'),
    ('Vikas Yadav', 2016, 94000.0, 'Engineering'),
    ('Pooja Singh', 2021, 60000.0, 'Human Resources'),
    ('Aman Verma', 2018, 83000.0, 'Engineering'),
    ('Kriti Mehta', 2019, 71000.0, 'Marketing'),
    ('Rohit Bansal', 2015, 101000.0, 'Engineering'),
    ('Sneha Kapoor', 2020, 66000.0, 'Sales'),
    ('Arjun Nair', 2017, 90000.0, 'Engineering'),
    ('Megha Joshi', 2018, 75000.0, 'Finance'),
    ('Sandeep Mishra', 2016, 96000.0, 'Engineering'),
    ('Nikita Arora', 2021, 62000.0, 'Human Resources'),
    ('Kunal Shah', 2019, 78000.0, 'Marketing'),
    ('Deepika Reddy', 2020, 67000.0, 'Sales'),
    ('Harshit Jain', 2017, 89000.0, 'Engineering'),
    ('Priyanka Das', 2018, 76000.0, 'Finance'),
    ('Varsha Iyer', 2016, 95000.0, 'Engineering'),
    ('Manav Gupta', 2022, 61000.0, 'Sales'),
    ('Ritika Kapoor', 2019, 72000.0, 'Marketing'),
    ('Adarsh Singh', 2015, 103000.0, 'Engineering'),
    ('Swati Verma', 2020, 68000.0, 'Finance'),
    ('Anmol Sharma', 2018, 84000.0, 'Engineering'),
    ('Nitin Yadav', 2017, 90000.0, 'Engineering'),
    ('Kiran Patel', 2021, 63000.0, 'Human Resources'),
    ('Sonia Mehta', 2019, 71000.0, 'Marketing'),
    ('Ravi Kumar', 2016, 95000.0, 'Engineering'),
    ('Divya Gupta', 2020, 67000.0, 'Finance'),
    ('Tarun Arora', 2015, 102000.0, 'Engineering'),
    ('Ayesha Khan', 2018, 76000.0, 'Marketing'),
    ('Saurabh Mishra', 2017, 89000.0, 'Engineering'),
    ('Pallavi Jain', 2021, 61000.0, 'Sales'),
    ('Ajit Singh', 2016, 94000.0, 'Engineering'),
    ('Komal Sharma', 2019, 73000.0, 'Human Resources'),
    ('Ramesh Patel', 2015, 101000.0, 'Engineering'),
    ('Shalini Verma', 2020, 66000.0, 'Finance'),
    ('Abhay Gupta', 2018, 85000.0, 'Engineering'),
    ('Nidhi Kapoor', 2019, 72000.0, 'Marketing'),
    ('Vivek Yadav', 2017, 90000.0, 'Engineering'),
    ('Pankaj Singh', 2016, 96000.0, 'Engineering'),
    ('Ritu Sharma', 2021, 60000.0, 'Human Resources'),
    ('Ankit Verma', 2018, 83000.0, 'Engineering'),
    ('Mohit Sharma', 2017, 88000.0, 'Engineering'),
    ('Tanya Arora', 2020, 67000.0, 'Marketing'),
    ('Rahul Jain', 2016, 95000.0, 'Engineering'),
    ('Neeraj Yadav', 2015, 102000.0, 'Engineering'),
    ('Aarti Mehta', 2018, 76000.0, 'Finance'),
    ('Keshav Singh', 2022, 61000.0, 'Sales'),
    ('Ishita Kapoor', 2019, 73000.0, 'Marketing'),
    ('Manish Gupta', 2017, 89000.0, 'Engineering'),
    ('Preeti Sharma', 2020, 68000.0, 'Human Resources'),
    ('Rohit Verma', 2016, 94000.0, 'Engineering'),
    ('Nisha Jain', 2018, 75000.0, 'Finance'),
    ('Anurag Singh', 2015, 101000.0, 'Engineering'),
    ('Pooja Arora', 2019, 72000.0, 'Marketing'),
    ('Gaurav Sharma', 2017, 90000.0, 'Engineering'),
    ('Seema Gupta', 2021, 61000.0, 'Sales'),
    ('Deepak Verma', 2016, 96000.0, 'Engineering'),
    ('Ruchi Kapoor', 2018, 78000.0, 'Finance'),
    ('Aakash Singh', 2015, 103000.0, 'Engineering'),
    ('Meenakshi Sharma', 2019, 73000.0, 'Human Resources'),
    ('Naveen Gupta', 2017, 88000.0, 'Engineering'),
    ('Sonal Verma', 2020, 67000.0, 'Marketing'),
    ('Rajesh Kumar', 2016, 95000.0, 'Engineering'),
    ('Alka Singh', 2018, 76000.0, 'Finance'),
    ('Yogesh Sharma', 2015, 101000.0, 'Engineering'),
    ('Bhavna Gupta', 2019, 72000.0, 'Marketing'),
    ('Rakesh Verma', 2017, 89000.0, 'Engineering'),
    ('Kavita Sharma', 2021, 60000.0, 'Human Resources'),
    ('Lokesh Singh', 2018, 84000.0, 'Engineering'),
    ('Sunita Gupta', 2020, 68000.0, 'Finance'),
    ('Mahesh Verma', 2016, 94000.0, 'Engineering'),
    ('Priti Sharma', 2019, 73000.0, 'Marketing'),
    ('Dinesh Gupta', 2015, 102000.0, 'Engineering'),
    ('Geeta Verma', 2018, 76000.0, 'Finance'),
    ('Suresh Sharma', 2017, 90000.0, 'Engineering'),
    ('Anita Gupta', 2021, 61000.0, 'Sales'),
    ('Ravindra Verma', 2016, 96000.0, 'Engineering'),
    ('Kamla Sharma', 2019, 72000.0, 'Human Resources'),
    ('Shiv Kumar', 2015, 103000.0, 'Engineering'),
    ('Rekha Gupta', 2020, 67000.0, 'Marketing'),
    ('Om Prakash', 2017, 88000.0, 'Engineering'),
    ('Lata Sharma', 2018, 75000.0, 'Finance'),
    ('Raju Verma', 2016, 94000.0, 'Engineering'),
    ('Kusum Gupta', 2019, 72000.0, 'Human Resources'),
    ('Mohan Sharma', 2015, 101000.0, 'Engineering'),
    ('Savita Verma', 2020, 68000.0, 'Finance'),
    ('Hari Singh', 2017, 89000.0, 'Engineering'),
    ('Radha Gupta', 2018, 76000.0, 'Marketing'),
]


def seed_if_empty(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM employees")
        count = cur.fetchone()[0]

    if count == 0:
        for row in SEED_EMPLOYEES:
            insert_employee(conn, *row)


# =====================================
# INIT
# =====================================

def initialize_database():
    conn = connect_db()
    create_employee_table(conn)
    seed_if_empty(conn)
    conn.close()


# =====================================
# QUERIES
# =====================================

def get_all_employees(conn) -> List[Employee]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM employees ORDER BY employee_id")
        rows = cur.fetchall()

    return [Employee(**row) for row in rows]


def get_employee_by_name(conn, name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM employees WHERE LOWER(name)=LOWER(%s)",
            (name,)
        )
        rows = cur.fetchall()

    return [Employee(**row) for row in rows]


def get_department_employees(conn, dept):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM employees WHERE LOWER(department)=LOWER(%s)",
            (dept,)
        )
        rows = cur.fetchall()

    return [Employee(**row) for row in rows]


def get_highest_salary_employee(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM employees ORDER BY salary DESC LIMIT 1"
        )
        row = cur.fetchone()

    return Employee(**row)


# =====================================
# TEST
# =====================================

if __name__ == "__main__":
    initialize_database()
    print("Database Ready")