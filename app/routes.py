from app import app
from flask import render_template, redirect, url_for, request
from app.models import Anak, Pengukuran
from app import db
from datetime import datetime, date
import pandas as pd
import os

# from app.generateAgeMonth import hitung_umur_bulan


@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data-anak')
def data_anak():
    anak_list = Anak.query.all()
    return render_template('data_anak.html', anak_list=anak_list)

@app.route('/anak/input', methods=['GET', 'POST'])
def input_data_anak():
    if request.method == 'POST':
        anak = Anak(
            nik=request.form.get('nik'),
            nama=request.form.get('nama'),
            jk=request.form.get('jk'),
            tgl_lahir=request.form.get('tanggallahir'),
            bb_lahir=request.form.get('bblahir'),
            tb_lahir=request.form.get('tblahir'),
            nama_ortu=request.form.get('namaortu'),
            prov=request.form.get('prov'),
            kab_kota=request.form.get('kabkota'),
            kecamatan=request.form.get('kecamatan'),
            puskesmas=request.form.get('puskesmas'),
            desa=request.form.get('desakelurahan'),
            posyandu=request.form.get('posyandu'),
            rt=request.form.get('rt'),
            rw=request.form.get('rw'),
            alamat=request.form.get('alamat'),
            usia_ukur=request.form.get('usiasaatukur'),
            berat=request.form.get('berat'),
            tinggi=request.form.get('tinggi'),
            lila=request.form.get('lila'),
            bb_u=request.form.get('bbu'),
            tb_u=request.form.get('tbu'),
            bb_tb=request.form.get('bbtb'),
            naik_berat_badan=request.form.get('naikberatbadan'),
            created_at=datetime.utcnow()
        )
        db.session.add(anak)
        db.session.commit()
        return redirect(url_for('data_anak'))

    return render_template('input_data_anak.html')


# @app.route('/anak/input')
# def input_data_anak():
#     return render_template('input_data_anak.html')

@app.route('/anak/<int:anak_id>')
def detail_anak(anak_id):
    anak = Anak.query.get_or_404(anak_id)
    return render_template('detail_anak.html', anak=anak)

@app.route('/anak/<int:anak_id>/edit', methods=['GET', 'POST'])
def edit_data_anak(anak_id):
    anak = Anak.query.get_or_404(anak_id)

    if request.method == 'POST':
        anak.nik = request.form['nik']
        anak.nama = request.form['nama']
        anak.jk = request.form['jk']
        anak.tgl_lahir = request.form['tgl_lahir']
        anak.bb_lahir = request.form['bb_lahir']
        anak.tb_lahir = request.form['tb_lahir']
        anak.nama_ortu = request.form['nama_ortu']
        anak.prov = request.form['prov']
        anak.kab_kota = request.form['kab_kota']
        anak.kecamatan = request.form['kecamatan']
        anak.puskesmas = request.form['puskesmas']
        anak.desa = request.form['desa']
        anak.posyandu = request.form['posyandu']
        anak.rt = request.form['rt']
        anak.rw = request.form['rw']
        anak.alamat = request.form['alamat']
        anak.usia_ukur = request.form['usia_ukur']
        anak.berat = request.form['berat']
        anak.tinggi = request.form['tinggi']
        anak.lila = request.form['lila']
        anak.bb_u = request.form['bb_u']
        anak.tb_u = request.form['tb_u']
        anak.bb_tb = request.form['bb_tb']
        anak.naik_berat_badan = request.form['naik_berat_badan']

        db.session.commit()
        return redirect(url_for('data_anak'))

    return render_template('edit_data_anak.html', anak=anak)

@app.route('/anak/<int:anak_id>/hapus', methods=['GET'])
def hapus_data_anak(anak_id):
    from app import db
    from app.models import Anak

    anak = Anak.query.get_or_404(anak_id)
    db.session.delete(anak)
    db.session.commit()
    return redirect(url_for('data_anak'))

