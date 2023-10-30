import numpy as np
from flask import Flask, render_template, request, url_for, redirect, session, flash
import pymysql.cursors
import bcrypt
from model_svm import predict_with_svm, X_train, Y_train, a, b

app = Flask(__name__)

app.secret_key = 'svmprogram'

conn = cursor = None

def openDatabase():
    global conn, cursor
    conn = pymysql.connect(host="localhost",user="root",password="",database="svm_db")
    cursor = conn.cursor()

def closeDatabase():
    global conn, cursor
    cursor.close()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].strip().encode('utf-8')
        openDatabase()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        closeDatabase()

        if user is not None and len(user) > 0:
            if bcrypt.checkpw(password, user[3].encode('utf-8')):
                session['username'] = user[1]
                session['email'] = user[2]
                return redirect(url_for('predict'))
            else:
                flash("Username and Password do not match")
                return redirect(url_for('login'))
        else:
            flash("User not found")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].strip().encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        openDatabase()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hash_password))
        conn.commit()
        closeDatabase()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/", methods=['GET', 'POST'])
def predict():
    nama = ""
    nim = ""
    if 'username' in session:
        if request.method == 'POST':
            REKAYASA_PL = int(request.form.get('REKAYASA PL', 0))
            DATA_MINING = int(request.form.get('DATA_MINING', 0))
            PEMROG = int(request.form.get('PEMROG', 0))
            MACHINE = int(request.form.get('MACHINE', 0))
            DEEP_LEARNING = int(request.form.get('DEEP_LEARNING', 0))
            BIG_DATA = int(request.form.get('BIG_DATA', 0))
            PBA = int(request.form.get('PBA', 0))
            UJI_KPL = int(request.form.get('UJI_KPL', 0))
            DESAIN_ANTARMUKA = int(request.form.get('DESAIN_ANTARMUKA', 0))
            GAME_DEVELOP = int(request.form.get('GAME_DEVELOP', 0))
            WEB_SEMANTIC = int(request.form.get('WEB_SEMANTIC', 0))
            VISUALISASI_DATA = int(request.form.get('VISUALISASI_DATA', 0))
            nama = request.form.get('NAMA')
            nim = request.form.get('NIM')
            data_nilai = np.array([[REKAYASA_PL, DATA_MINING, PEMROG, MACHINE, DEEP_LEARNING, BIG_DATA,PBA,UJI_KPL,DESAIN_ANTARMUKA, GAME_DEVELOP,WEB_SEMANTIC,VISUALISASI_DATA ]])
            prediksi_user = predict_with_svm(X_train, Y_train, data_nilai, a, b)
            kategori = {-1: 'REKAYASA PERANGKAT LUNAK', 1: 'DATA MINING'}
            hasil_prediksi = kategori.get(prediksi_user[0])
            session['nama'] = request.form.get('NAMA')
            session['nim'] = request.form.get('NIM')
            print(hasil_prediksi)
            return render_template("index.html", data=hasil_prediksi,nama=nama, nim=nim)
        return render_template("index.html", nama=nama, nim=nim)
    return render_template("login.html")
@app.route('/referensi')
def referensi():
    return render_template('referensi.html')

@app.route('/check-session')
def check_session():
    if 'username' in session:
        return f'Sesi dengan kunci "username" sudah ada: {session["username"]}'
    else:
        return 'Sesi belum ada.'




if __name__ == '__main__':
    app.run(debug=True)
