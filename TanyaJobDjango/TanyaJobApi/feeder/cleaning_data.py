import requests
import json
import MySQLdb
import re


with open('config.json') as data_file:
    config = json.load(data_file)

db = MySQLdb.connect(
    host=config["tanyajob_db"]["host"],
    user=config["tanyajob_db"]["user"],
    passwd=config["tanyajob_db"]["passwd"],
    db="tanyajob_chat")


cur = db.cursor()
cur.execute("SELECT title FROM tanyajob_chat.job_job GROUP BY title;")

removed_words = ["Jakarta", "Area", "Jember","Semarang", "Jember", "Walk in Interview","Batch", "Viii","Yogyakarta","Surabaya", "Barat", "Jogja", "Tangerang", "Selatan","Pt Indosurya Finance", "PT", "Depok","Karawang", "Cibubur", "Bekasi", "Rembang", "Dki", "Alam Sutera","Bandung", "Boyolali","Cililitan","Cibinong", "Cibubur", "Citraland Mall", "Depok","Emporium Pluit Mall", "Makasar", "Samarinda", "Semarang","Pt Star Cosmos","Jawa Tengah", ",","Cilegon", "Pusat", "Di Mall Ambasador", "Di Depok Town Square","Depok Town Square", "Di Bec - Bandung","Jawa","Tengah"," - ", " , ", "Banyuwangi", "Kediri", "Tulungagung", "Trenggalek", "Dan Sekitarnya", "Tarakan","for Bod", "Interview", "Langsung","1","2","3","4","5","6","7","8","9","Bank Cimb Niaga Jabodetabek","Cimb","Jabodetabek","Cianjur","Solo","Di Pusat Grosir Cililitan","Grosir","Jatim","- ", "Penempatan", " : ",
"Cabang", "Palembang","Balikpapan","Kota /Riau","Traveloka","Bogor","Denpasar","Bali","Bca","Bank Swasta","Palu",":","Bank Sampoerna","Makasar","Bengkulu","Purwokerto","dan "," Dan "," & ","Bogor","Di Mangga Dua Mall","Loker","Lowongan Kerja","Di Supermall Karawaci","Karawaci"," and "," And ","Delivery Sub Agen Jne Berau","Traveloka","Bengkulu","Pontianak","Sanggau","Lamongan","Bojonegoro","Kalimantan","Kalimantan Timur","Dept.Makishinko","Dept.Nitto Kohki","Dept.Tone","Div.Nitto Wil.","Bali","Bank Niaga","Pekanbaru","Patisserie","Sukabumi","Timur","Global Intrima","Pati ","Yogya","Maybank","Mataram","Papua","Pt. Trisula Prima Agung","Pt Epson Cikarang","Cikarang","Pt Epson","Kendari","Wilayah","Ciledug","Magang"]

replaced_words = [["Manager", "Manajer"],["Sr.", "Senior"], ["Jr.", "Junior"], ["Staf ", "Staff "],["Teacher","Teacher "],["Teachers", "Teacher"],["Technician","Teknisi"]]

count = 0
f= open("sql_update.sql","w+")
for row in cur.fetchall():
    count += 1
    original_title = row[0]
    cleaned_title = original_title.strip()
    if '(' in cleaned_title and ')' in cleaned_title:
        start = cleaned_title.index('(')
        end = cleaned_title.index(')')
        cleaned_title = cleaned_title.replace(cleaned_title[start:end+1], "")
    if '(' in cleaned_title and ')' in cleaned_title:
        start = cleaned_title.index('(')
        end = cleaned_title.index(')')
        cleaned_title = cleaned_title.replace(cleaned_title[start:end+1], "")
    if '[' in cleaned_title and ']' in cleaned_title:
        start = cleaned_title.index('[')
        end = cleaned_title.index(']')
        cleaned_title = cleaned_title.replace(cleaned_title[start:end+1], "")

    for w in removed_words:
        cleaned_title = cleaned_title.replace(w, "")

    for w in replaced_words:
        cleaned_title = cleaned_title.replace(w[0], w[1])
    cleaned_title = cleaned_title.strip()
    cleaned_title = cleaned_title.replace("  ", " ")
        

    print original_title
    print cleaned_title

    query = "UPDATE tanyajob_chat.job_job SET title = '" + cleaned_title +"' WHERE title = '" + original_title + "';"
    f.write(query)
    cur.execute(query)
    db.commit()
    print "-----------------------------------------"
print count
f.close() 
