import sqlite3



def get_goal(login):
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT goal
    FROM users_characteristics
    WHERE login = ?
    ''', (login,))
    
    goal = cursor.fetchone()[0]
    return goal


def get_user_notes(login):
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT feels, cost, weight, water, created_at
        FROM users_note
        WHERE login = ?
    ''', (login,))
    
    rows = cursor.fetchall()[0]

    if rows is None:
        return
    
    response_data = {
        "feels": rows[0],
        "cost": rows[1],
        "weight": rows[2],
        "water": rows[3],
        "created_at": rows[4]
    }
    
    return response_data


def get_user_statystics(login: str) -> dict:
    goal = get_goal(login)
    user_notes = get_user_notes(login)
    if goal is None or user_notes is None:
        return
    user_notes["goal"] = goal
    return user_notes