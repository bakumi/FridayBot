import sqlite3
from aiogram.fsm.state import State, StatesGroup



#################### admin database ####################

class AddInfo(StatesGroup):
    new_post = State()
    photo = State()
    description = State()
    button_1 = State()
    button_2 = State()
    button_3 = State()
    symbol = State()
    edit_photo = State()
    edit_description = State()
    edit_button_1 = State()
    edit_button_2 = State()
    edit_button_3 = State()
    edit_symbol = State()
        

class Admindb:
    def __init__(self) -> None:
        self.dp = sqlite3.connect("admin_db.db")
        self.cur = self.dp.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS admin_table(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         photo BLOB,
                         description TEXT,
                         symbol TEXT)''')
        self.dp.commit()
        self.add_missing_columns()


    def add_missing_columns(self):
        existing_columns = [row[1] for row in self.cur.execute("PRAGMA table_info(admin_table)")]
        columns_to_add = {
            "button_1": "TEXT",
            "button_2": "TEXT",
            "button_3": "TEXT",
            "correct_button": "INTEGER"
        }
        for column, column_type in columns_to_add.items():
            if column not in existing_columns:
                self.cur.execute(f"ALTER TABLE admin_table ADD COLUMN {column} {column_type}")
        self.dp.commit()


    def add_info(self, photo, description, symbol, button_1, button_2, button_3, correct_button):
        self.cur.execute("""INSERT INTO admin_table (photo, description, symbol, button_1, button_2, button_3, correct_button)
                            VALUES (?, ?, ?, ?, ?, ?, ?)""", (photo, description, symbol, button_1, button_2, button_3, correct_button))
        self.dp.commit()


    def get_info(self):
        self.cur.execute("""SELECT photo, description, symbol, button_1, button_2, button_3, correct_button FROM admin_table ORDER BY id DESC LIMIT 1""")
        return self.cur.fetchone()


    def update_info(self, column, value):
        self.cur.execute(f"UPDATE admin_table SET {column} = ? WHERE id = (SELECT MAX(id) FROM admin_table)", (value,))
        self.dp.commit()


admin_db = Admindb()

saved_post_data = None


def save_post_data(data):
    global saved_post_data
    saved_post_data = data

def get_saved_post_data():
    return admin_db.get_info()

#################### admin database ####################



#################### users database ####################

class Userdb:
    def __init__(self) -> None:
        self.dp = sqlite3.connect("user_db.db")
        self.cur = self.dp.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user_table(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER,
                         username TEXT)''')
        self.dp.commit()
        self.add_missing_columns()


    def add_missing_columns(self):
        existing_columns = [row[1] for row in self.cur.execute("PRAGMA table_info(user_table)")]
        if 'correct_button' not in existing_columns:
            self.cur.execute("ALTER TABLE user_table ADD COLUMN correct_button INTEGER")
        self.dp.commit()


    def add_user(self, user_id, username, correct_button):
        self.cur.execute("""INSERT INTO user_table (user_id, username, correct_button)
                            VALUES (?, ?, ?)""", (user_id, username, correct_button))
        self.dp.commit()


user_db = Userdb()

#################### users database ####################