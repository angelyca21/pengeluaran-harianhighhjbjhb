from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pengeluaran.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pengeluaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    jumlah = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({
        "pesan": "Aplikasi Pencatatan Pengeluaran Harian",
        "status": "aktif"
    })

@app.route('/pengeluaran', methods=['GET'])
def get_pengeluaran():
    data = Pengeluaran.query.all()

    hasil = []

    for item in data:
        hasil.append({
            "id": item.id,
            "nama": item.nama,
            "jumlah": item.jumlah
        })

    return jsonify(hasil)

@app.route('/tambah', methods=['POST'])
def tambah_pengeluaran():
    data = request.json

    pengeluaran_baru = Pengeluaran(
        nama=data['nama'],
        jumlah=data['jumlah']
    )

    db.session.add(pengeluaran_baru)
    db.session.commit()

    return jsonify({
        "pesan": "Data berhasil ditambahkan"
    })

@app.route('/hapus/<int:id>', methods=['DELETE'])
def hapus_pengeluaran(id):
    data = Pengeluaran.query.get(id)

    if not data:
        return jsonify({
            "pesan": "Data tidak ditemukan"
        })

    db.session.delete(data)
    db.session.commit()

    return jsonify({
        "pesan": "Data berhasil dihapus"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "sehat"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)