@app.route('/anak/<int:anak_id>/data-pengukuran')
def data_pengukuran(anak_id):
    pengukuran_list = Pengukuran.query.filter_by(id_anak=anak_id).all()
    pengukuran_list = Pengukuran.query.filter_by(id_anak=anak_id).all()
    return render_template('data_pengukuran.html', pengukuran_list=pengukuran_list, anak_id=anak_id)


@app.route('/anak/<int:anak_id>/data-pengukuran/input', methods=['GET', 'POST'])
def input_pengukuran(anak_id):
    

    if request.method == 'POST':
        anak = Anak.query.get_or_404(anak_id)
        pengukuran = Pengukuran.query.filter_by(id_anak=anak_id).order_by(Pengukuran.created_at.desc()).first()

        def hitung_umur_bulan(tgl_lahir):
            """
            Menghitung umur dalam bulan berdasarkan tanggal lahir hingga hari ini.

            :param tgl_lahir: datetime.date
            :return: int (umur dalam bulan)
            """
            today = date.today()
            tahun = today.year - tgl_lahir.year
            bulan = today.month - tgl_lahir.month
            hari = today.day - tgl_lahir.day

            umur_bulan = tahun * 12 + bulan
            if hari < 0:
                umur_bulan -= 1  # Jika belum genap bulan, kurangi 1 bulan

            return umur_bulan

        def hitung_zs_tbu(tb, umur_bulan, jenis_kelamin):
            # Load file WHO Z-score
            # df = pd.read_excel("data/bbu_who.xlsx", sheet_name="tb_u")
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'bbu_who.xlsx')
            df = pd.read_excel(file_path, sheet_name="tb_u")


            # Filter data berdasarkan umur dan jenis kelamin
            data = df[(df['Month'] == umur_bulan) & (df['JK'].str.lower() == jenis_kelamin.lower())]

            if data.empty:
                return None  # atau raise ValueError("Data WHO tidak ditemukan")

            median = data['M'].values[0]
            min1sd = data['SD1neg'].values[0]

            # Hitung Z-score TB/U
            zs = (tb - median) / (median - min1sd)

            return round(zs, 2)

        umur = hitung_umur_bulan(anak.tgl_lahir)
        tb_u = hitung_zs_tbu(pengukuran.tinggi, umur, anak.jk)
        print(tb_u)

        # pengukuran = Pengukuran(
        #     id_anak=anak_id,
        #     tinggi=request.form['tinggi'],
        #     berat=request.form['berat'],
        #     lila=request.form['lila'],
        #     lingkar_kepala=request.form['lingkar_kepala'],
        #     edema=request.form['edema'],
        #     ikut_kelas_ibu=request.form['ikut_kelas_ibu'],
        #     cara_ukur=request.form['cara_ukur'],
        #     created_at=datetime.utcnow()
        # )

        # db.session.add(pengukuran)
        # db.session.commit()

        return redirect(url_for('detail_anak', anak_id=anak_id))

    return render_template('input_pengukuran.html', anak_id=anak_id)


    

@app.route('/klasifikasi-stunting')
def klasifikasi_stunting():
    return render_template('klasifikasi_stunting.html')

@app.route('/klasifikasi-stunting/input')
def input_data():
    return render_template('input_data.html')

@app.route('/klasifikasi-stuting/<int:anak_id>')
def detail_klasifikasi(anak_id):
    return render_template('detail_klasifikasi.html', anak_id=anak_id)

@app.route('/klasifikasi/<int:anak_id>/edit')
def edit_klasifikasi(anak_id):
    return render_template('edit_klasifikasi.html', anak_id=anak_id)

@app.route('/klasifikasi/<int:anak_id>/hapus')
def hapus_klasifikasi(anak_id):
    # logika hapus data
    return redirect(url_for('klasifikasi_stunting'))

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")
