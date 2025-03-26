import sqlite3
from io import BytesIO
import matplotlib as plt
import pandas as pd



def get_goal(login: str) -> str:
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT goal
    FROM users_characteristics
    WHERE login = ?
    ''', (login,))
    
    goal = cursor.fetchone()[0]
    return goal


def get_user_notes(login: str) -> dict:
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
    
    # response_data = {
    #     "feels": rows[0],
    #     "cost": rows[1],
    #     "weight": rows[2],
    #     "water": rows[3],
    #     "created_at": rows[4]
    # }
    
    # return response_data

    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['wellbeing', 'weight', 'expenses', 'created_at'])
    df['created_at'] = pd.to_datetime(df['created_at'])
    return df


def plot_user_notes(notes_df, goal: str):
    if goal == "Жиросжигание":
        notes_df['productivity'] = notes_df['wellbeing'] / (notes_df['weight'] + notes_df['expenses'])
    elif goal == "Набор массы":
        notes_df['productivity'] = notes_df['wellbeing'] / (notes_df['weight'] - notes_df['weight'] + 10)
    elif goal == "Поддержание формы":
        notes_df['productivity'] = notes_df['wellbeing'] / (notes_df['weight'] + 10 - notes_df['weight'])
    else:
        notes_df['productivity'] = notes_df['wellbeing']


    plt.style.use('seaborn-v0_8-darkgrid')
    plots = {}
    
    # График самочувствия
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(notes_df['created_at'], notes_df['wellbeing'], color='tab:red', marker='o')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Самочувствие')
    ax.set_title('Зависимость самочувствия от даты')
    ax.grid(True)
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plots['wellbeing'] = img_bytes
    plt.close(fig)

    # График веса
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(notes_df['created_at'], notes_df['weight'], color='tab:blue', marker='o')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Вес')
    ax.set_title('Зависимость веса от даты')
    ax.grid(True)
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plots['weight'] = img_bytes
    plt.close(fig)

    # График затрат
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(notes_df['created_at'], notes_df['expenses'], color='tab:green', marker='o')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Затраты')
    ax.set_title('Зависимость затрат от даты')
    ax.grid(True)
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plots['expenses'] = img_bytes
    plt.close(fig)

    # График продуктивности
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(notes_df['created_at'], notes_df['productivity'], color='tab:purple', marker='o')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Продуктивность')
    ax.set_title('Зависимость продуктивности от даты')
    ax.grid(True)
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plots['productivity'] = img_bytes
    plt.close(fig)

    return plots


def get_user_statystics(login: str) -> dict:
    goal = get_goal(login)
    user_notes = get_user_notes(login)
    if goal is None or user_notes is None:
        return
    user_notes["goal"] = goal
    plots = plot_user_notes(user_notes, goal)
    return plots