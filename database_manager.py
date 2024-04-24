import sqlite3
import random

conn = sqlite3.connect('inventory.db')


def create_table():
    conn.execute('''CREATE TABLE IF NOT EXISTS inventars(
                preces_id INTEGER,
                nosaukums TEXT,
                apjoms INTEGER,
                nepieciesamais_apjoms INTEGER)''')
    
    conn.commit()

def check_inventory():
    cursor = conn.cursor()

    all_data = cursor.execute('''SELECT * FROM inventars''')
    rows = cursor.fetchall()
    return rows


def add_item(nosaukums, apjoms, nepieciesamais_apjoms):
    item_id = random.randint(100000, 999999)

    conn.execute('''INSERT INTO inventars VALUES (?,?,?,?)''', 
                 (item_id, nosaukums, apjoms, nepieciesamais_apjoms))

    conn.commit()


def delete_item(id):
    item_id = random.randint(100000, 999999)

    conn.execute('''DELETE FROM inventars WHERE preces_id = (?) ''', 
                 (id,))

    conn.commit()


def edit_item(produkta_id, nosaukums, apjoms, nepieciesamais_apjoms):
    cursor = conn.cursor()

    cursor.execute('''UPDATE inventars SET 
                        nosaukums = ?,
                        apjoms = ?,
                        nepieciesamais_apjoms = ?
                        WHERE preces_id = ?''', 
                        (nosaukums, apjoms, nepieciesamais_apjoms, produkta_id))

    conn.commit()
    cursor.close()


def authenticate(username_input, password_input):
    cursor = conn.cursor()

    cursor.execute('''SELECT id FROM users WHERE username = ? AND password = ?''', (username_input, password_input))
    data = cursor.fetchall()
    cursor.close()
    if data:
        return data[0][0]
    else:
        return 0


def return_access(user_id):
    cursor = conn.cursor()

    cursor.execute('''SELECT access FROM users WHERE id = ?''', (user_id,))
    access_data = cursor.fetchone()

    access_value = access_data[0]
    access_items = access_value.strip("()'\n").split(';')
    
    cursor.close()
    return access_items
