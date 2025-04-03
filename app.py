import sqlite3
from flask import Flask, request, jsonify
from src.network_service import ai_main
from src.statistics_service import get_user_statystics
from src.user_service import UserService
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

def get_db_connection():
    conn = sqlite3.connect('users_data.db')
    return conn

@app.route("/api/check-user", methods=['POST'])
def check_user():
    data = request.json
    required_attributes = ["login"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    conn = get_db_connection()
    user_service = UserService(conn)
    result = user_service.login_exist(data.get("login"))
    conn.close()
    return jsonify({"message": str(result)}), 200

@app.route("/api/register-user", methods=['POST'])
def registration():
    data = request.json
    required_attributes = ["login", "password"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
        
    login = data.get("login")
    password = data.get("password")

    conn = get_db_connection()
    user_service = UserService(conn)
    if user_service.login_exist(login):
        conn.close()
        return jsonify({"error": "Login already exist!"}), 400
    else:
        if user_service.register_user(login, password):
            conn.close()
            return jsonify({"message": "User registered!"}), 200
        else:
            conn.close()
            return jsonify({"message": "Fatal error"}), 400
    

@app.route("/api/login-user", methods=['POST'])
def login():
    data = request.json
    required_attributes = ["login", "password"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
        
    login = data.get("login")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM users WHERE login = ?', (login,))
    user = cursor.fetchone()

    if user is None:
        conn.close()
        return jsonify({"error": "User not found!"}), 404
    else:
        user_service = UserService(conn)
        if user_service.check_password(password, user[0]):
            user_data = user_service.get_user_data(login)
            conn.close()
            if user_data is None:
                return jsonify({"error": "User profile not found!"}), 404
            return jsonify({"login": login, "data": user_data}), 200
        else:
            conn.close()
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

    characteristics = (login, height, weight, gender, location, activities, diseases, cooking_time, goal, budget, food_preferences, allergies, supplements, lifestyle, workout_schedule)

    conn = get_db_connection()
    user_service = UserService(conn)
    if user_service.login_exist(login):
        user_service.add_user_characteristics(characteristics)
        conn.close()
        return jsonify({"message": "User characteristics received!"}), 200
    else:
        conn.close()
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

    notes = (login, feels, cost, weight, water)
    conn = get_db_connection()
    user_service = UserService(conn)
    user_service.add_user_note(notes)
    conn.close()
    return jsonify({"message": "User note received!"}), 200


@app.route("/api/get-dietplan", methods=['POST'])
async def get_diet_paln():
    data = request.json
    required_attributes = ["login"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    
    login = data.get("login")
    conn = get_db_connection()
    user_service = UserService(conn)
    if user_service.login_exist(login):
        conn.close()
        diet_plan = await ai_main(login)
        if diet_plan[1] == 200:
            return jsonify({"result": diet_plan[0]}), 200
        else:
            return jsonify({"message": "Problem with AI, try again"}), 500
    else:
        conn.close()
        return jsonify({"error": "User not found!"}), 404
    

@app.route("/api/get-statistics", methods=['POST'])
async def get_statystics():
    data = request.json
    required_attributes = ["login"]
    for attr in required_attributes:
        if attr not in data:
            return jsonify({"error": f"{attr} is required!"}), 400
    login = data.get("login")
    user_statystics: dict = get_user_statystics(login)
    if user_statystics is None:
        return jsonify({"error": "create profile or insert it!"}), 400
    return jsonify(user_statystics), 200
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)