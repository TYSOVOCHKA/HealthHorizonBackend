import sqlite3
from flask import Flask, request, jsonify
from src.ai_api import ai_main
import bcrypt


app = Flask(__name__)


def init_db() -> None:
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        login TEXT UNIQUE,
        password TEXT)
    """)
    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users_characteristics(
        login TEXT UNIQUE,
        height INTEGER,
        weight INTEGER,
        gender TEXT,
        location TEXT,
        activities TEXT,
        diseases TEXT,
        cooking_time TEXT,
        goal TEXT,
        budget INTEGER,
        food_preferences TEXT,
        allergies TEXT,
        supplements TEXT,
        lifestyle TEXT,
        workout_schedule TEXT
    )     
    """)
    conn.commit()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users_note(
        login TEXT,
        feels INTEGER,
        cost INTEGER,
        weight INTEGER,
        water INTEGER,
        created_at TEXT DEFAULT (datetime('now', 'localtime'))
    )
    """)
    conn.commit()
    conn.close()

init_db()


def get_hashed_password(plain_text_password):
    byte_password = plain_text_password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def check_password(plain_text_password, hashed_password):
    byte_password = plain_text_password.encode('utf-8')
    return bcrypt.checkpw(byte_password, hashed_password)

def login_exist(login: str) -> bool:
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE login = ?', (login,))
    return True if cursor.fetchone() is not None else False

def get_user_data(login: str) -> dict:
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users_characteristics WHERE login = ?', (login,))
    user_data = cursor.fetchone()
    conn.close()
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


@app.route("/api/check-user", methods=['POST'])
def check_user():
    data = request.json
    required_attributes = ["login"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    return jsonify({"message": str(login_exist(data.get("login")))}), 200


@app.route("/api/register-user", methods=['POST'])
def registration():
    data = request.json
    required_attributes = ["login", "password"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
        
    login = data.get("login")
    password = data.get("password")

    if login_exist(login):
        return jsonify({"error": "Login already exist!"}), 400
    else:
        conn = sqlite3.connect('users_data.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, get_hashed_password(password)))
        conn.commit()
        conn.close()

        return jsonify({"message": "User registered!"}), 200
    

@app.route("/api/login-user", methods=['POST'])
def login():
    data = request.json
    required_attributes = ["login", "password"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
        
    login = data.get("login")
    password = data.get("password")

    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM users WHERE login = ?', (login,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "User not found!"}), 404
    else:
        if check_password(password, user[0]):
            user_data = get_user_data(login)
            if user_data is None:
                return jsonify({"error": "User profile not found!"}), 404
            return jsonify({"login": login, "data": user_data}), 200
        else:
            return jsonify({"error": "Wrong password!"}), 400


@app.route("/api/add-user-characteristics", methods=['POST'])
async def add_user_characteristics():
    data = request.json
    required_attributes = ["login", "height", "weight", "gender", "location", "activities", "diseases",
    "cooking_time", "goal", "budget", "food_preferences", "allergies", "supplements", "lifestyle", "workout_schedule"]

    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    
    login = data.get("login")
    height = data.get("height")
    weight = data.get("weight")
    gender = data.get("gender")
    location = data.get("location")
    activities = data.get("activities")
    diseases = data.get("diseases")
    cooking_time = data.get("cooking_time")
    goal = data.get("goal")
    budget = data.get("budget")
    food_preferences = data.get("food_preferences")
    allergies = data.get("allergies")
    supplements = data.get("supplements")
    lifestyle = data.get("lifestyle")
    workout_schedule = data.get("workout_schedule")

    if login_exist(login):
        conn = sqlite3.connect('users_data.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO users_characteristics (
            login, height, weight, gender, location, activities, diseases, 
            cooking_time, goal, budget, food_preferences, allergies, 
            supplements, lifestyle, workout_schedule)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, 
            (login, height, weight, gender, location, activities, diseases, cooking_time, goal, budget, food_preferences, allergies, supplements, lifestyle, workout_schedule)) 
        conn.commit()
        conn.close()  
    
        return jsonify({"message": "User characteristics received!"}), 200
    else:
        return jsonify({"error": "User not found!"}), 404


@app.route("/api/add-note", methods=['POST'])
async def add_user_note():
    data = request.json
    required_attributes = ["login", "feels", "cost", "weight", "water"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    
    login = data.get("login")
    feels = data.get("feels")
    cost = data.get("cost")
    weight = data.get("weight")
    water = data.get("water")

    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO users_note (
        login, feels, cost, weight, water)
    VALUES (?, ?, ?, ?, ?)
    """, 
        (login, feels, cost, weight, water)) 
    conn.commit()
    conn.close()  
    
    return jsonify({"message": "User note received!"}), 200


@app.route("/api/get-dietplan", methods=['POST'])
async def get_diet_paln():
    data = request.json
    required_attributes = ["login"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    
    if login_exist(data.get("login")):
        diet_plan = await ai_main(data.get("login"))
        if diet_plan[1] == 200:
            return jsonify({"result": diet_plan[0]}), 200
        else:
            return jsonify({"message": "Problem with AI, try again"}), 500
    else:
        return jsonify({"error": "User not found!"}), 404
    

@app.route("/api/get-statystics", methods=['POST'])
async def get_statystics():
    data = request.json
    required_attributes = ["login"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)