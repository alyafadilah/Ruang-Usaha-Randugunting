from flask import Flask, render_template, abort, redirect, url_for
import math

app = Flask(__name__)

# =========================================================
# DATA UMKM
# =========================================================
# GANTI DATA DI BAWAH DENGAN DATA ASLI PENELITIANMU.
#
# Urutan skor:
# C1 = Lama Usaha
# C2 = Pendapatan
# C3 = Jangkauan Pemasaran
# C4 = Pemanfaatan Digital
# C5 = Jumlah Orang
#
# Skor di bawah hanya CONTOH untuk menjalankan tampilan.
# =========================================================

UMKM_DATA = [
    {
        "id": "ayam-goreng-kalasan-bu-wiwik",
        "name": "Ayam Goreng Kalasan Bu Wiwik",
        "scores": [5, 5, 5, 4, 4]
    },
    {
        "id": "sate-bu-ratmi-randugunting",
        "name": "Sate Bu Ratmi Randugunting",
        "scores": [5, 4, 4, 4, 4]
    },
    {
        "id": "dapur-mama-rista",
        "name": "Dapur Mama Rista",
        "scores": [3, 4, 4, 4, 3]
    },
    {
        "id": "toko-gas-dan-kelontong-pak-yuniarto",
        "name": "Toko Gas dan Kelontong Pak Yuniarto",
        "scores": [4, 4, 3, 3, 3]
    },
    {
        "id": "kost-pak-fajar",
        "name": "Kost Pak Fajar",
        "scores": [4, 3, 3, 3, 3]
    },
    {
        "id": "roti-syafaat",
        "name": "Roti Syafaat",
        "scores": [3, 3, 3, 3, 3]
    },
    {
        "id": "warung-mak-nyak",
        "name": "Warung Mak Nyak",
        "scores": [3, 3, 3, 2, 3]
    },
    {
        "id": "kletikan",
        "name": "Kletikan",
        "scores": [2, 3, 3, 3, 2]
    },
        {
        "id": "warung-ibu-sukini",
        "name": "Warung Ibu Sukini",
        "scores": [3, 2, 2, 2, 2]
    },
    {
        "id": "butik-ibu-esti",
        "name": "Butik Ibu Esti",
        "scores": [2, 2, 2, 3, 2]
    },
    {
        "id": "ayam-segar-ibu",
        "name": "Ayam Segar Ibu",
        "scores": [5, 2, 2, 2, 2]
    },
    {
        "id": "toko-madani",
        "name": "Toko Madani",
        "scores": [3, 5, 1, 2, 4]
    }
]


# =========================================================
# KRITERIA
# =========================================================

CRITERIA = [
    {
        "code": "C1",
        "name": "Lama Usaha",
        "short": "Pengalaman dan keberlangsungan usaha",
        "type": "Benefit",
        "weight": 0.20,
        "slug": "lama-usaha",
        "icon": "01"
    },
    {
        "code": "C2",
        "name": "Pendapatan",
        "short": "Gambaran kemampuan ekonomi usaha",
        "type": "Benefit",
        "weight": 0.25,
        "slug": "pendapatan",
        "icon": "02"
    },
    {
        "code": "C3",
        "name": "Jangkauan Pemasaran",
        "short": "Luasnya pasar yang dijangkau",
        "type": "Benefit",
        "weight": 0.20,
        "slug": "jangkauan-pemasaran",
        "icon": "03"
    },
    {
        "code": "C4",
        "name": "Pemanfaatan Digital",
        "short": "Penggunaan media digital dalam usaha",
        "type": "Benefit",
        "weight": 0.20,
        "slug": "pemanfaatan-digital",
        "icon": "04"
    },
    {
        "code": "C5",
        "name": "Jumlah Orang",
        "short": "Keterlibatan orang dalam usaha",
        "type": "Benefit",
        "weight": 0.15,
        "slug": "jumlah-orang",
        "icon": "05"
    }
]

# =========================================================
# PENJELASAN ASPEK
# =========================================================

