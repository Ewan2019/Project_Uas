from flask import Flask, render_template, request, url_for, flash, session, redirect  # Mengimpor modul yang dibutuhkan dari Flask
from flask_mysqldb import MySQL  # Mengimpor modul Flask-MySQLdb untuk koneksi database MySQL
from werkzeug.security import check_password_hash, generate_password_hash  # Mengimpor modul untuk enkripsi dan verifikasi password

app = Flask(__name__)  # Membuat objek Flask bernama 'app'
app.secret_key = 'secret_key'  # Ganti dengan secret key yang lebih aman

#koneksi  # Bagian konfigurasi koneksi database
app.config['MYSQL_HOST'] = 'localhost'  # Menetapkan host database
app.config['MYSQL_USER'] = 'root'  # Menetapkan username database
app.config['MYSQL_PASSWORD'] = ''  # Menetapkan password database
app.config['MYSQL_DB'] = 'recrutment'  # Menetapkan nama database

mysql = MySQL(app)  # Membuat objek MySQL untuk koneksi ke database

#indeks  # Dekorator untuk route '/' (halaman utama)
@app.route('/')
def indeks():
    if 'loggedin' in session:  # Memeriksa apakah pengguna sudah login (ada session 'loggedin')
        return render_template('indeks.html')  # Merender template 'indeks.html' jika sudah login
    flash('Harap Login dulu', 'danger')  # Menampilkan pesan flash 'Harap Login dulu' dengan kategori 'danger'
    return redirect(url_for('login'))  # Mengarahkan ke halaman login

#registrasi  # Dekorator untuk route '/registrasi' (halaman registrasi)
@app.route('/registrasi', methods=('GET','POST'))
def registrasi():
    if request.method == 'POST':  # Memeriksa apakah metode request adalah POST
        username = request.form['username']  # Mengambil username dari form
        email = request.form['email']  # Mengambil email dari form
        password = request.form['password']  # Mengambil password dari form

        #cek username atau email  # Memeriksa apakah username atau email sudah ada di database
        cursor = mysql.connection.cursor()  # Membuat objek cursor untuk menjalankan query
        cursor.execute('SELECT * FROM tb_login WHERE username=%s OR email=%s', (username, email, ))  # Menjalankan query untuk mencari username atau email
        akun = cursor.fetchone()  # Mengambil data akun yang ditemukan
        if akun is None:  # Jika akun tidak ditemukan
            cursor.execute('INSERT INTO tb_login VALUES (NULL, %s, %s, %s)', (username, email, generate_password_hash(password)))  # Menjalankan query untuk memasukkan data akun baru
            mysql.connection.commit()  # Melakukan commit perubahan ke database
            flash('Registrasi Berhasil', 'success')  # Menampilkan pesan flash 'Registrasi Berhasil' dengan kategori 'success'
        else:  # Jika akun ditemukan
            flash('Username atau email sudah ada', 'danger')  # Menampilkan pesan flash 'Username atau email sudah ada' dengan kategori 'danger'
    return render_template('registrasi.html')  # Merender template 'registrasi.html'

#login  # Dekorator untuk route '/login' (halaman login)
@app.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':  # Memeriksa apakah metode request adalah POST
        email = request.form['email']  # Mengambil email dari form
        password = request.form['password']  # Mengambil password dari form

        #cek data username  # Memeriksa data username di database
        cursor = mysql.connection.cursor()  # Membuat objek cursor untuk menjalankan query
        cursor.execute('SELECT * FROM tb_login WHERE email=%s', (email, ))  # Menjalankan query untuk mencari email
        akun = cursor.fetchone()  # Mengambil data akun yang ditemukan
        if akun is None:  # Jika akun tidak ditemukan
            flash('Login Gagal, Cek Username anda', 'danger')  # Menampilkan pesan flash 'Login Gagal, Cek Username anda' dengan kategori 'danger'
        elif not check_password_hash(akun[3], password):  # Jika akun ditemukan tetapi password salah
            flash('Login Gagal, Cek Password anda', 'danger')  # Menampilkan pesan flash 'Login Gagal, Cek Password anda' dengan kategori 'danger'
        else:  # Jika akun ditemukan dan password benar
            session['loggedin'] = True  # Menetapkan session 'loggedin' sebagai True
            session['username'] = akun[1]  # Menetapkan session 'username' dengan username dari database
            return redirect(url_for('indeks'))  # Mengarahkan ke halaman utama ('indeks')
    return render_template('login.html')  # Merender template 'login.html'

#logout  # Dekorator untuk route '/logout' (halaman logout)
@app.route('/logout')
def logout():
    session.pop('loggedin', None)  # Menghapus session 'loggedin'
    session.pop('username', None)  # Menghapus session 'username'
    return redirect(url_for('login'))  # Mengarahkan ke halaman login

