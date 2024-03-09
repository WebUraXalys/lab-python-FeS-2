import sqlite3


def create_table(cursor) -> None:
    """
    This function creates a table named Note if it isn't existing.
    """
    cursor.execute("DROP TABLE IF EXISTS Note")
    query = """CREATE TABLE Note(
            ID INT PRIMARY KEY NOT NULL,
            NAME CHAR(20) NOT NULL, 
            DATE DATETIME,
            NOTE CHAR(150))"""
    cursor.execute(query)


def display_menu() -> str:
    """
    This function displays a menu to the user and returns the choice.
    """
    print("1. Add record")
    print("2. Change record")
    print("3. Delete record")
    print("4. Show database")
    print("5. Exit")
    choice = input("Choose an option: ")
    return choice


def add_record(conn, cursor, input_string) -> None:
    """
    This function allows the user to add a new record to the database.
    """
    parts = input_string.split(',')
    if len(parts) == 4:  
        id, name, date_str, note = parts
        id = int(id.strip())
        name = name.strip()
        date_str = date_str.strip()
        note = note.strip()


        try:
            import datetime
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Error: Date should be in format YYYY-MM-DD HH:MM:SS")
            return

        cursor.execute("SELECT * FROM Note WHERE ID = ?", (id,))
        existing_record = cursor.fetchone()
        if existing_record:
            print("Error: Record with ID {} already exists.".format(id))
        else:
            conn.execute("INSERT INTO Note (ID, NAME, DATE, NOTE) VALUES (?, ?, ?, ?)", (id, name, date, note))
            conn.commit()
    else:
        print("Invalid input format. Please provide ID, Name, Date, and Note separated by commas.")


def update_record(conn, cursor) -> None:
    """
    This function allows the user to update a record in the database.
    """
    id = int(input("Enter ID of note you want to change: "))
    note = input("Enter new note: ")
    conn.execute("UPDATE Note SET NOTE = ? WHERE ID = ?", (note, id))
    conn.commit()


def delete_record(conn, cursor) -> None:
    """
    This function allows the user to delete a record from the database.
    """
    id = int(input("Enter ID of note you want to delete: "))
    conn.execute("DELETE FROM Note WHERE ID = ?", (id,))
    conn.commit()


def show_records(cursor) -> None:
    """
    This function displays all records in the Note table.
    """
    cursor.execute("SELECT * FROM Note")
    records = cursor.fetchall()
    for record in records:
        print(record)


conn = sqlite3.connect('notebook.db')
cursor = conn.cursor()

create_table(cursor)

while True:
    choice = display_menu()
    if choice == '1':
        input_string = input("Enter ID, Name, Date (YYYY-MM-DD HH:MM:SS), Note separated by commas: ")
        add_record(conn, cursor, input_string)
    elif choice == '2':
        update_record(conn, cursor)
    elif choice == '3':
        delete_record(conn, cursor)
    elif choice == '4':
        show_records(cursor)
    elif choice == '5':
        break
    else:
        print("Invalid choice")

cursor = conn.execute("SELECT * FROM Note")
print(cursor.fetchall())

conn.close()
