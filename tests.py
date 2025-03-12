import requests

BASE_URL = "http://127.0.0.1:5000"
HEADERS = {
    "Content-Type": "application/json"
}

def test_check_user():
    payload = {"login": "test_user"}
    response = requests.post(f"{BASE_URL}/api/check-user", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert "message" in response.json()

def test_register_user():
    payload = {"login": "test_user", "password": "test_password"}
    response = requests.post(f"{BASE_URL}/api/register-user", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "User registered!"

def test_login_user():
    payload = {"login": "test_user", "password": "test_password"}
    response = requests.post(f"{BASE_URL}/api/login-user", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert "login" in response.json()
    assert "data" in response.json()

def test_add_user_characteristics():
    payload = {
        "login": "test_user",
        "height": 175,
        "weight": 70,
        "gender": "male",
        "location": "City, Country",
        "activities": "running",
        "diseases": "none",
        "cooking_time": 30,
        "goal": "weight loss",
        "budget": 1000,
        "food_preferences": "vegan",
        "allergies": "nuts",
        "supplements": "vitamin D",
        "lifestyle": "active",
        "workout_schedule": "Monday, Wednesday, Friday"
    }
    response = requests.post(f"{BASE_URL}/api/add-user-characteristics", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "User characteristics received!"

def test_add_note():
    payload = {
        "login": "test_user",
        "feels": 8,
        "cost": 500,
        "weight": 70,
        "water": 2
    }
    response = requests.post(f"{BASE_URL}/api/add-note", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "User note received!"

def test_get_dietplan():
    payload = {"login": "test_user"}
    response = requests.post(f"{BASE_URL}/api/get-dietplan", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert "result" in response.json()

def test_get_statistics():
    payload = {"login": "test_user"}
    response = requests.post(f"{BASE_URL}/api/get-statystics", headers=HEADERS, json=payload)
    assert response.status_code == 200

if __name__ == "__main__":
    test_check_user()
    test_register_user()
    test_login_user()
    test_add_user_characteristics()
    test_add_note()
    test_get_dietplan()
    test_get_statistics()