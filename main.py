import tkinter as tk
from tkinter import messagebox
import requests
import os
from dotenv import load_dotenv

load_dotenv() 
API_KEY = os.getenv("WEATHERAPI_KEY") 
BASE_URL = "http://api.weatherapi.com/v1"

#ФУНКЦИЯ ПОЛУЧЕНИЯ ПОГОДЫ

def get_weather(city):
    """
    Получает текущую погоду для указанного города, используя WeatherAPI.com.
    """
    if not API_KEY:
        messagebox.showerror("Ошибка", "Ключ API (WEATHERAPI_KEY) не найден. Проверьте ваш файл .env.")
        return None
    
    complete_url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}&lang=ru"
    
    try:
        response = requests.get(complete_url)
        response.raise_for_status() 
        data = response.json()
        
        if "error" in data:
            messagebox.showerror("Ошибка API", data["error"]["message"])
            return None

        city_name = data["location"]["name"]
        temperature = data["current"]["temp_c"] 
        description = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_kph"]
        
        # Форматирование результата
        result = (
            f"--- Погода в {city_name} ---\n"
            f"Температура: {temperature}°C\n"
            f"Описание: {description.capitalize()}\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} км/ч"
        )
        return result

    except requests.exceptions.HTTPError as e:
        # Специальная обработка для ошибки 401 
        if response.status_code == 401:
            messagebox.showerror("Ошибка 401", "Неверный API-ключ. Проверьте ключ в .env.")
        else:
            messagebox.showerror("Ошибка HTTP", f"Ошибка HTTP: {e}")
        return None
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка сети", f"Ошибка при подключении: {e}")
        return None
    except Exception as e:
        messagebox.showerror("Непредвиденная ошибка", f"Произошла ошибка: {e}")
        return None


def search_weather():
    """Обрабатывает ввод пользователя и отображает результаты погоды."""

    city = city_entry.get().strip() 
    
    if not city:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите название города.")
        result_label.config(text="Ожидание ввода города...")
        return

    weather_info = get_weather(city)
    if weather_info:
        result_label.config(text=weather_info)


# НАСТРОЙКА ГЛАВНОГО ОКНА И ЗАПУСК 

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Система Управления Погодой")
    app.geometry("400x380") 
    app.resizable(False, False) 

    
    tk.Label(app, text="Введите город:", font=('Arial', 12)).pack(pady=10)
    
    city_entry = tk.Entry(app, width=30, font=('Arial', 12))
    city_entry.pack(pady=5, padx=20)
    # Привязка кнопки Enter к функции поиска
    city_entry.bind('<Return>', lambda event: search_weather()) 
    
    
    search_button = tk.Button(app, text="Узнать Погоду", command=search_weather, 
                              bg='#303F9F', fg='white', font=('Arial', 11, 'bold'))
    search_button.pack(pady=10)

    # Метка для отображения результата
    result_label = tk.Label(app, text="Введите город и нажмите 'Узнать Погоду'", 
                            justify=tk.LEFT, fg='#303F9F', wraplength=350,
                            font=('Arial', 11))
    result_label.pack(pady=15, padx=20)

    # Кнопка для выхода
    exit_button = tk.Button(app, text="Выход из Программы", command=app.destroy, 
                            bg='#D32F2F', fg='white', font=('Arial', 11))
    exit_button.pack(pady=10)

    app.mainloop()