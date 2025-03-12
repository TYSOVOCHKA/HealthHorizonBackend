# Flask API for User Management and Diet Plan

This Flask API provides endpoints to manage user data, characteristics, notes, and to generate a diet plan. It uses SQLite for data storage and bcrypt for password hashing.

## API Endpoints

### `/api/check-user` [POST]

Checks if a user exists.

**Request:**
```json
{
    "login": "example_login"
}
```

**Response:**
```json
{
    "message": "True/False"
}
```

### `/api/register-user` [POST]

Registers a new user.

**Request:**
```json
{
    "login": "example_login",
    "password": "example_password"
}
```

**Response:**
```json
{
    "message": "User registered!"
}
```

### `/api/login-user` [POST]

Logs in a user and retrieves their profile data.

**Request:**
```json
{
    "login": "example_login",
    "password": "example_password"
}
```

**Response:**
```json
{
    "login": "example_login",
    "data": {
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
}
```

### `/api/add-user-characteristics` [POST]

Adds or updates user characteristics.

**Request:**
```json
{
    "login": "example_login",
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
```

**Response:**
```json
{
    "message": "User characteristics received!"
}
```

### `/api/add-note` [POST]

Adds a user note.

**Request:**
```json
{
    "login": "example_login",
    "feels": 8,
    "cost": 500,
    "weight": 70,
    "water": 2
}
```

**Response:**
```json
{
    "message": "User note received!"
}
```

### `/api/get-dietplan` [POST]

Generates a diet plan for the user based on their characteristics.

**Request:**
```json
{
    "login": "example_login"
}
```

**Response:**
```json
{
    "result": "Diet plan details..."
}
```

### `/api/get-statystics` [POST]

(Endpoint description and functionality not provided in the original code)