import sqlite3
import random

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS inventars(
                    preces_id INTEGER,
                    nosaukums TEXT UNIQUE,
                    apjoms INTEGER,
                    nepieciesamais_apjoms INTEGER)''')
        
        self.conn.commit()

    def check_inventory(self):
        cursor = self.conn.cursor()

        cursor.execute('''SELECT * FROM inventars''')
        rows = cursor.fetchall()
        return rows


    def add_item(self, nosaukums, apjoms, nepieciesamais_apjoms):
        item_id = random.randint(100000, 999999)

        self.conn.execute('''INSERT INTO inventars VALUES (?,?,?,?)''', 
                    (item_id, nosaukums, apjoms, nepieciesamais_apjoms))

        self.conn.commit()


    def delete_item(self, id):
        self.conn.execute('''DELETE FROM inventars WHERE preces_id = (?) ''', 
                    (id,))

        self.conn.commit()


    def edit_item(self, produkta_id, nosaukums, apjoms, nepieciesamais_apjoms):
        cursor = self.conn.cursor()

        cursor.execute('''UPDATE inventars SET 
                            nosaukums = ?,
                            apjoms = ?,
                            nepieciesamais_apjoms = ?
                            WHERE preces_id = ?''', 
                            (nosaukums, apjoms, nepieciesamais_apjoms, produkta_id))

        self.conn.commit()
        cursor.close()


    def authenticate(self, username_input, password_input):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id FROM users WHERE username = ? AND password = ?''', (username_input, password_input))
        data = cursor.fetchall()
        cursor.close()
        if data:
            return data[0][0]
        else:
            return 0


    def return_access(self, user_id):
        cursor = self.conn.cursor()

        cursor.execute('''SELECT access FROM users WHERE id = ?''', (user_id,))
        access_data = cursor.fetchone()

        access_value = access_data[0]
        access_items = access_value.strip("()'\n").split(';')
        
        cursor.close()
        return access_items


class UserManager(Database):
    def __init__(self):
        super().__init__()

    def authenticate(self, username_input, password_input):
        return super().authenticate(username_input, password_input)

    def return_access(self, user_id):
        access_items = super().return_access(user_id)
        return access_items
    

class UserRegistration(Database):
    def __init__(self):
        super().__init__()

    def register_user(self, username, password, access):
        user_id = random.randint(1000, 9999)
        self.conn.execute('''INSERT INTO users VALUES (?,?,?)''', (user_id, username, password, access))
        self.conn.commit()

    def display_users(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM users''')
        users = cursor.fetchall()
        cursor.close()

