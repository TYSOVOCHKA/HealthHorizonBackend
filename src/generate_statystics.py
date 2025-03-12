# import sqlite3



# def get_goal(user_id):
#     conn = sqlite3.connect('users_data.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#     SELECT goal
#     FROM profiles
#     WHERE user_id = ?
#     ''', (user_id,))
    
#     goal = cursor.fetchone()[0]
#     return goal


# def get_user_notes(user_id):
#     conn = sqlite3.connect('users_data.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT wellbeing, weight, expenses, created_at
#         FROM notes
#         WHERE user_id = ?
#     ''', (user_id,))
    
#     rows = cursor.fetchall()
    
#     # df = pd.DataFrame(rows, columns=['wellbeing', 'weight', 'expenses', 'created_at'])
#     # df['created_at'] = pd.to_datetime(df['created_at'])
#     # return df
#     print(rows)

# get_user_notes()