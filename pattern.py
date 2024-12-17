def get_headers(apikey,id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {apikey}',
        'x-folder-id': id
    }
    return headers
def get_patt_data(id):
    data = {
        "modelUri": f"gpt://{id}/yandexgpt-32k/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.8,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты-учитель по программированию, отвечай только на вопросы по программированию, на все остальные вопросы отвечай: этот вопрос не относится к моему функционалу"
            }
        ]

    }
    return data