import requests

url = "http://localhost:8000/api/user_answers/"

payload = ['{"category": "Degree",	"text": "Pendidikan terakhir saya {{x}}"}',
           '{"category": "Degree",	"text": "{{x}}"}',
           '{"category": "Degree",	"text": "Saya lulusan {{x}}"}',
           '{"category": "Degree",	"text": "Tingkat pendidikan terakhir saya {{x}}"}',
           '{"category": "Degree",	"text": "Jenjang Pendidikan terakhir saya {{x}}"}',
           '{"category": "Degree",	"text": "Ya, saya lulusan {{x}}"}',
           '{"category": "Degree",	"text": "Tidak, saya lulusan {{x}}"}',
           '{"category": "Degree",	"text": "Bukan, saya lulusan {{x}}"}',
           '{"category": "Degree",	"text": "Ya, saya sudah lulus {{x}}"}',
           '{"category": "Degree",	"text": "Ya, saya sudah lulus {{x}}"}',
           '{"category": "Major",	"text": "Ya"}',
           '{"category": "Major",	"text": "Ya betul"}',
           '{"category": "Major",	"text": "Tidak"}',
           '{"category": "Major",	"text": "Bukan"}',
           
           '{"category": "Age",	"text": "{{x}}"}',
           '{"category": "Age",	"text": "Umur saya {{x}}"}',
           '{"category": "Age",	"text": "Umur saya {{x}} tahun"}',
           '{"category": "Age",	"text": "Saya {{x}} tahun"}',
           '{"category": "Age",	"text": "Saya berumur {{x}} tahun"}',
           '{"category": "Age",	"text": "Umur saya {{x}} tahun sekarang"}',
           '{"category": "Age",	"text": "Sekarang umur saya {{x}} tahun"}',
           '{"category": "Age",	"text": "Sekarang saya berumur {{x}} tahun"}',
           '{"category": "Age",	"text": "Tahun ini umur saya {{x}} tahun"}',
           '{"category": "Age",	"text": "Tahun ini saya berumur {{x}} tahun"}',
           '{"category": "Age",	"text": "Umur saya {{x}} tahun ini"}',
           '{"category": "Age",	"text": "Umur saya {{x}} tahun"}',
           '{"category": "Age",	"text": "Saya {{x}} tahun"}',
           '{"category": "Age",	"text": "Saya lahir tahun {{x}}"}',
           '{"category": "Age",	"text": "Tahun {{x}}"}',

           '{"category": "Skill",	"text": "{{x}}"}',
           '{"category": "Skill",	"text": "Kemampuan saya {{x}}"}',
           '{"category": "Skill",	"text": "Skill saya {{x}}"}',
           '{"category": "Skill",	"text": "Saya bisa {{x}}"}',
           '{"category": "Skill",	"text": "Saya memiliki kemampuan {{x}}"}',
           '{"category": "Skill",	"text": "Saya punya kemampuan {{x}}"}',
           '{"category": "Skill",	"text": "Saya punya skill {{x}}"}',
           '{"category": "Skill",	"text": "Saya memiliki keterampilan {{x}}"}',
           '{"category": "Skill",	"text": "Saya punya keterampilan {{x}}"}',
           '{"category": "Skill",	"text": "Saya menguasai {{x}}"}',
           '{"category": "Skill",	"text": "Kemampuan yang saya punya {{x}}"}',
           
           '{"category": "Major",	"text": "{{x}}"}',
           '{"category": "Major",	"text": "Jurusan {{x}}"}',
           '{"category": "Major",	"text": "Saya kuliah di jurusan {{x}}"}',
           '{"category": "Major",	"text": "Jurusan kuliah saya{{x}}"}',	
           '{"category": "Major",	"text": "Saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Pas kuliah saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Waktu kuliah saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Sekarang saya kuliah di jurusan {{x}}"}',
           '{"category": "Major",	"text": "Sekarang saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Dulu saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Saya lulusan jurusan {{x}}"}',
           '{"category": "Major",	"text": "Di sekolah saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Di SMK saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Di SMA saya ambil jurusan {{x}}"}',
           '{"category": "Major",	"text": "Saya ambil bidang {{x}}"}',
           '{"category": "Major",	"text": "Saya ambil bidang pendidikan {{x}}"}',
           
           
           '{"category": "Salary",	"text": "Gajinya sekitar {{x}}-{{x}}"}',
           '{"category": "Salary","text": "Gaji saya sekitar {{x}}"}',
           '{"category": "Salary",	"text": "Sekitar {{x}}-{{x}}"}',
           '{"category": "Salary",	"text": "{{x}}-{{x}}"}',
           '{"category": "Salary","text": "{{x}}"}',
           '{"category": "Salary","text": "Gaji yang saya inginkan {{x}} sampai {{x}}"}',
           
           '{"category": "Position","text": "Saya menjabat sebagai {{x}} sebelumnya"}',
           '{"category": "Position","text": "Jabatan saya sebelumnya {{x}}"}',
           '{"category": "Position","text": "Jabatan saya {{x}}"}',
           '{"category": "Position","text": "Saya menjabat sebagai {{x}}"}',
           
           '{"category": "Residence","text": "{{x}}"}',
           '{"category": "Residence","text": "Di {{x}}"}',
           '{"category": "Residence","text": "Saya tinggal di {{x}}"}',
           '{"category": "Residence","text": "Saya tinggal di provinsi {{x}}"}',
           '{"category": "Residence","text": "Sekarang tinggal di {{x}}"}',
           '{"category": "Residence","text": "Sekarang di {{x}}"}',
           
           '{"category": "Location","text": "{{x}}"}',
           '{"category": "Location","text": "{{x}}, {{x}}"}',
           '{"category": "Location","text": "Di {{x}}, {{x}}"}',
           '{"category": "Location","text": "Saya ingin ditempatkan di {{x}}"}',
           '{"category": "Location","text": "Saya ingin ditempatkan di {{x}}, {{x}}"}',
           '{"category": "Location","text": "Saya mau kerja di {{x}}"}',
           
           '{"category": "Facility","text": "{{x}}"}',
           '{"category": "Facility","text": "{{x}}, {{x}}"}',
           '{"category": "Facility","text": "Fasilitas yang saya inginkan {{x}}"}',
           '{"category": "Facility","text": "Fasilitas yang saya inginkan {{x}}, {{x}}"}',
           '{"category": "Facility","text": "Saya butuh fasilitas {{x}}, {{x}}"}',
           
           '{"category": "WorkExp",	"text": "Jobdesk saya adalah {{x}}"}',
           '{"category": "WorkExp",	"text": "{{x}} tahun"}',
           '{"category": "WorkExp",	"text": "Saya sudah pernah bekerja selama {{x}}"}',
           '{"category": "WorkExp",	"text": "Tugas saya adalah {{x}}"}',
           '{"category": "WorkExp",	"text": "Tanggung jawab saya adalah {{x}}"}',
           '{"category": "WorkExp",	"text": "Pekerjaan saya saat ini {{x}}"}',
           '{"category": "WorkExp",	"text": "Pekerjaan saya sekarang {{x}}"}',
           '{"category": "WorkExp",	"text": "Saya pernah bekerja di {x} sebagai {{x}}"}',
           '{"category": "WorkExp",	"text": "Saya pernah bekerja di {x}"}',
           '{"category": "WorkExp",	"text": "Ya, saya sedang bekerja"}',
           '{"category": "WorkExp",	"text": "Tidak, saya sedang bekerja"}',
           '{"category": "WorkExp",	"text": "Ya, saya fresh graduate"}',
           '{"category": "WorkExp",	"text": "Tidak, saya bukan fresh graduate"}',
           '{"category": "WorkExp",	"text": "Tidak, saya sudah pernah bekerja"}',
           '{"category": "WorkExp",	"text": "Ya, saya sudah pernah bekerja"}',
           '{"category": "WorkExp",	"text": "Tidak, saya sudah lulus"}',
           '{"category": "WorkExp",	"text": "Tidak"}',
           '{"category": "WorkExp",	"text": "Ya"}',
           '{"category": "WorkExp",	"text": "Belum"}',
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
