from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="produk_db"
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produk")
    data = cursor.fetchall()
    return render_template('index.html', data=data)

@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form['nama_produk']
    kategori = request.form['kategori']
    harga = request.form['harga']
    stok = request.form['stok']

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produk (nama_produk, kategori, harga, stok) VALUES (%s,%s,%s,%s)",
        (nama, kategori, harga, stok)
    )
    db.commit()
    return redirect('/')

@app.route('/hapus/<int:id>')
def hapus(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM produk WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produk WHERE id=%s", (id,))
    data = cursor.fetchone()
    return render_template('edit.html', data=data)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nama = request.form['nama_produk']
    kategori = request.form['kategori']
    harga = request.form['harga']
    stok = request.form['stok']

    cursor = db.cursor()
    cursor.execute(
        "UPDATE produk SET nama_produk=%s, kategori=%s, harga=%s, stok=%s WHERE id=%s",
        (nama, kategori, harga, stok, id)
    )
    db.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)