ASPEK_DETAIL = {
    "lama-usaha": {
        "title": "Lama Usaha",
        "subtitle": "Melihat pengalaman dan keberlangsungan usaha.",
        "question": "Mengapa aspek ini dipilih?",
        "description": (
            "Lama usaha digunakan untuk melihat pengalaman dan "
            "keberlangsungan suatu usaha. Usaha yang telah berjalan "
            "lebih lama dapat memiliki pengalaman dalam menghadapi "
            "perubahan pasar, mempertahankan pelanggan, dan mengelola "
            "kegiatan usaha."
        ),
        "relevance": (
            "Aspek ini relevan karena dapat memberikan gambaran "
            "mengenai seberapa lama suatu usaha mampu bertahan "
            "dan menjalankan kegiatan usahanya."
        ),
        "measurement": (
            "Penilaian dilakukan berdasarkan kategori lama usaha "
            "yang telah ditentukan dalam instrumen penelitian."
        )
    },
    "pendapatan": {
        "title": "Pendapatan",
        "subtitle": "Melihat gambaran kemampuan ekonomi usaha.",
        "question": "Mengapa aspek ini dipilih?",
        "description": (
            "Pendapatan digunakan untuk melihat gambaran kemampuan "
            "ekonomi suatu usaha. Besarnya pendapatan dapat memberikan "
            "informasi mengenai aktivitas penjualan dan kondisi usaha."
        ),
        "relevance": (
            "Aspek ini relevan karena pendapatan merupakan salah satu "
            "indikator yang dapat membantu menggambarkan kondisi "
            "ekonomi dan perkembangan usaha."
        ),
        "measurement": (
            "Penilaian dilakukan berdasarkan kategori rata-rata "
            "pendapatan kotor per bulan."
        )
    },
    "jangkauan-pemasaran": {
        "title": "Jangkauan Pemasaran",
        "subtitle": "Melihat luasnya pasar yang dijangkau.",
        "question": "Mengapa aspek ini dipilih?",
        "description": (
            "Jangkauan pemasaran digunakan untuk melihat seberapa "
            "luas suatu usaha menjangkau pelanggan. Jangkauan dapat "
            "berkaitan dengan lingkungan sekitar, wilayah yang lebih "
            "luas, maupun pelanggan di luar daerah."
        ),
        "relevance": (
            "Aspek ini relevan karena luasnya jangkauan pemasaran "
            "dapat memberikan gambaran mengenai cakupan pasar "
            "yang dimiliki suatu usaha."
        ),
        "measurement": (
            "Penilaian dilakukan berdasarkan kategori wilayah "
            "pemasaran yang telah ditentukan."
        )
    },
    "pemanfaatan-digital": {
        "title": "Pemanfaatan Digital",
        "subtitle": "Melihat penggunaan media digital dalam usaha.",
        "question": "Mengapa aspek ini dipilih?",
        "description": (
            "Pemanfaatan digital digunakan untuk melihat sejauh "
            "mana usaha memanfaatkan media digital dalam kegiatan "
            "pemasaran maupun penjualan."
        ),
        "relevance": (
            "Aspek ini relevan karena media digital dapat menjadi "
            "salah satu sarana untuk memperkenalkan produk, "
            "menjangkau pelanggan, dan mendukung kegiatan usaha."
        ),
        "measurement": (
            "Penilaian dilakukan berdasarkan tingkat pemanfaatan "
            "media digital yang digunakan oleh masing-masing usaha."
        )
    },
    "jumlah-orang": {
        "title": "Jumlah Orang",
        "subtitle": "Melihat keterlibatan orang dalam menjalankan usaha.",
        "question": "Mengapa aspek ini dipilih?",
        "description": (
            "Jumlah orang digunakan untuk melihat banyaknya orang "
            "yang terlibat dalam menjalankan kegiatan usaha, baik "
            "pemilik, anggota keluarga, maupun tenaga kerja."
        ),
        "relevance": (
            "Aspek ini relevan karena dapat memberikan gambaran "
            "mengenai keterlibatan sumber daya manusia dalam "
            "operasional usaha."
        ),
        "measurement": (
            "Penilaian dilakukan berdasarkan jumlah orang yang "
            "terlibat dalam kegiatan usaha."
        )
    }
}

# =========================================================
# FUNGSI PERHITUNGAN TOPSIS
# =========================================================

