import numpy as np
import pandas as pd
from flask import Flask, render_template, request, url_for, redirect, session, flash
from sklearn import svm
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
# Model Login
app.secret_key = "Membuat Login Flask"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'manual'  # Remove '.sql' from the database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Model Predict
data = pd.read_csv('DATA MHS.csv')
df = pd.DataFrame(data, columns=['NAMA', 'NIM', 'PRODI', 'SPK', 'DATA_MINING', 'PEMROG', 'MACHINE', 'OUTCOME'])

x = df[['SPK', 'DATA_MINING', 'PEMROG', 'MACHINE']].values
y = df['OUTCOME'].values

x_train = x
y_train = y

model = svm.SVC(kernel='linear', C=1.0)
model.fit(x_train, y_train)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user is not None and len(user) > 0:
            if bcrypt.checkpw(password, user['password'].encode('utf-8')):
                session['username'] = user['username']
                session['email'] = user['email']
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
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hash_password))
        mysql.connection.commit()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/predict", methods=["POST"])
def predict():
    input_data = request.form['input_data']
    float_features = [float(x) for x in input_data.split()]
    feature = [np.array(float_features)]
    prediction = model.predict(feature)
    return render_template("index.html", prediction_text="Hasil Rekomendasi: {}".format(prediction[0]))


if __name__ == '__main__':
    app.run(debug=True)
