from app import app
from flask import render_template, redirect, url_for, request
from app.models import Anak, Pengukuran, Detail_anak, Klasifikasi, User
from app import db
from datetime import datetime, date
import pandas as pd
import os
import joblib
import numpy as np
import json
from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import login_required


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')

svm_rbf = joblib.load(os.path.join(MODEL_DIR, 'model_svm.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
le = joblib.load(os.path.join(MODEL_DIR, 'label.pkl'))


# from app.generateAgeMonth import hitung_umur_bulan
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Login berhasil!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Username atau password salah!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash("Password tidak sama!", "danger")
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password)

            if User.query.filter_by(username=username).first():
                flash("Username sudah dipakai!", "danger")
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash("Email sudah terdaftar!", "danger")
                return redirect(url_for('register'))

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registrasi berhasil, silakan login.", "success")
            return redirect(url_for('login'))

        return render_template('register.html')

@app.route('/')
@login_required
def dashboard():
    if 'user_id' not in session:
        flash("Harap login dulu!", "warning")
        return redirect(url_for('login'))

    total_anak = Anak.query.count()
    
    klasifikasi_list = Klasifikasi.query.all()
    total_normal = 0
    total_stunting = 0
    total_stunting_parah = 0

    for item in klasifikasi_list:
        if item.status_stunting == "Normal":
            total_normal += 1
        elif item.status_stunting == "Stunting":
            total_stunting += 1
        elif item.status_stunting == "Stunting Parah":
            total_stunting_parah += 1

    data = {
        'total_anak': total_anak,
        'total_normal': total_normal,
        'total_stunting': total_stunting,
        'total_stunting_parah': total_stunting_parah,
    }

    chart_data = {
        "labels": ["Normal", "Stunting", "Stunting Parah"],
        "values": [total_normal, total_stunting, total_stunting_parah]
    }

    return render_template('dashboard.html', data=data, chart_data=json.dumps(chart_data))


@app.route('/data-anak')
@login_required
def data_anak():
    anak_list = Anak.query.all()
    return render_template('data_anak.html', anak_list=anak_list)

@app.route('/anak/input', methods=['GET', 'POST'])
@login_required
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

        flash('Data berhasil ditambahkan!', 'success')
        return redirect(url_for('data_anak'))

    return render_template('input_data_anak.html')


# @app.route('/anak/input')
# def input_data_anak():
#     return render_template('input_data_anak.html')

@app.route('/anak/<int:anak_id>')
@login_required
def detail_anak(anak_id):
    anak = Anak.query.get_or_404(anak_id)
    return render_template('detail_anak.html', anak=anak)

@app.route('/anak/<int:anak_id>/edit', methods=['GET', 'POST'])
@login_required
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
@login_required
def hapus_data_anak(anak_id):
    from app import db
    from app.models import Anak

    anak = Anak.query.get_or_404(anak_id)
    db.session.delete(anak)
    db.session.commit()
    return redirect(url_for('data_anak'))

@app.route('/anak/<int:anak_id>/data-pengukuran')
@login_required
def data_pengukuran(anak_id):
    anak = Anak.query.get_or_404(anak_id)

    #print(pengukuran_list)
    pengukuran_list = (
        db.session.query(Pengukuran, Detail_anak)
        .outerjoin(Detail_anak, (Pengukuran.id_anak == Detail_anak.id_anak) & (Pengukuran.created_at == Detail_anak.tgl_pengukuran))
        .filter(Pengukuran.id_anak == anak_id)
        .order_by(Pengukuran.created_at.desc())
        .all()
    )

    # Ambil satu detail terbaru berdasarkan tanggal pengukuran
    detail_terakhir = (
        Detail_anak.query
        .filter_by(id_anak=anak_id)
        .order_by(Detail_anak.tgl_pengukuran.desc())
        .first()
    )

    return render_template('data_pengukuran.html', pengukuran_list=pengukuran_list, anak=anak, detail_terakhir=detail_terakhir, anak_id=anak_id)


@app.route('/anak/<int:anak_id>/data-pengukuran/input', methods=['GET', 'POST'])
@login_required
def input_pengukuran(anak_id):

    if request.method == 'POST':
        anak = Anak.query.get_or_404(anak_id)
        # pengukuran = Pengukuran.query.filter_by(id_anak=anak_id).order_by(Pengukuran.created_at.desc()).first()
        tinggi = float(request.form.get('tinggi'))
        berat = float(request.form.get('berat'))

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
            file_path = os.path.join(os.path.dirname(__file__), 'data', 'bbu_who.xlsx')
            df = pd.read_excel(file_path, sheet_name="tbu")

            # Filter data berdasarkan umur dan jenis kelamin
            data = df[(df['Month'] == umur_bulan) & (df['Sex'].str.lower() == jenis_kelamin)]


            print(df)
            print(data)
            if data.empty:
                return None  # atau raise ValueError("Data WHO tidak ditemukan")

            median = float(data['M'].values[0])
            min1sd = float(data['SD1neg'].values[0])

            # # Hitung Z-score TB/U
            zs = (tb - median) / (median - min1sd)

            print("m", data['M'])
            print("sd", data['SD1neg'])
            # print(zs)

            return zs
        
        def hitung_zs_bbu(bb, umur_bulan, jenis_kelamin):
            # Load file WHO Z-score
            file_path = os.path.join(os.path.dirname(__file__), 'data', 'bbu_who.xlsx')
            df = pd.read_excel(file_path, sheet_name="bbu")

            # Filter data berdasarkan umur dan jenis kelamin
            data = df[(df['Month'] == umur_bulan) & (df['Sex'].str.lower() == jenis_kelamin)]

            if data.empty:
                return None  # atau raise ValueError("Data WHO tidak ditemukan")

            median = float(data['M'].values[0])
            min1sd = float(data['SD1neg'].values[0])

            # # Hitung Z-score TB/U
            zs = (bb - median) / (median - min1sd)

            return zs
        
        def hitung_zs_bbtb(bb, tb, jenis_kelamin):
            # Load file WHO Z-score
            file_path = os.path.join(os.path.dirname(__file__), 'data', 'bbu_who.xlsx')
            df = pd.read_excel(file_path, sheet_name="bbtb")

            # Filter data berdasarkan umur dan jenis kelamin
            data = df[(df['Length'] == tb) & (df['Sex'].str.lower() == jenis_kelamin)]

            if data.empty:
                return None  # atau raise ValueError("Data WHO tidak ditemukan")

            median = float(data['M'].values[0])
            min1sd = float(data['SD1neg'].values[0])

            # # Hitung Z-score TB/U
            zs = (bb - median) / (median - min1sd)

            return zs
        
        

        jenis_kelamin = anak.jk.lower()
        umur = hitung_umur_bulan(anak.tgl_lahir)
        tb_u = hitung_zs_tbu(tinggi, umur, jenis_kelamin)
        bb_u = hitung_zs_bbu(berat, umur, jenis_kelamin)
        bb_tb = hitung_zs_bbtb(berat, tinggi, jenis_kelamin)

        print({tb_u, bb_u, bb_tb})
 


        pengukuran = Pengukuran(
            id_anak=anak_id,
            tinggi=request.form['tinggi'],
            berat=request.form['berat'],
            lila=request.form['lila'],
            lingkar_kepala=request.form['lingkar_kepala'],
            edema=request.form['edema'],
            ikut_kelas_ibu=request.form['ikut_kelas_ibu'],
            cara_ukur=request.form['cara_ukur'],
            created_at=datetime.utcnow()
        )

        detail_anak = Detail_anak(
            id_anak=anak_id,
            tinggi=request.form['tinggi'],
            berat=request.form['berat'],
            umur=umur,
            tgl_pengukuran=datetime.utcnow(),
            lila=request.form['lila'],
            zs_bb_u=bb_u,
            zs_tb_u=tb_u,
            zs_bb_tb=bb_tb,
            lingkar_kepala=request.form['lingkar_kepala'],
            edema=request.form['edema'],
            ikut_kelas_ibu=request.form['ikut_kelas_ibu'],
            cara_ukur=request.form['cara_ukur'],
            created_at=datetime.utcnow()
        )

        db.session.add(pengukuran)
        db.session.add(detail_anak)
        db.session.commit()

        
        flash('Data berhasil ditambahkan!', 'success')
        return redirect(url_for('detail_anak', anak_id=anak_id))
    
    return render_template('input_pengukuran.html', anak_id=anak_id)


@app.route('/anak/<int:anak_id>/data-pengukuran/<int:pengukuran_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_pengukuran(anak_id, pengukuran_id):
    anak = Anak.query.get_or_404(anak_id)
    pengukuran = Pengukuran.query.get_or_404(pengukuran_id)
    detail_anak = Detail_anak.query.filter_by(id_anak=anak_id, tgl_pengukuran=pengukuran.created_at).first()

    if request.method == 'POST':
        tinggi = float(request.form.get('tinggi'))
        berat = float(request.form.get('berat'))

        # Fungsi helper umur
        def hitung_umur_bulan(tgl_lahir):
            today = date.today()
            tahun = today.year - tgl_lahir.year
            bulan = today.month - tgl_lahir.month
            hari = today.day - tgl_lahir.day
            umur_bulan = tahun * 12 + bulan
            if hari < 0:
                umur_bulan -= 1
            return umur_bulan

        # Fungsi hitung Z-score (sama seperti input)
        def hitung_zs_tbu(tb, umur_bulan, jenis_kelamin):
            file_path = os.path.join(os.path.dirname(__file__), 'data', 'bbu_who.xlsx')
            df = pd.read_excel(file_path, sheet_name="tbu")
            data = df[(df['Month'] == umur_bulan) & (df['Sex'].str.lower() == jenis_kelamin)]
            if data.empty:
                return None
            median = float(data['M'].values[0])
            min1sd = float(data['SD1neg'].values[0])
            return (tb - median) / (median - min1sd)

        def hitung_zs_bbu(bb, umur_bulan, jenis_kelamin):
            file_path = os.path.join(os.path.dirname(__file__), 'data', 'bbu_who.xlsx')
            df = pd.read_excel(file_path, sheet_name="bbu")
            data = df[(df['Month'] == umur_bulan) & (df['Sex'].str.lower() == jenis_kelamin)]
            if data.empty:
                return None
            median = float(data['M'].values[0])
            min1sd = float(data['SD1neg'].values[0])
            return (bb - median) / (median - min1sd)

        def hitung_zs_bbtb(bb, tb, jenis_kelamin):
            file_path = os.path.join(os.path.dirname(__file__), 'data', 'bbu_who.xlsx')
            df = pd.read_excel(file_path, sheet_name="bbtb")
            data = df[(df['Length'] == tb) & (df['Sex'].str.lower() == jenis_kelamin)]
            if data.empty:
                return None
            median = float(data['M'].values[0])
            min1sd = float(data['SD1neg'].values[0])
            return (bb - median) / (median - min1sd)

        # Hitung ulang z-score
        jenis_kelamin = anak.jk.lower()
        umur = hitung_umur_bulan(anak.tgl_lahir)
        tb_u = hitung_zs_tbu(tinggi, umur, jenis_kelamin)
        bb_u = hitung_zs_bbu(berat, umur, jenis_kelamin)
        bb_tb = hitung_zs_bbtb(berat, tinggi, jenis_kelamin)

        # Update data pengukuran
        pengukuran.tinggi = request.form['tinggi']
        pengukuran.berat = request.form['berat']
        pengukuran.lila = request.form['lila']
        pengukuran.lingkar_kepala = request.form['lingkar_kepala']
        pengukuran.edema = request.form['edema']
        pengukuran.ikut_kelas_ibu = request.form['ikut_kelas_ibu']
        pengukuran.cara_ukur = request.form['cara_ukur']
        pengukuran.updated_at = datetime.utcnow()

        # Update detail anak
        if detail_anak:
            detail_anak.tinggi = request.form['tinggi']
            detail_anak.berat = request.form['berat']
            detail_anak.umur = umur
            detail_anak.lila = request.form['lila']
            detail_anak.zs_bb_u = bb_u
            detail_anak.zs_tb_u = tb_u
            detail_anak.zs_bb_tb = bb_tb
            detail_anak.lingkar_kepala = request.form['lingkar_kepala']
            detail_anak.edema = request.form['edema']
            detail_anak.ikut_kelas_ibu = request.form['ikut_kelas_ibu']
            detail_anak.cara_ukur = request.form['cara_ukur']
            detail_anak.updated_at = datetime.utcnow()

        db.session.commit()

        flash('Data pengukuran berhasil diperbarui!', 'success')
        return redirect(url_for('detail_anak', anak_id=anak_id))

    return render_template('edit_data_pengukuran.html', anak=anak, pengukuran=pengukuran, detail_anak=detail_anak)

@app.route('/anak/<int:anak_id>/data-pengukuran/<int:pengukuran_id>/delete', methods=['POST'])
@login_required
def delete_pengukuran(anak_id, pengukuran_id):
    pengukuran = Pengukuran.query.get_or_404(pengukuran_id)
    detail_anak = Detail_anak.query.filter_by(
        id_anak=anak_id, 
        tgl_pengukuran=pengukuran.created_at
    ).first()

    # hapus data dari db
    db.session.delete(pengukuran)
    if detail_anak:
        db.session.delete(detail_anak)
    db.session.commit()

    flash('Data pengukuran berhasil dihapus!', 'success')
    return redirect(url_for('detail_anak', anak_id=anak_id))


@app.route('/klasifikasi-stunting')
@login_required
def klasifikasi_stunting():
    klasifikasi_list = Klasifikasi.query.all()
    return render_template('klasifikasi_stunting.html', klasifikasi_list=klasifikasi_list)



# Fungsi prediksi
def prediksi_manual(jenis_kelamin, umur, berat, tinggi):
    """
    Fungsi prediksi status stunting berdasarkan input manual.

    Parameter:
    - jenis_kelamin: 'L' atau 'P'
    - umur: dalam bulan (int/float)
    - berat: dalam kg (float)
    - tinggi: dalam cm (float)
    """
    # Encode jenis kelamin: 'L' -> 0, 'P' -> 1
    jk_encoded = 0 if jenis_kelamin.upper() == 'L' else 1

    # Pastikan umur, berat, tinggi adalah float
    umur = float(umur)
    berat = float(berat)
    tinggi = float(tinggi)

    # Normalisasi fitur umur, berat, tinggi
    data_to_scale = np.array([[umur, berat, tinggi]])
    scaled_data = scaler.transform(data_to_scale)

    # Gabungkan jenis kelamin (tidak dinormalisasi) + data yang sudah dinormalisasi
    final_data = np.concatenate([[jk_encoded], scaled_data[0]])
    final_data = final_data.reshape(1, -1)  # pastikan bentuk (1, 4) untuk model

    # Prediksi menggunakan model SVM
    prediksi = svm_rbf.predict(final_data)

    # Decode hasil prediksi ke nama label
    hasil_label = le.inverse_transform(prediksi)

    return hasil_label[0]


# Route input
@app.route('/klasifikasi-stunting/input', methods=['GET', 'POST'])
@login_required
def input_data():
    if request.method == 'POST':
        nama = request.form.get('nama')
        jk = request.form.get('jeniskelamin')  # name di input form harus 'jeniskelamin'
        umur = request.form.get('umur')
        berat = request.form.get('berat')
        tinggi = request.form.get('tinggi')


        # Prediksi status stunting
        status = prediksi_manual(jk, umur, berat, tinggi)
        print(status)
        print(berat)
        print(tinggi)
        print(jk)


        if status == 0:
            status_label = "Normal"
        elif status == 1:
            status_label = "Stunting"
        elif status == 2:
            status_label = "Stunting Parah"
        else:
            status_label = "Tidak Diketahui"


        # Simpan ke database
        new_klasifikasi = Klasifikasi(
            nama=nama,
            jk=jk,
            umur=umur,
            berat=berat,
            status_gizi_bbu="",
            tinggi=tinggi,
            status_stunting=status_label,
            created_at=datetime.utcnow()
        )

        db.session.add(new_klasifikasi)
        db.session.commit()
        return redirect(url_for('klasifikasi_stunting'))  # sesuaikan dengan nama fungsi route tampilan data

    return render_template('input_data.html')

@app.route('/klasifikasi-stuting/<int:klasifikasi_id>')
@login_required
def detail_klasifikasi(klasifikasi_id):
    detail_klasifikasi = Klasifikasi.query.get_or_404(klasifikasi_id)
    return render_template('detail_klasifikasi.html', klasifikasi_id=klasifikasi_id)

@app.route('/klasifikasi/<int:klasifikasi_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_klasifikasi(klasifikasi_id):
    detail_klasifikasi = Klasifikasi.query.get_or_404(klasifikasi_id)

    if request.method == 'POST':
        nama = request.form.get('nama')
        jk = request.form.get('jeniskelamin')
        umur = request.form.get('umur')
        berat = request.form.get('berat')
        tinggi = request.form.get('tinggi')

        detail_klasifikasi.nama = nama
        detail_klasifikasi.jk = jk
        detail_klasifikasi.umur = umur
        detail_klasifikasi.berat = berat
        detail_klasifikasi.tinggi = tinggi

        # Prediksi ulang status stunting setelah diubah
        status_prediksi_angka = prediksi_manual(jk, umur, berat, tinggi)
        
        # --- PERBAIKAN DILAKUKAN DI SINI ---
        # Mengubah hasil prediksi angka menjadi label teks
        if status_prediksi_angka == 0:
            status_label = "Normal"
        elif status_prediksi_angka == 1:
            status_label = "Stunting"
        elif status_prediksi_angka == 2:
            status_label = "Stunting Parah"
        else:
            status_label = "Tidak Diketahui"
        
        # Memperbarui kolom status_stunting dengan label teks
        detail_klasifikasi.status_stunting = status_label
            
        db.session.commit()
        flash('Data klasifikasi berhasil diperbarui!', 'success')
        return redirect(url_for('klasifikasi_stunting'))
    
    return render_template('edit_klasifikasi.html', klasifikasi=detail_klasifikasi)

@app.route('/klasifikasi/<int:klasifikasi_id>/hapus')
@login_required
def hapus_klasifikasi(klasifikasi_id):
    from app import db
    from app.models import Anak

    detail_klasifikasi = Klasifikasi.query.get_or_404(klasifikasi_id)
    db.session.delete(detail_klasifikasi)
    db.session.commit()
    return redirect(url_for('klasifikasi_stunting'))



@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Anda berhasil logout.", "info")
    return redirect(url_for('login'))
