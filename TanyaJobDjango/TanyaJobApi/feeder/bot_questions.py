import requests

url = "http://localhost:8000/api/bot_questions/"

payload = ['{"category": "Age","text": "Umur kamu berapa?"}',
           '{"category": "Major","text": "Kamu kuliah di jurusan apa?"}']
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "9ad5e836-84cb-401e-9021-bc28552d4964"
    }


for p in payload:
    print p
    response = requests.request("POST", url, data=p, headers=headers)

    print(response.text)
