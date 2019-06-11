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
cur.execute("SELECT title, original_title FROM tanyajob_chat.job_job GROUP BY title;")

removed_words = ["tanggerang", "aceh ", "palopo", "Jakarta", "Area", "Jember","Semarang", "Jember", "Walk in Interview","Batch", "Viii","Yogyakarta","Surabaya", "Barat", "Jogja", "Tangerang", "Selatan","Pt Indosurya Finance", "PT", "Depok","Karawang", "Cibubur", "Bekasi", "Rembang", "Dki", "Alam Sutera","Bandung", "Boyolali","Cililitan","Cibinong", "Cibubur", "Citraland Mall", "Depok","Emporium Pluit Mall", "Makasar", "Samarinda", "Semarang","Pt Star Cosmos","Jawa Tengah", ",","Cilegon", "Pusat", "Di Mall Ambasador", "Di Depok Town Square","Depok Town Square", "Di Bec - Bandung","Jawa","Tengah"," - ", " , ", "Banyuwangi", "Kediri", "Tulungagung", "Trenggalek", "Dan Sekitarnya", "Tarakan","for Bod", "Interview", "Langsung","1","2","3","4","5","6","7","8","9","Bank Cimb Niaga Jabodetabek","Cimb","Jabodetabek","Cianjur","Solo","Di Pusat Grosir Cililitan","Grosir","Jatim","- ", "Penempatan", " : ",
"Cabang", "Palembang","Balikpapan","Kota /Riau","Traveloka","Bogor","Denpasar","Bali","Bca","Bank Swasta","Palu",":","Bank Sampoerna","Makasar","Bengkulu","Purwokerto","dan "," Dan "," & ","Bogor","Di Mangga Dua Mall","Loker","Lowongan Kerja","Di Supermall Karawaci","Karawaci"," and "," And ","Delivery Sub Agen Jne Berau","Traveloka","Bengkulu","Pontianak","Sanggau","Lamongan","Bojonegoro","Kalimantan","Kalimantan Timur","Dept.Makishinko","Dept.Nitto Kohki","Dept.Tone","Div.Nitto Wil.","Bali","Bank Niaga","Pekanbaru","Patisserie","Sukabumi","Timur","Global Intrima","Pati ","Yogya","Maybank","Mataram","Papua","Pt. Trisula Prima Agung","Pt Epson Cikarang","Cikarang","Pt Epson","Kendari","Wilayah","Ciledug","Magang","Sidoarjo","makasar","di ", " marin ", " for ", " of ", " toko ", "dot ","sidoarjo", "BELILAS", "BANDUNG", "BALIKPAPAN", "Ambon", "Sragen", "SORONG", "Singkawang", " Kota", " Batu", "BATULICIN", " BONTANG", " Brebes", " Bukittinggi", "Cileungsi", "jakarta", " on " , " to ", " in ", " batam ", " cosmos ", " pt ", " bekasi ", " selatan ", " semarang", " pekanbaru", " riau ", " tengah", " kota", " palembang", " tangerang ", " depok", " jambi", " surabaya", " karawang", " banda", " aceh", " selatan",  " bekasi", " star", " bintaro", " balikpapan", " samarinda", " to", " cianjur", " tower", " lumajang", " situbondo", " tangerang", " staff", " sudirman", " penempatan", " barat", " jabodetabek", " aeon", " green"," lokasi", "ambarawa", " nonhalal", " traveloka", " yogyakarta", " email", " kediri", "cibinong", "cibaliung", " jember", " jombang", " kudus", " lampung", " madiun", " magelang", " medan", " mojokerto", " padang", " pasaman", " pati", " ponorogo", " purwokerto", "rangkasbitung", " rembang" , " serang", " singaraja", " sleman", " sorong", " sukabumi", " tabanan", " yogyakarta", " mojokerto", " denpasar", " kalianda", " kudus", " lembang", " makassar", " majalaya", " malang", " padalarang", "pringsewu", " soreang", " pondok", " gede", " jabung", " tanjung", " timika", " bandung", " berbahasa", " myfeet", " senen", " atrium", "bali ", "balikpapan", "bekasi ", "tasikmalaya", "bogor", "kebayoran", " baru", "pesanggrahan", "purwodadi", "purworejo", "alam ", " sutera", "ambon ","and ", " bandung", " bangka", " banjar", "banjarmasin", "officer", "banten", "banyuwangi", "barat ", "kalimantan", " lombok", "baturaja", " tulang", " bawang", "baubau ", " yamaha", " indonesia", " atambua", " mall", " mal " "meropolitan", " pluit", "avenua", "manado","bandung","pusat","cikarang", "bukittinggi", "sentanri", " parung", " jkt ", " tarakan", " timur", " utara", " gojek", "gowa ", "gresik ", "grobogan ", "jabodetabek", "jambi ", "jayapura ", "jawa ", "timur", " jember", "jogja ", "johor ", "jombang ", "kabanjahekaro", "kalianda ", "karanganyar", "karawang ", "kendari ", "ketapang ", "konawe", "kuningan", "lamongan", "leuwiliang", "langsa", " madura", " majalengka", " luwuk", "linggau", "lubuk", " mataram", " martapura", " maros", "muko", " palangkaraya", " nganjuk", " palopo", " palu", " kopo " , "surbaya", "sumbawa", "prabumulih", " poso", " pakam", " marelan", " manna", "tugumulyo", "gianyar", "grobongan", "indramayu", "jermber", "jenepinto", " karo ", " kabanjahe", " kepanjen", " kupang ", " kisaran ", " kerukut", " pangkalan", " kerinci", " kebumen", "serpong", " cimb ", " niaga ", " swasta", "batam ", "baratutara", "batu ", " licin", "bawang ", "bca ", "berau ", "betung ","bima ", "binjaisumatera ", "bintaro ","biznet ", "blitar ", "blora ","singkawang", "sintang","padang", "medan", "makassar", "cirebon", "jayaputa", "batam", "serang"," selatan", "sanggau","singaraja", "tembilahan", " sumba", " sintang", " sampit", " tegal", " tanggamus", " stabat"," sibolga", " sampang", "serpong", "bulukumba", "bulian ", " muara", "bungo ", "bungur", "cimb ", "cinere ", "cipete ", " jakbar ", "citral", "emporium", "mempawah", "kupang","magetan","pamulang", "pasuruan", " kopo", " raya", " karo", " kisaran", "raja", "sarolangun", " metro", " kiara ", "warung", "garut", "gorontalo", "rokan" , "hilir", " pangkal " , " pinang" , "panimbang", "pasuruan", "payakumbuh", "pematang", "siantar", "rantau", "prapat", "probolinggo", "purwakarta", "picung", "tenggarong", "tambun", "temanggung", "tambun", "pontianak", " raja", "pekalongan", "kuantam", "teluk", "maumere", "sumatera", "sumatra", "fifgroup", " goa ", "pangkalpinang", " pelabuhan ", " ratu", " rantauprapat" , "lampung", " rengat", " seatan", "sanggata", "selong", "siborongborong", "sidempuan"," subang", " sug", " takalar", " tebing " , " tinggi", " temangung", "tinanggea", "tuban", "wates", "sentani","bumi " , "klaten", ",angkutana", "monosari","monowali","ngawi", "sukohargjo", "jayapura", "xl"," sulawesi", "kranggan", "kasinocambodia","cileungsi","cimahi","cilacap", " singa", "morowali"," sukoharjo"," jaksel"]

replaced_words = [["Manager", "Manajer"],["Sr.", "Senior"],["senioir", "Senior"], ["Jr.", "Junior"], ["Staf ", "Staff "],["Teacher","Teacher "],["Teachers", "Teacher"],["Technician","Teknisi"],["operational","operasional"],["administration","administrasi"],["sekertaris","sekretaris"],["secretary","sekretaris"], ["tekhnisi", "teknisi"],["mrketing", "marketing"]]

count = 0
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

    regex = re.compile('[^a-zA-Z\s]')
    tagged_title = regex.sub(' ', cleaned_title.lower()).split()
    tagged_title = sorted(tagged_title)

    tagged_title = (' | '.join(tagged_title))
    print tagged_title

    query = "UPDATE tanyajob_chat.job_job SET title = '" + tagged_title +"' WHERE title = '" + original_title + "';"
    cur.execute(query)
    db.commit()
    print "-----------------------------------------"
print count
