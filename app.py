from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "mysql.railway.internal",
    "user": "root",
    "password": "ZBokFDzGmJNIJfbcxNMiyYQVxPEvHLUF",
    "database": "railway"
    "connection_timeout": 10,
    "use_pure": True
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produk")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', data=data)
except Exception as e:
    return f"Koneksi database gagal: {e}", 500

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

@app.route('/hapus/<int:id>')
def hapus(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM produk WHERE id=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produk WHERE id=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit.html', data=data)

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

if __name__ == "__main__":
    app.run(debug=True)