def calculate_topsis():
    matrix = [item["scores"] for item in UMKM_DATA]

    # Normalisasi vektor
    normalized = []

    for j in range(len(CRITERIA)):
        denominator = math.sqrt(
            sum(row[j] ** 2 for row in matrix)
        )

        column = []

        for row in matrix:
            if denominator == 0:
                column.append(0)
            else:
                column.append(row[j] / denominator)

        normalized.append(column)

    # Normalisasi terbobot
    weighted = []

    for i in range(len(matrix)):
        row = []

        for j, criterion in enumerate(CRITERIA):
            value = normalized[j][i] * criterion["weight"]
            row.append(value)

        weighted.append(row)

    # Solusi ideal positif dan negatif
    ideal_positive = []
    ideal_negative = []

    for j, criterion in enumerate(CRITERIA):
        values = [row[j] for row in weighted]

        if criterion["type"] == "Benefit":
            ideal_positive.append(max(values))
            ideal_negative.append(min(values))
        else:
            ideal_positive.append(min(values))
            ideal_negative.append(max(values))

    # Jarak dan nilai preferensi
    results = []

    for i, item in enumerate(UMKM_DATA):
        distance_positive = math.sqrt(
            sum(
                (weighted[i][j] - ideal_positive[j]) ** 2
                for j in range(len(CRITERIA))
            )
        )

        distance_negative = math.sqrt(
            sum(
                (weighted[i][j] - ideal_negative[j]) ** 2
                for j in range(len(CRITERIA))
            )
        )

        total_distance = distance_positive + distance_negative

        if total_distance == 0:
            preference = 0
        else:
            preference = distance_negative / total_distance

        results.append({
            **item,
            "score": preference,
            "distance_positive": distance_positive,
            "distance_negative": distance_negative
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    for index, item in enumerate(results, start=1):
        item["rank"] = index

    return results


def get_umkm_by_id(umkm_id):
    for item in UMKM_DATA:
        if item["id"] == umkm_id:
            return item

    return None


def get_ranking_by_id(umkm_id):
    for item in calculate_topsis():
        if item["id"] == umkm_id:
            return item

    return None


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    ranking = calculate_topsis()

    return render_template(
        "dashboard.html",
        umkm=UMKM_DATA,
        criteria=CRITERIA,
        ranking=ranking
    )


@app.route("/alternatif")
def alternatif():
    return render_template(
        "alternatif.html",
        umkm=UMKM_DATA,
        criteria=CRITERIA
    )


@app.route("/alternatif/<umkm_id>")
def detail_alternatif(umkm_id):
    item = get_umkm_by_id(umkm_id)

    if item is None:
        abort(404)

    ranking_item = get_ranking_by_id(umkm_id)

    return render_template(
        "detail_alternatif.html",
        item=item,
        ranking_item=ranking_item,
        criteria=CRITERIA
    )


@app.route("/penilaian")
def penilaian():
    return render_template(
        "penilaian.html",
        umkm=UMKM_DATA,
        criteria=CRITERIA
    )


@app.route("/aspek")
def aspek():
    return render_template(
        "aspek.html",
        criteria=CRITERIA
    )


@app.route("/aspek/<slug>")
def aspek_detail(slug):
    detail = ASPEK_DETAIL.get(slug)

    if detail is None:
        abort(404)

    criterion = next(
        (item for item in CRITERIA if item["slug"] == slug),
        None
    )

    return render_template(
        "aspek_detail.html",
        detail=detail,
        criterion=criterion
    )


@app.route("/metode")
def metode():
    return render_template("metode.html")


@app.route("/metode/ahp")
def ahp():
    return render_template(
        "ahp.html",
        criteria=CRITERIA
    )


@app.route("/metode/topsis")
def topsis():
    return render_template(
        "topsis.html",
        criteria=CRITERIA
    )


@app.route("/ranking")
def ranking():
    results = calculate_topsis()

    return render_template(
        "ranking.html",
        ranking=results,
        criteria=CRITERIA
    )


@app.route("/ranking/<umkm_id>")
def detail_ranking(umkm_id):
    item = get_ranking_by_id(umkm_id)

    if item is None:
        abort(404)

    return render_template(
        "detail_ranking.html",
        item=item,
        criteria=CRITERIA
    )


# =========================================================
# ROUTE SARAN PENGEMBANGAN
# =========================================================

# Route pengaman jika masih ada link lama yang menuju /saran
@app.route("/saran")
def saran_redirect():
    return redirect(url_for("ranking"))


# Route utama untuk saran berdasarkan UMKM yang dipilih
@app.route("/saran/<umkm_id>")
def saran(umkm_id):
    umkm = get_umkm_by_id(umkm_id)

    if umkm is None:
        abort(404)

    ranking_item = get_ranking_by_id(umkm_id)

    return render_template(
        "saran.html",
        umkm=umkm,
        ranking_item=ranking_item,
        criteria=CRITERIA,
        aspek_detail=ASPEK_DETAIL
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)