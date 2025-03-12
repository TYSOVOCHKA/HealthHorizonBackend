import os
from g4f.client import AsyncClient
import sqlite3
from dotenv import load_dotenv


load_dotenv()


class DeepSeekEntity:
    def __init__(self):
        self.API_KEY = os.getenv("AI_API_KEY")

    
    @staticmethod
    def get_user_characteristics(login: str) -> tuple:
        conn = sqlite3.connect('users_data.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT login, height, weight, gender, location, activities, diseases, cooking_time, goal, budget, food_preferences,
                       allergies, supplements, lifestyle, workout_schedule
        FROM users_characteristics
        WHERE login = ?""", (login,))
        user_charact = cursor.fetchone()
        conn.close()
        return user_charact
    

    @staticmethod
    def get_user_prompt(profile: tuple) -> str:
        profile_data = {
        "height": profile[1],
        "weight": profile[2],
        "gender": profile[3],
        "location": profile[4],
        "activities": profile[5],
        "diseases": profile[6],
        "cooking_time": profile[7],
        "goal": profile[8],
        "budget": profile[9],
        "food_preferences": profile[10],
        "allergies": profile[11],
        "supplements": profile[12],
        "lifestyle": profile[13],
        "workout_schedule": profile[14]
    }
        
        prompt = f"""
        Составь подробный план питания на неделю с учётом следующих параметров:

        - **Рост:** {profile_data['height']} см
        - **Вес:** {profile_data['weight']} кг
        - **Пол:** {profile_data['gender']}
        - **Локация:** {profile_data['location']} – учти актуальные цены на продукты в этом регионе
        - **Уровень активности:** {profile_data['activities']}
        - **Наличие заболеваний:** {profile_data['diseases']}
        - **Время на готовку:** {profile_data['cooking_time']}
        - **Цель питания:** {profile_data['goal']}
        - **Бюджет:** {profile_data['budget']}
        - **Пищевые предпочтения:**
            - {profile_data['food_preferences']}
        - **Аллергии:** {profile_data['allergies']}
        - **Использование БАДов:** {profile_data['supplements']}
        - **Образ жизни:** {profile_data['lifestyle']}
        - **График тренировок:** {profile_data['workout_schedule']}

        На основе этих данных предоставь:

        1. Рацион на неделю с разбивкой по дням и приёмам пищи.
        2. Калорийность и соотношение Б/Ж/У в день.
        3. Советы по приготовлению, если время ограничено.
        4. Удобные варианты перекусов для поддержания энергии.
        5. Сколько примерно это будет стоить.

        Обязательно отвечай только на русском языке!
        """
        return prompt


    async def generate_user_receipt(self, login: str) -> str:
        user_charact = self.get_user_characteristics(login)
        prompt = self.get_user_prompt(user_charact)
        try:
            client = AsyncClient()     
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                web_search = False,
            )
            return (response.choices[0].message.content, 200)
        except Exception as error:
            return (error, 400)
        

async def ai_main(user_id):
    deep = DeepSeekEntity()
    receipt = await deep.generate_user_receipt(user_id)
    return receipt