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
    stok = request.form['stok']
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE produk SET nama_produk=%s, kategori=%s, harga=%s, stok=%s WHERE id=%s",
        (nama, kategori, harga, stok, id)
    )
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

# jalanin aplikasi di port dari environment variabel
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
