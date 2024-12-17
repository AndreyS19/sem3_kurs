import requests
import json
from pattern import get_patt_data, get_headers
from pathlib import Path
def get_var(key):# получения переменных из json
    path = Path("C:/Users/79659/Desktop/Питон_проекты/ya-gpt-chatbot-main/app/json_files/varData.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get(key)
def data_set(userid,text, role):# загрузка данных о сообщениях в json-файл сообщений
    path = Path(get_var("path"))
    data = json.loads(path.read_text(encoding="utf-8"))
    for currId in data["users"]:
        if currId.get("id") == userid:
            # Добавление сообщения в список messages
            currId["messages"].append({"role": role, "text": text})
            break
    else:
        # Если пользователь не найден, добавляем его в список users
        data["users"].append({
            "id": userid,
            "messages": [{"role": role, "text": text}]
        })
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

def data_reset(userid):# удаление данных о сообщениях пользователя из json файла при нажатии кнопки завершения диалога
    path = Path(get_var("path"))
    data = json.loads(path.read_text(encoding="utf-8"))
    for currId in data["users"]:
        if currId["id"] == userid:
            # Удаление сообщений из списка messages
            currId["messages"] = []
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            break
        else:
            print("История сообщений пуста")
def data_reset_closing():# удаление данных о сообщения пользователя из json файла при завершении работы программы
    path = Path(get_var("path"))
    data = json.loads(path.read_text(encoding="utf-8"))
    for currId in data["users"]:
        # Удаление сообщений из списка messages
        currId["messages"] = []
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
def send_message(message: str):# отправление сообщений в пром-режиме
    data = get_patt_data(get_var("sa_id"))
    data["messages"].append({"role": "user","text": message})
    print(data)
    response = requests.post(get_var("url"), json=data, headers=get_headers(get_var("apikey"),get_var("sa_id")))
    return response
def send_message_dialogue(userid):# отправление сообщений в режиме диалога
    data = get_patt_data(get_var("sa_id"))
    path = Path(get_var("path"))
    json_data = json.loads(path.read_text(encoding="utf-8"))
    for currId in json_data["users"]:
        if currId.get("id") == userid:
            # Добавление сообщения в список messages
            data["messages"].extend(currId["messages"])

            print(json.dumps(data, indent=4, sort_keys=True))
            break
    response = requests.post(get_var("url"), json=data, headers=get_headers(get_var("apikey"),get_var("sa_id")))
    return response
def extract_text(response):# получение текста из полученных от гпт значений
    print(response.text)
    data = json.loads(response.text)
    try:
        # Получение значения поля text из блока message
        text = data['result']['alternatives'][0]['message']['text']
    except KeyError:
        text = "Ошибка"
    return text