#lowongan  # Dekorator untuk route '/lowongan' (halaman lowongan)
@app.route('/lowongan', methods=['GET', 'POST'])
def lowongan():
    if request.method == 'POST':  # Memeriksa apakah metode request adalah POST
        nik = request.form['nik']  # Mengambil NIK dari form

        # Cek data nik  # Memeriksa data NIK di database
        cursor = mysql.connection.cursor()  # Membuat objek cursor untuk menjalankan query
        cursor.execute('SELECT * FROM tb_datapelamar WHERE nik=%s', (nik, ))  # Menjalankan query untuk mencari NIK
        akun = cursor.fetchone()  # Mengambil data akun yang ditemukan
        if akun is None:  # Jika akun tidak ditemukan
            flash('Login Gagal, Cek nik anda', 'danger')  # Menampilkan pesan flash 'Login Gagal, Cek nik anda' dengan kategori 'danger'
        else:  # Jika akun ditemukan
            session['loggedin'] = True  # Menetapkan session 'loggedin' sebagai True
            session['nik'] = akun[2]  # Menetapkan session 'nik' dengan NIK dari database
            flash('Anda berhasil Apply', 'success')  # Menampilkan pesan flash 'Anda berhasil Apply' dengan kategori 'success'
            return redirect(url_for('lowongan'))  # Mengarahkan kembali ke halaman lowongan
    return render_template('lowongan.html')  # Merender template 'lowongan.html'

# Route /dataDiri menerima metode POST  # Dekorator untuk route '/dataDiri' (form data diri)
@app.route('/dataDiri', methods=['GET', 'POST'])
def dataDiri():
    if request.method == 'POST':  # Memeriksa apakah metode request adalah POST
        nama_pelamar = request.form['nama_pelamar']  # Mengambil nama pelamar dari form
        nik = request.form['nik']  # Mengambil NIK dari form
        nomer_hp = request.form['nomer_hp']  # Mengambil nomor HP dari form
        email = request.form['email']  # Mengambil email dari form
        domisili = request.form['domisili']  # Mengambil domisili dari form
        jenis_kelamin = request.form['jenis_kelamin']  # Mengambil jenis kelamin dari form
        tanggal_lahir = request.form['tanggal_lahir']  # Mengambil tanggal lahir dari form
        pendidikan = request.form['pendidikan']  # Mengambil pendidikan dari form
        usia = request.form['usia']  # Mengambil usia dari form

        # Periksa data pelamar
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_datapelamar WHERE nik=%s OR email=%s', (nik, email))
        existing_data = cursor.fetchone()

        if existing_data:
            flash('Data diri dengan NIK atau email yang sama sudah terdaftar. Silakan masukkan data diri ulang.', 'danger')
        else:
            cursor.execute('INSERT INTO tb_datapelamar VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nama_pelamar, nik, nomer_hp, email, domisili, jenis_kelamin, tanggal_lahir, pendidikan, usia))
            mysql.connection.commit()
            flash('Data diri berhasil ditambahkan', 'success')

    return render_template('dataDiri.html')  # Merender template 'dataDiri.html' untuk form data diri

# penerimaan calon karyawan futaba
@app.route('/futaba', methods=['GET', 'POST'])  # Dekorator untuk route '/futaba' (halaman penerimaan calon karyawan futaba)
def futaba():
    if request.method == 'POST':  # Memeriksa apakah metode request adalah POST
        nik = request.form['nik']  # Mengambil NIK dari form

        # Check data based on 'nik'  # Memeriksa data berdasarkan NIK
        cursor = mysql.connection.cursor()  # Membuat objek cursor untuk menjalankan query
        cursor.execute('SELECT * FROM tb_datapelamar WHERE nik=%s', (nik, ))  # Menjalankan query untuk mencari data pelamar berdasarkan NIK
        akun = cursor.fetchone()  # Mengambil data pelamar yang ditemukan
        if akun is None:  # Jika data pelamar tidak ditemukan
            flash('Login Gagal, Cek nik anda', 'danger')  # Menampilkan pesan flash 'Login Gagal, Cek nik anda' dengan kategori 'danger'
        else:  # Jika data pelamar ditemukan
            # Insert data into tb_futaba  # Memasukkan data pelamar ke dalam tabel tb_futaba
            cursor.execute('INSERT INTO tb_futaba VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (akun[1], akun[2], akun[3], akun[4], akun[5], akun[6], akun[7], akun[8], akun[9]))  # Menjalankan query untuk memasukkan data pelamar ke dalam tb_futaba
            mysql.connection.commit()  # Melakukan commit perubahan ke database
            flash('Berhasil apply', 'success')  # Menampilkan pesan flash 'Berhasil apply' dengan kategori 'success'
            return redirect(url_for('futaba'))  # Mengarahkan kembali ke halaman futaba
    return render_template('futaba.html')  # Merender template 'futaba.html' untuk halaman penerimaan calon karyawan futaba

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor()

            cursor.execute('SELECT * FROM tb_login WHERE username=%s', (username,))
            akun = cursor.fetchone()

            if akun:
                if check_password_hash(akun[3], password):
                    cursor.execute('DELETE FROM tb_login WHERE username=%s', (username,))
                    mysql.connection.commit()

                    flash('Akun berhasil dihapus', 'success')
                    return redirect(url_for('logout'))
                else:
                    flash('Password tidak cocok', 'danger')
            else:
                flash('Akun tidak ditemukan', 'danger')
        
        elif 'nik' in request.form:
            nik = request.form['nik']
            cursor = mysql.connection.cursor()

            cursor.execute('SELECT * FROM tb_datapelamar WHERE nik=%s', (nik,))
            data_pelamar = cursor.fetchone()

            if data_pelamar:
                cursor.execute('DELETE FROM tb_datapelamar WHERE nik=%s', (nik,))
                mysql.connection.commit()

                flash('Data pelamar berhasil dihapus', 'success')
            else:
                flash('Data pelamar tidak ditemukan', 'danger')

    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)