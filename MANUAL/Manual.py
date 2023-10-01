import numpy as np
# def svm(x):
    # Data latih

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

X = np.array([
    [85, 0, 85, 0],
    [70, 85, 70, 72],
    [89, 85, 50, 85],
    [85, 89, 89, 85],
    [75, 75, 72, 85]
])
y = np.array([1, -1, 1, -1, 1])

# Inisialisasi bobot (a) dan bias (b)
a = np.zeros(X.shape[0])
b = 0

# Parameter pembelajaran
C = 1
lambda_val = 0.5

# Definisi fungsi kernel RBF
def rbf_kernel(x1, x2, gamma=0.1):
    return np.exp(-gamma * np.linalg.norm(x1 - x2)**2)

# Menghitung matriks Hessian dengan kernel RBF
Hessian = np.zeros((X.shape[0], X.shape[0]))
for i in range(X.shape[0]):
    for j in range(X.shape[0]):
        Hessian[i][j] = y[i] * y[j] * rbf_kernel(X[i], X[j])

# Proses pelatihan SVM dengan kernel RBF
for epoch in range(100):
    for i in range(X.shape[0]):
        Ei = np.dot(a * y, Hessian[i]) + b - y[i]
        if (y[i] * Ei < -0.01 and a[i] < C) or (y[i] * Ei > 0.01 and a[i] > 0):
            # Pilih indeks acak j yang berbeda dengan i
            j = i
            while j == i:
                j = np.random.randint(0, X.shape[0])

            Ej = np.dot(a * y, Hessian[j]) + b - y[j]

            # Simpan nilai lama
            ai_old, aj_old = a[i], a[j]
            bi_old, bj_old = b, b

            # Hitung batas atas (H) dan batas bawah (L)
            if y[i] != y[j]:
                L = max(0, aj_old - ai_old)
                H = min(C, C + aj_old - ai_old)
            else:
                L = max(0, ai_old + aj_old - C)
                H = min(C, ai_old + aj_old)

            if L == H:
                continue

            # Hitung nilai baru untuk aj
            eta = 2 * rbf_kernel(X[i], X[j]) - rbf_kernel(X[i], X[i]) - rbf_kernel(X[j], X[j])
            if eta >= 0:
                continue
            aj_new = aj_old - y[j] * (Ei - Ej) / eta
            aj_new = max(L, min(H, aj_new))

            if np.abs(aj_new - aj_old) < 0.00001:
                continue

            # Hitung nilai baru untuk ai
            ai_new = ai_old + y[i] * y[j] * (aj_old - aj_new)

            # Hitung b
            bi_new = b - Ei - y[i] * (ai_new - ai_old) * rbf_kernel(X[i], X[i]) - y[j] * (aj_new - aj_old) * rbf_kernel(X[i], X[j])
            bj_new = b - Ej - y[i] * (ai_new - ai_old) * rbf_kernel(X[i], X[j]) - y[j] * (aj_new - aj_old) * rbf_kernel(X[j], X[j])

            if 0 < ai_new < C:
                b = bi_new
            elif 0 < aj_new < C:
                b = bj_new
            else:
                b = (bi_new + bj_new) / 2

            # Update nilai a
            a[i] = ai_new
            a[j] = aj_new

# Data uji
X_test = np.array([
    [77, 75, 70, 75],
    [70, 86, 70, 70]
])

# Melakukan prediksi
predictions = []
for i in range(X_test.shape[0]):
    f_x = np.dot(a * y, np.array([rbf_kernel(X[j], X_test[i]) for j in range(X.shape[0])])) + b
    if f_x > 0:
        predictions.append(1)
    else:
        predictions.append(-1)

# Menampilkan hasil prediksi
print("Hasil Prediksi:", predictions)
# return predictions