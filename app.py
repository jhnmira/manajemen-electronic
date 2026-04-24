# dibuat dengan flask(python) + mysql-connector-python
from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("MYSQLHOST"),
    "user": os.environ.get("MYSQLUSER"),
    "password": os.environ.get("MYSQLPASSWORD"),
    "database": os.environ.get("MYSQLDATABASE"),
    "port": int(os.environ.get("MYSQLPORT", 3306)),
    "connection_timeout": 10,
    "use_pure": True
}

# membuat koneksi ke database
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# nampilin semua data produk
@app.route('/')
def index():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM produk")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('index.html', data=data)
    except Exception as e:
        return f"Koneksi database gagal: {e}", 500

# nambahin produk baru
@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form['nama_produk']
    kategori = request.form['kategori']
    harga = request.form['harga']
    stok = request.form['stok']
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produk (nama_produk, kategori, harga, stok) VALUES (%s,%s,%s,%s)",
        (nama, kategori, harga, stok)
    )
    produk_id = cursor.lastrowid
    # catat riwayat stok awal
    cursor.execute(
        "INSERT INTO riwayat_stok (produk_id, stok_lama, stok_baru, keterangan) VALUES (%s,%s,%s,%s)",
        (produk_id, 0, stok, 'Produk baru ditambahkan')
    )
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

# hapus produk berdasarkan id nya
@app.route('/hapus/<int:id>')
def hapus(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM produk WHERE id=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

# nampilin form edit produk
@app.route('/edit/<int:id>')
def edit(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produk WHERE id=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit.html', data=data)

# nyimpen perubahan data produk
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nama = request.form['nama_produk']
    kategori = request.form['kategori']
    harga = request.form['harga']
    stok_baru = request.form['stok']
    db = get_db()
    cursor = db.cursor()
    # ambil stok lama dulu
    cursor.execute("SELECT stok FROM produk WHERE id=%s", (id,))
    row = cursor.fetchone()
    stok_lama = row[0] if row else 0
    cursor.execute(
        "UPDATE produk SET nama_produk=%s, kategori=%s, harga=%s, stok=%s WHERE id=%s",
        (nama, kategori, harga, stok_baru, id)
    )
    # catat riwayat perubahan stok
    cursor.execute(
        "INSERT INTO riwayat_stok (produk_id, stok_lama, stok_baru, keterangan) VALUES (%s,%s,%s,%s)",
        (id, stok_lama, stok_baru, 'Stok diupdate')
    )
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

# nampilin halaman form tambah produk
@app.route('/tambah-produk')
def tambah_produk():
    return render_template('tambah.html')

# jalanin aplikasi di port dari environment variabel
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
