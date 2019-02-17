import requests

url = "http://localhost:8000/api/bot_questions/"

payload = [
    '{"category": "Age",			"text": "Umur kamu berapa?"}',
    '{"category": "Age",			"text": "Berapa umur kamu?"}',
    '{"category": "Age",			"text": "Berapa umur kamu sekarang?"}',
    '{"category": "Age",			"text": "Sekarang berapa umur kamu?"}',
    '{"category": "Age",			"text": "Tahun ini umur kamu berapa?"}',
    '{"category": "Age",			"text": "Tahun ini berapa umur kamu?"}',
    '{"category": "Age",			"text": "Tahun ini berapa umurmu?"}',
    '{"category": "Age",			"text": "Umur kamu berapa tahun ini?"}',
    '{"category": "Age",			"text": "Berapa umur kamu tahun ini?"}',
    '{"category": "Age",			"text": "Berapa umurmu tahun ini?"}',
    '{"category": "Age",			"text": "Usia kamu berapa?"}',
    '{"category": "Age",			"text": "Berapa usia kamu?"}',
    '{"category": "Age",			"text": "Berapa usia kamu sekarang?"}',
    '{"category": "Age",			"text": "Sekarang berapa usia kamu?"}',
    '{"category": "Age",			"text": "Tahun ini usia kamu berapa?"}',
    '{"category": "Age",			"text": "Tahun ini berapa usia kamu?"}',
    '{"category": "Age",			"text": "Tahun ini berapa usiamu?"}',
    '{"category": "Age",			"text": "Usia kamu berapa tahun ini?"}',
    '{"category": "Age",			"text": "Berapa usia kamu tahun ini?"}',
    '{"category": "Age",			"text": "Berapa usiamu tahun ini?"}',
    '{"category": "Degree",			"text": "Pendidikan terakhir kamu apa?"}',
    '{"category": "Degree",			"text": "Boleh tahu pendidikan terakhir kamu?"}',
    '{"category": "Degree",			"text": "Tingkat pendidikan terakhir kamu apa?"}',
    '{"category": "Degree",			"text": "Jenjang pendidikan terakhir kamu apa?"}',
    '{"category": "Degree",			"text": "Kamu lagi ambil pendidikan tingkat apa?"}',
    '{"category": "SkillSet",			"text": "Coba sebutkan kemampuan kamu apa saja"}',
    '{"category": "SkillSet",			"text": "Coba sebutkan skill set kamu"}',
    '{"category": "SkillSet",			"text": "Nah, aku mau tau dulu nih skill set kamu apa saja"}',
    '{"category": "SkillSet",			"text": "Kamu punya kemampuan apa saja?"}',
    '{"category": "SkillSet",			"text": "Kamu punya keterampilan apa saja?"}',
    '{"category": "SkillSet",			"text": "Kalo keterampilan,kamu bisa apa saja nih?"}',
    '{"category": "SkillSet",			"text": "Menurut kamu, kamu punya skill apa saja?"}',
    '{"category": "SkillSet",			"text": "Mau tau dong skill kamu apa saja nih?"}',
    '{"category": "SkillSet",			"text": "Coba sebutkan hardskill kamu"}',
    '{"category": "SkillSet",			"text": "Boleh sebutin salah satu skill yang kamu miliki ga?"}',
    '{"category": "SkillSet",			"text": "Apa skill yang kamu miliki?"}',
    '{"category": "SkillSet",			"text": "Skill apa yang kamu miliki?"}',
    '{"category": "Major",			"text": "Jurusan kamu apa?"}',
    '{"category": "Major",			"text": "Kalau boleh tahu jurusan kamu apa ya?"}',
    '{"category": "Major",			"text": "Kamu ambil jurusan apa?"}',
    '{"category": "Major",			"text": "Kamu lulusan jurusan apa?"}',
    '{"category": "Major",			"text": "Kamu lagi ambil bidang pendidikan apa?"}',
    '{"category": "Major",			"text": "Peminatan yang kamu ambil dijurusan kamu apa?"}',
    '{"category": "Major",			"text": "Kamu ambil peminatan apa?"}',
    '{"category": "WorkExp",			"text": "Kamu sudah bekerja berapa bulan?"}',
    '{"category": "WorkExp",			"text": "Kamu sudah pernah bekerja berapa bulan?"}',
    '{"category": "WorkExp",			"text": "Berapa bulan kamu bekerja sebelumnya?"}',
    '{"category": "WorkExp",			"text": "Berapa bulan lamanya kamu bekerja sebelumnya?"}',
    '{"category": "WorkExp",			"text": "Sebelumnya, kamu pernah bekerja berapa bulan?"}',
    '{"category": "Position",			"text": "Jabatan terakhir kamu apa?"}',
    '{"category": "Position",			"text": "Apa posisi terakhir yang kamu tempati?"}',
    '{"category": "Position",			"text": "Di tempat kerjamu yang dulu, kamu berada pada posisi sebagai apa?"}',
    '{"category": "Position",			"text": "Apa jenjang karirmu saat ini?"}',
    '{"category": "Position",			"text": "Posisi terakhirmu sebagai apa?"}',
    '{"category": "Position",			"text": "Di tingkat mana posisimu sebelumnya?"}',
    '{"category": "Position",			"text": "Kamu menjabat sebagai apa sebelumnya?"}',
    '{"category": "Position",			"text": "Apa jabatan terakhir yang kamu raih?"}',
    '{"category": "SalaryUpper",		"text": "Berapa gaji maksimum yang kamu inginkan?"}',
    '{"category": "SalaryLower",		"text": "Berapa minimum yang kamu inginkan?"}',
    '{"category": "SalaryUpper",		"text": "Berapa gaji maksimum yang kamu harapkan?"}',
    '{"category": "SalaryLower",		"text": "Berapa gaji minimum yang kamu harapkan?"}',
    '{"category": "SalaryUpper",		"text": "Sebutkan gaji maksimum yang kamu inginkan"}',
    '{"category": "SalaryLower",		"text": "Sebutkan gaji minimum yang kamu inginkan"}',
    '{"category": "Location",			"text": "Kamu tinggal dimana?"}',
    '{"category": "Location",			"text": "Kamu berasal dari mana?"}',
    '{"category": "Location",			"text": "Domisili manakah kamu?"}',
    '{"category": "Location",			"text": "Di mana kota tempat kamu tinggal?"}',
    '{"category": "Location",			"text": "Kota manakah tempat kamu tinggal?"}',
    '{"category": "Location",			"text": "Di mana lokasi tempat tinggalmu?"}',
    '{"category": "Location",			"text": "Kamu sekarang tinggal di mana?"}',
    '{"category": "Location",			"text": "Lokasi mana yang kamu inginkan?"}',
    '{"category": "Location",			"text": "Apakah kamu bersedia ditempatkan di kota sesuai domisilimu?"}',
    '{"category": "Facility",			"text": "Fasilitas apa yang kamu inginkan?"}',
    '{"category": "Facility",			"text": "Fasilitas apa yang kamu butuhkan untuk menunjang pekerjaanmu?"}',
    '{"category": "Facility",			"text": "Apa jenis fasilitas yang kamu inginkan?"}',
    '{"category": "Facility",			"text": "Apa tunjangan yang kamu harapkan?"}',
    '{"category": "Facility",			"text": "Fasilitas apa saja yang kamu butuhkan?"}',
    '{"category": "Facility",			"text": "Apa saja fasilitas yang kamu butuhkan?"}',
    '{"category": "Facility",			"text": "Apa saja fasilitas yang kamu perlukan?"}',
    '{"category": "Facility",			"text": "Fasilitas apa saja yang kamu inginkan?"}',
    '{"category": "Industry",			"text": "Sekarang kamu sedang bekerja di industri apa?"}',
    '{"category": "Industry",			"text": "Sekarang kamu sedang bekerja di industri apa ya?"}',
    '{"category": "Industry",			"text": "Sekarang kamu sedang bekerja di industri apa sih?"}',
    '{"category": "Field",			"text": "Bidang pekerjaan kamu apa?"}',
    '{"category": "Field",			"text": "Sekarang bidang pekerjaan kamu apa sih?"}',
    '{"category": "Field",			"text": "Sebutkan bidang pekerjaanmu!"}',
    '{"category": "Field",			"text": "Apa bidang pekrjaanmu saat ini?"}',
    '{"category": "JobLevel",			"text": "Pangkat kamu sekarang apa sih?"}',
    '{"category": "JobLevel",			"text": "Apa pangkat kerja kamu saat ini?"}',
    '{"category": "ExpectedLocation",		"text": "Lokasi kerja manakah yang kamu inginkan?"}',
    '{"category": "ExpectedLocation",		"text": "Lokasi mana yang kamu inginkan untuk bekerja?"}',
    '{"category": "ExpectedLocation",		"text": "Di mana lokasi penempatan kerja yang kamu inginkan?"}',
    '{"category": "ExpectedLocation",		"text": "Lokasi manakah yang kamu inginkan utk bekerja?"}',
    '{"category": "ExpectedLocation",		"text": "Di kota manakah kamu bersedia ditempatkan?"}',
]
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "9ad5e836-84cb-401e-9021-bc28552d4964"
}

for p in payload:
    print p
    response = requests.request("POST", url, data=p, headers=headers)

    print(response.text)
