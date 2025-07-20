import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
def db_connect():
   conn = sqlite3.connect('instance/students.db')
   conn.row_factory = sqlite3.Row  # Enable access to columns by name
   return conn, conn.cursor()

# Create the students table
def create_table():
    conn, cursor = db_connect()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            index_number VARCHAR(20) UNIQUE,
            name VARCHAR(100),
            phone VARCHAR(15),
            grades VARCHAR(50)
        )
    ''')
    conn.commit()
    conn.close()

# Insert sample data
def insert_sample_data():
    conn, cursor = db_connect()
    sample_data = [
        ('S001', 'John Doe', '0545287775', 'A,B,C'),
        ('S002', 'Jane Smith', '0987654321', 'B,C,A'),
        ('S003', 'Alice Johnson', '5555555555', 'C,B,A'),
        ('S004', 'Bob Brown', '4444444444', 'A,A,B'),
        ('S005', 'Charlie White', '3333333333', 'B,C,B'),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO students (index_number, name, phone, grades)
        VALUES (?, ?, ?, ?)
    ''', sample_data)
    conn.commit()
    conn.close()
    

create_table()
insert_sample_data()


