# main.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import datasets

# visualisasi hasil ConvexHull
import matplotlib.pyplot as plt

# implementasi Convex Hull
import myConvexHull as Ch

data = datasets.load_breast_cancer() #data yang dipakai

#create a DataFrame
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)
print(df.shape)
df.head()

plt.figure(figsize=(10, 6))
colors = ['b', 'r', 'g']
plt.title('ash vs alcalinity_of_ash')
plt.xlabel(data.feature_names[0]) # data untuk x
plt.ylabel(data.feature_names[1]) # data untuk y
for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:, [0, 1]].values # ambil data x dan y
    hull = Ch.myConvexHull(bucket)  # bagian ini diganti dengan hasil implementasi ConvexHull Divide & Conquer
    hull = np.transpose(hull)
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    plt.plot(hull[0], hull[1], colors[i])
plt.legend()
#  menampilkan hasil convex hull
plt.show()