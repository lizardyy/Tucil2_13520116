# Tugas Kecil 2 IF2211 Strategi Algoritma Semester II tahun 2021/2022

Implementasi Convex Hull untuk Visualisasi Tes Linear Separability Dataset dengan Algoritma Divide and Conquer

## Disusun Oleh

Nama : Mahesa Lizardy

NIM : 13520116

Kelas : 2

## cara penggunaan

lakukan command berikut pada terminal

```
python src/main.py
```

## Mengganti dataset

pada file main.py ganti dataset menjadi data yang lain pada

```
data = datasets.load_iris()
```

misalnya

```
data = datasets.load_wine()`
```

## Mengganti kolom

pada file main.py ganti nomor kolom pada

```
plt.xlabel(data.feature_names[1]) plt.ylabel(data.feature_names[2])
```

dan

```
bucket = bucket.iloc[:, [1, 2]].values`
```
