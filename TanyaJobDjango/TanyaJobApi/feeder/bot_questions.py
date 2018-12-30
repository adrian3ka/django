import requests

url = "http://localhost:8000/api/bot_questions/"

payload = ['{"category": "Age","text": "Umur kamu berapa?"}',
		   '{"category": "Age","text": "Berapa umur kamu?"}',
		   '{"category": "Age","text": "Berapa umur kamu sekarang?"}',
		   '{"category": "Age","text": "Sekarang berapa umur kamu?"}',
		   '{"category": "Age","text": "Tahun ini umur kamu berapa?"}',
		   '{"category": "Age","text": "Tahun ini berapa umur kamu?"}',
		   '{"category": "Age","text": "Tahun ini berapa umurmu?"}',
		   '{"category": "Age","text": "Umur kamu berapa tahun ini?"}',
		   '{"category": "Age","text": "Berapa umur kamu tahun ini?"}',
		   '{"category": "Age","text": "Berapa umurmu tahun ini?"}',
		   '{"category": "Age","text": "Usia kamu berapa?"}',
		   '{"category": "Age","text": "Berapa usia kamu?"}',
		   '{"category": "Age","text": "Berapa usia kamu sekarang?"}',
		   '{"category": "Age","text": "Sekarang berapa usia kamu?"}',
		   '{"category": "Age","text": "Tahun ini usia kamu berapa?"}',
		   '{"category": "Age","text": "Tahun ini berapa usia kamu?"}',
		   '{"category": "Age","text": "Tahun ini berapa usiamu?"}',
		   '{"category": "Age","text": "Usia kamu berapa tahun ini?"}',
		   '{"category": "Age","text": "Berapa usia kamu tahun ini?"}',
		   '{"category": "Age","text": "Berapa usiamu tahun ini?"}',
		   '{"category": "Age","text": "Kamu lahir tahun berapa?"}',
		   '{"category": "Age","text": "Tahun berapa kamu lahir?"}',
		   
		   '{"category": "Degree","text": "Pendidikan terakhir kamu apa?"}',
		   '{"category": "Degree","text": "Boleh tahu pendidikan terakhir kamu?"}',
		   '{"category": "Degree","text": "Tingkat pendidikan terakhir kamu apa?"}',
		   '{"category": "Degree","text": "Jenjang pendidikan terakhir kamu apa?"}',
		   '{"category": "Degree","text": "Apakah kamu lulusan SMA/SMK?"}',
		   '{"category": "Degree","text": "Apakah kamu lulusan S1?"}',
		   '{"category": "Degree","text": "Apakah kamu lulusan S2?"}',
		   '{"category": "Degree","text": "Apakah kamu lulusan S3?"}',
		   '{"category": "Degree","text": "Gelar terakhir kamu apa?"}',
		   '{"category": "Degree","text": "Kamu lagi ambil pendidikan tingkat apa?"}',
		   '{"category": "Degree","text": "Sekarang lagi kuliah di tingkat apa?"}',
		   
		   '{"category": "Skill","text": "Coba sebutkan kemampuan kamu apa saja"}',
		   '{"category": "Skill","text": "Coba sebutkan skill set kamu"}',
		   '{"category": "Skill","text": "Nah, aku mau tau dulu nih skill set kamu apa saja"}',
		   '{"category": "Skill","text": "Kamu punya kemampuan apa saja?"}',
		   '{"category": "Skill","text": "Kamu punya keterampilan apa saja?"}',
		   '{"category": "Skill","text": "Kalo keterampilan,kamu bisa apa saja nih?"}',
		   '{"category": "Skill","text": "Menurut kamu, kamu punya skill apa saja?"}',
		   '{"category": "Skill","text": "Mau tau dong skill kamu apa saja nih?"}',
		   '{"category": "Skill","text": "Coba sebutkan hardskill kamu"}',
		   '{"category": "Skill","text": "Coba sebutkan softskill kamu"}',
		   
           '{"category": "Major","text": "Kamu kuliah di jurusan apa?"}',
           '{"category": "Major","text": "Jurusan kuliah kamu apa?"}',
           '{"category": "Major","text": "Kalau boleh tahu jurusan kamu apa ya?"}',
           '{"category": "Major","text": "Mau tau dong jurusan kuliah kamu"}',
           '{"category": "Major","text": "Kamu ambil kuliah jurusan apa?"}',
           '{"category": "Major","text": "Memang kamu ambil jurusan apa?"}',
           '{"category": "Major","text": "Pas kuliah kamu ambil jurusan apa?"}',
           '{"category": "Major","text": "Waktu kuliah kamu ambil jurusan apa?"}',
           '{"category": "Major","text": "Sekarang lagi kuliah di jurusan apa?"}',
           '{"category": "Major","text": "Dulu pas kuliah kamu ambil jurusan apa?"}',
           '{"category": "Major","text": "Kamu lulusan jurusan apa?"}',
           '{"category": "Major","text": "Di sekolah kamu ambil jurusan apa?"}',
           '{"category": "Major","text": "Di SMK kamu ambil jurusan apa?"}',
           '{"category": "Major","text": "Di SMA kamu ambil jurusan apa?"}',
           '{"category": "Major","text": "Kamu lagi ambil bidang pendidikan apa?"}',
           '{"category": "Major","text": "Peminatan yang kamu ambil dijurusan kamu apa?"}',
           '{"category": "Major","text": "Kamu ambil peminatan apa?"}',
           
           '{"category": "WorkExp","text": "Sebelumnya, apa kamu sudah pernah bekerja?"}',
           '{"category": "WorkExp","text": "Apakah kamu memiliki pengalaman kerja?"}',
           '{"category": "WorkExp","text": "Kamu sudah pernah bekerja belum?"}',
           '{"category": "WorkExp","text": "Apakah kamu fresh graduate?"}',
           '{"category": "WorkExp","text": "Apakah kamu baru lulus?"}',
           '{"category": "WorkExp","text": "Coba sebutkan pengalaman kerja yang dimiliki"}',
           '{"category": "WorkExp","text": "Kamu sudah pernah bekerja dimana saja?"}',
           '{"category": "WorkExp","text": "Sebelumnya, kamu pernah bekerja dimana saja?"}',
           '{"category": "WorkExp","text": "Saat ini pekerjaanmu apa?"}',
           '{"category": "WorkExp","text": "Apa pekerjaan kamu sekarang?"}',
           '{"category": "WorkExp","text": "Apakah kamu saat ini sedang bekerja?"}',
           '{"category": "WorkExp","text": "Apa jobdesk pada perusahaan yang lama?"}',
           '{"category": "WorkExp","text": "Apa jabatan kamu di perusahaan tersebut?"}',
           '{"category": "WorkExp","text": "Apa tugas kamu diperusahaan lama?"}',
           '{"category": "WorkExp","text": "Apa tanggung jawab kamu di perusahaan lama?"}',
           
           '{"category": "WorkDuration","text": "Kamu sudah pernah bekerja berapa lama?"}',
           
           '{"category": "Position","text": "Jabatan terakhir kamu apa?"}',
           '{"category": "Position","text": "Apa posisi terakhir yang kamu tempati?"}',
           '{"category": "Position","text": "Di tempat kerjamu yang dulu, kamu berada pada posisi sebagai apa?"}',
           '{"category": "Position","text": "Apa jenjang karirmu sebelumnya?"}',
           '{"category": "Position","text": "Posisi terakhirmu sebagai apa?"}',
           '{"category": "Position","text": "Di tingkat mana posisimu sebelumnya?"}',
           '{"category": "Position","text": "Kamu menjabat sebagai apa sebelumnya?"}',
           '{"category": "Position","text": "Apa jabatan terakhir yang kamu raih?"}',
           
           '{"category": "Salary","text": "Berapa range gaji yang kamu inginkan?"}',
           '{"category": "Salary","text": "Berapa minimum dan maksimum gaji yang kamu inginkan?"}',
           '{"category": "Salary","text": "Berapa gaji yang kamu harapkan?"}',
           '{"category": "Salary","text": "Berapa kisaran gaji yg kamu harapkan?"}',
           '{"category": "Salary","text": "Boleh tau kisaran gaji yang kamu inginkan?"}',
           '{"category": "Salary","text": "Kamu mau range gaji berapa?"}',
           '{"category": "Salary","text": "Sebutkan range gaji yang kamu inginkan"}',
           
           '{"category": "Salary","text": "Berapa gaji mu sebelumnya?"}',
           '{"category": "Salary","text": "Berapa gaji minimum dan maksimum yg kamu dpt sebelumnya?"}',
           '{"category": "Salary","text": "Kisaran gaji kamu sebelumnya berapa?"}',
           '{"category": "Salary","text": "Boleh tau kisaran gaji yang kamu dapat sebelumnya?Berapa kisaran gaji yang kamu peroleh sebelumnya?"}',
           '{"category": "Salary","text": "Boleh tau kisaran gaji kamu sebelumnya?"}',
           '{"category": "Salary","text": "Gaji kamu sebelumnya berapa?"}',
           '{"category": "Salary","text": "Kamu dulu gajinya di kisaran berapa?"}',
         
           '{"category": "Location","text": "Kamu tinggal dimana?"}',
           '{"category": "Location","text": "Kamu berasal dari mana?"}',
           '{"category": "Location","text": "Domisili manakah kamu?"}',
           '{"category": "Location","text": "Di mana kota tempat kamu tinggal?"}',
           '{"category": "Location","text": "Kota manakah tempat kamu tinggal?"}',
           '{"category": "Location","text": "Di mana lokasi tempat tinggalmu?"}',
           '{"category": "Location","text": "Kamu sekarang tinggal di mana?"}',
           
           '{"category": "Location","text": "Lokasi mana yang kamu inginkan?"}',
           '{"category": "Location","text": "Lokasi tempat tinggal mana yang kamu inginkan untuk bekerja?"}',
           '{"category": "Location","text": "Di mana lokasi penempatan yang kamu inginkan?"}',
           '{"category": "Location","text": "Lokasi manakah yang kamu inginkan utk bekerja?"}',
           '{"category": "Location","text": "Di manakah kamu bersedia ditempatkan?"}',
           '{"category": "Location","text": "Apakah kamu bersedia ditempatkan di kota sesuai domisilimu?"}',
           
           '{"category": "Facility","text": "Fasilitas apa yang kamu inginkan?"}',
           '{"category": "Facility","text": "Fasilitas apa yang kamu butuhkan untuk menunjang pekerjaanmu?"}',
           '{"category": "Facility","text": "Apa jenis fasilitas yang kamu inginkan?"}',
           '{"category": "Facility","text": "Apa tunjangan yang kamu harapkan?"}',
           '{"category": "Facility","text": "Fasilitas apa saja yang kamu butuhkan?"}',
           '{"category": "Facility","text": "Apa saja fasilitas yang kamu butuhkan?"}',
           '{"category": "Facility","text": "Apa saja fasilitas yang kamu perlukan?"}',
           '{"category": "Facility","text": "Fasilitas apa saja yang kamu inginkan?"}',
           
           
           
           
           
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
