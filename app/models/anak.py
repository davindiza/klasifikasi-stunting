# app/models.py
from app import db
from datetime import datetime

class Anak(db.Model):
    __tablename__ = 'tb_anak'

    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16))
    nama = db.Column(db.String(100))
    jk = db.Column(db.Enum('L', 'P', name='jenis_kelamin'), nullable=False)
    tgl_lahir = db.Column(db.Date)
    bb_lahir = db.Column(db.Float)
    tb_lahir = db.Column(db.Float)
    nama_ortu = db.Column(db.String(100))
    prov = db.Column(db.String(100))
    kab_kota = db.Column(db.String(100))
    kecamatan = db.Column(db.String(100))
    puskesmas = db.Column(db.String(100))
    desa = db.Column(db.String(100))
    posyandu = db.Column(db.String(100))
    rt = db.Column(db.Integer)
    rw = db.Column(db.Integer)
    alamat = db.Column(db.String(255))
    usia_ukur = db.Column(db.Integer)
    berat = db.Column(db.Float)
    tinggi = db.Column(db.Float)
    lila = db.Column(db.Float)
    bb_u = db.Column(db.Float)
    tb_u = db.Column(db.Float)
    bb_tb = db.Column(db.Float)
    naik_berat_badan = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Pengukuran(db.Model):
    __tablename__ = 'tb_pengukuran'

    id = db.Column(db.Integer, primary_key=True)
    id_anak = db.Column(db.Integer)
    cara_ukur = db.Column(db.String(50))
    lila = db.Column(db.Float)
    tinggi = db.Column(db.Float)
    berat = db.Column(db.Float)
    lingkar_kepala = db.Column(db.String(50))
    edema = db.Column(db.String(50))
    ikut_kelas_ibu = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Detail_anak(db.Model):
    __tablename__ = 'tb_detail_anak'

    id = db.Column(db.Integer, primary_key=True)
    id_anak = db.Column(db.Integer)
    umur = db.Column(db.Integer)  # <-- perbaikan huruf C
    tgl_pengukuran = db.Column(db.DateTime)  # <-- perbaikan huruf C
    cara_ukur = db.Column(db.String(50))
    lila = db.Column(db.Float)
    tinggi = db.Column(db.Float)
    berat = db.Column(db.Float)
    zs_bb_u = db.Column(db.Float)
    zs_tb_u = db.Column(db.Float)
    zs_bb_tb = db.Column(db.Float)
    lingkar_kepala = db.Column(db.String(50))
    edema = db.Column(db.String(50))
    ikut_kelas_ibu = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Klasifikasi(db.Model):
    __tablename__ = 'tb_klasifikasi'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    umur = db.Column(db.Integer)  # <-- perbaikan huruf C
    jk = db.Column(db.Enum('L', 'P', name='jenis_kelamin'), nullable=False)
    tinggi = db.Column(db.Float)
    berat = db.Column(db.Float)
    status_gizi_bbu = db.Column(db.String(50))
    status_stunting = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)