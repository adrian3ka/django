import requests

url = "http://localhost:8000/api/user_answers/"

payload = ['{"category": "Degree","text": "Pendidikan terakhir saya {{x}}"}',
           '{"category": "Degree","text": "{{x}}"}',
           '{"category": "Degree","text": "Saya lulusan {{x}}"}',
           '{"category": "Degree","text": "Tingkat pendidikan terkahir saya {{x}}"}',
           '{"category": "Degree","text": "Jenjang Pendidikan terakhir saya {{x}}"}',
           '{"category": "Major","text": "Kamu kuliah dijurusan apa {{x}}"}']
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "9ad5e836-84cb-401e-9021-bc28552d4964"
    }


for p in payload:
    print p
    response = requests.request("POST", url, data=p, headers=headers)

    print(response.text)
