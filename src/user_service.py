import sqlite3
import bcrypt

class UserService:
    def __init__(self, database_connection):
        self.conn = database_connection
        self.cursor = database_connection.cursor()

    @staticmethod
    def get_hashed_password(plain_text_password: str):
        byte_password = plain_text_password.encode('utf-8')
        hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
        return hashed_password

    @staticmethod
    def check_password(plain_text_password: str, hashed_password: str):
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')

        byte_password = plain_text_password.encode('utf-8')
        return bcrypt.checkpw(byte_password, hashed_password)

    def get_user_data(self, login: str) -> dict:
        self.cursor.execute('SELECT * FROM users_characteristics WHERE login = ?', (login,))
        user_data = self.cursor.fetchone()
        if user_data is not None:
            return {
                "height": user_data[1],
                "weight": user_data[2],
                "gender": user_data[3],
                "location": user_data[4],
                "activities": user_data[5],
                "diseases": user_data[6],
                "cooking_time": user_data[7],
                "goal": user_data[8],
                "budget": user_data[9],
                "food_preferences": user_data[10],
                "allergies": user_data[11],
                "supplements": user_data[12],
                "lifestyle": user_data[13],
                "workout_schedule": user_data[14]
            }
        return None

    def login_exist(self, login: str) -> bool:
        self.cursor.execute('SELECT 1 FROM users WHERE login = ?', (login,))
        return True if self.cursor.fetchone() is not None else False

    def register_user(self, login, password):
        try:
            self.cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, self.get_hashed_password(password)))
            self.conn.commit()
            return True
        except Exception as error:
            print(error)
            return False

    def add_user_characteristics(self, characteristics: tuple) -> bool:
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO users_characteristics (
                    login, height, weight, gender, location, activities, diseases, 
                    cooking_time, goal, budget, food_preferences, allergies, 
                    supplements, lifestyle, workout_schedule)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, characteristics)
            self.conn.commit()
            return True
        except Exception as error:
            print(error)
            return False
        
    
    def get_attr_info(self, attr, login):
        self.cursor.execute(f'SELECT {attr} from users_characteristics WHERE login = ?', (login,))
        user_data = self.cursor.fetchone()
        if user_data is not None:
            return user_data[0]
        return None

    def add_user_note(self, notes: tuple) -> bool:
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO users_note (
                    login, feels, cost, weight, water)
                VALUES (?, ?, ?, ?, ?)
                """, notes)
            self.conn.commit()
            return True
        except Exception as error:
            print(error)
            return False