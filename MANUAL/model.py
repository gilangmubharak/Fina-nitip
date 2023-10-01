from flask import Flask, request, render_template
import pickle
from sklearn import svm

# Import kelas SVM dari file yang sesuai
from model import manual  # Gantilah dengan nama file dan kelas yang sesuai

# Inisialisasi objek SVM
svm = manual()

# Lakukan langkah-langkah pelatihan yang sesuai (seperti generateMinMaxData, generateAlpha, dll.)

# Lakukan prediksi pada data uji
xTest = [0.2, 0.3, 0.4]  # Gantilah dengan data uji yang sesuai
predicted_class = svm.fxTest(xTest)  # Lakukan prediksi

#membuat model
model_svm = pickle.load(open('model.sav','rb'))



app = Flask(__name__)

# Memuat model
with open('model.sav', 'rb') as model_file:
    diabetes_model = pickle.load(model_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    SPK = float(request.form['SPK'])
    Datamining = float(request.form['Data Mining'])
    Pemrograman = float(request.form['Pemrograman'])
    machinelearning = float(request.form['machinelearning'])
   

    # Prediksi
    svm_prediction =([[SPK,  Datamining, Pemrograman, machinelearning]])

    if svm_prediction[0] == 0:
        svm_prediction= 'MHS ambil RPL'
    else:
        svm_prediction = 'MHS ambil Data'

    return render_template('result.html', predict=svm_prediction)

if __name__ == '__main__':
    app.run(debug=True)
