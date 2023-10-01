import numpy as np
#  Membaca file CSV
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data.append(line.strip().split(','))
    return data
   
# Menjalankan fungsi untuk membaca data CSV
csv_file_path = 'DATA MHS.csv'  # Ganti dengan path file CSV Anda
data = read_csv('DATA MHS.csv')

# Menampilkan data yang sudah dibaca
for row in data:
    print(row)
# Memisahkan atribut (X) dan label (y)
def separate_attributes_and_labels(data):
    X = []
    y = []
    for row in data:
        attributes = row[1:7]  # Kolom "nama", "nim", "nilai_sok", dan "nilai_data_mining"
        label = row[-1]
          # Kolom "label"
        X.append(attributes)
        y.append(label)
    return X, y
# Memisahkan atribut (X) dan label (y)
X, y = separate_attributes_and_labels(data)

# Menampilkan atribut (X) dan label (y)
print("Atribut (X):")
for row in X:
    print(row)

print("\nLabel (y):")
for label in y:
    print(label)
import math
def setMaxMinData(self, maxD, minD):
    self.normalMax = maxD
    self.normalMin = minD
def generateMinMaxData(self):
    self.normalMax = self.generateNormal(len(self.data[0])-1, -99999999)
    self.normalMin = self.generateNormal(len(self.data[0])-1, 99999999)
    for i in self.data:
        for j in range(len(i)-1):
            if self.normalMax[j] < i[j]:
                self.normalMax[j] = i[j]
            if self.normalMin[j] > i[j]:
                self.normalMin[j] = i[j]

def normalizeData(self):
    self.dataNormal = []
    for i in range(len(self.data)):
        temp = []
        for j in range(len(self.data[i])-1):
            temp.append((self.data[i][j] - self.normalMin[j]) / ((self.normalMax[j] - self.normalMin[j]) * 1.0))
        self.dataNormal.append(temp)
def generateAlpha(self):
    self.alphaList = []
    self.deltaAlpha = []
    self.Error = []
    for i in range(len(self.dataNormal)):
        self.alphaList.append(self.alpha)
        self.deltaAlpha.append(1)
        self.Error.append(0)
def CalculateKernel(self, x, y):
    result = 0
    for idx in range(len(x)):
        result += x[idx] * y[idx]
    result = math.pow(result + self.constanta, 2)
    return result
def CalculateHessian(self, kelasX, kelasY, x, y):
    return kelasX * kelasY * (self.CalculateKernel(x, y) + math.pow(self.lambd, 2))
def getKelasData(self):
    for i in self.data:
        self.classified.append(i[-1])
def Hessian(self):
    self.getKelasData()
    result = []
    for i in range(len(self.dataNormal)):
        temp_result_in_line = []
        for j in range(len(self.dataNormal)):
            temp_result_in_line.append(
                self.CalculateHessian(self.classified[i], self.classified[j], self.dataNormal[i], self.dataNormal[j])
            )
        result.append(temp_result_in_line)
    self.Hessian_Matrix = result
def calculateE(self, D, a):
    E = 0
    for i in range(len(D)):
        E += a[i] * D[i] * 1.0
    return E
def calculateDeltaAlpha(self, E, a):
    deltaAlpha = min(max(self.gamma * (1.0 - E), a), self.constanta - a)
    return deltaAlpha
def generateAlpha(self):
    self.alphaList = []
    self.deltaAlpha = []
    self.Error = []
    for i in range(len(self.dataNormal)):
        self.alphaList.append(self.alpha)
        self.deltaAlpha.append(1)
        self.Error.append(0)

def updateAlpha(self, deltaA, a):
    return a + deltaA
def calculateFX(self, indexPN):
    hasil = 0
    for i in range(len(self.alphaList)):
        hasil += self.alphaList[i] * self.classified[i] * self.Hessian_Matrix[indexPN][i]
    return hasil

def calculateB(self):
    hasil = 0
    for i in self.indexPN:
        hasil += self.calculateFX(i)
    hasil = hasil * (-0.5)
    print("B",hasil)
    return hasil
def generateMatrixKernel(self, xTest):
    mat_ = []
    for i in self.dataNormal:
        mat_.append(self.CalculateKernel(i, xTest))

    # print("matkernel", mat_)
    print("matkernel", mat_)
    return mat_
# Data aktual (ground truth)
y_true = [1, 1, 1, -1, 1, 1, 1, -1, 1, 1]
x_true = [1, 1, 1, -1, 1, 1, 1, -1, 1, 1]
# Prediksi model
#y_pred = [1, -1, 1, 1, 1, 1, 1, -1, 1, 1]

# Menghitung jumlah prediksi yang benar
correct_predictions = 0
total_predictions = len(y_true)

for i in range(total_predictions):
    if y_true[i] == y_pred[i]:
        correct_predictions += 1

# Menghitung akurasi
accuracy = correct_predictions / total_predictions

print(f'Akurasi: {accuracy * 100:.2f}%')

