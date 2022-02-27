import numpy as np
import math

def myConvexHull(bucket):
    # Pemrosessan ConvexHull atas
    arrup =np.ndarray([0,2])
    # Pemrosessan ConvexHull bawah
    arrdown =np.ndarray([0,2])

    # menampung ConvexHull gabungan atas dan bawah
    arr =np.ndarray([0,2])
    
    # mencari titiks ekstrem P1, Pn
    maks,minn,raw_bucket = find_extreme(bucket)
    #assign P1 untuk pemrosesan atas
    arrup= np.append(arrup, [maks], axis=0)

    #assign Pn untuk pemrosesan bawah
    arrdown= np.append(arrdown,[minn], axis=0)
   
    #membagi titik menjadi bagian atas dan bawah dari garis P1Pn
    raw_bucket_up,raw_bucket_down = create_bucket_updown(raw_bucket,maks,minn) 

    # memproses convex hull atas
    arrup = convex_hull_up(raw_bucket_up,maks,minn,arrup)

    # memproses convex hull bawah
    arrdown = convex_hull_down(raw_bucket_down,maks,minn,arrdown)

    # flip for plotting
    arrup = np.flip(arrup,0)
    # sort for plotting
    arrup =quickSort(arrup,0,len(arrup)-1)

    # sort for plotting
    arrdown = quickSort(arrdown,0,len(arrdown)-1)
    # flip for plotting
    arrdown = np.flip(arrdown,0)

    # menggabungkan array convex hull atas dan bawah
    # tambahkan min diawal untuk keperluan plot
    arr = np.append(arr,[minn],axis =0)
    arr = np.append(arr,arrup,axis=0)
    arr = np.append(arr,arrdown,axis=0)

    return arr

def find_extreme(bucket):
    # mencari titik ekstreme yaitu P1 Pn

    #Pn
    maks = max(bucket[:, 0])
    indeksmaks = np.where(bucket[:, 0] == maks)
    maksordinat=bucket[indeksmaks, 1];
    i_maks = indeksmaks[0][0]

    # kasus jika terdapat nilai absis yang sama maka ditinjau nilai ordinatnya
    for i in range(0,len(bucket)-1):
        if(maks == bucket[i, 0]):
            if (maksordinat[0,0] <= bucket[i, 1]):
                i_maks = i
    bucketmax=bucket[i_maks]

    # menghapus nilai ekstreme dari array
    bucket = np.delete(bucket,[i_maks],axis =0)

    #P1
    minn = min(bucket[:, 0])
    indeksmin = np.where(bucket[:, 0] == minn)
    minordinat=bucket[indeksmin, 1];
    i_min = indeksmin[0][0]

    for i in range(0,len(bucket)-1):
        if(minn == bucket[i, 0]):
            if(minordinat[0,0]>=bucket[i, 1]):
                i_min = i
    bucketmin =bucket[i_min]

    # menghapus nilai ekstreme dari array
    bucket = np.delete(bucket,[i_min],axis =0)
    return bucketmax, bucketmin ,bucket

def detpoint(x1,y1,x2,y2,x3,y3):
    # mengirimkan nilai yang menandakan titik berada di bawah atau atas garis
    # gradien
    m = (y3-y2)/(x3-x2)

    # offset
    c = y3 - m*x3

    # titik yang akan dibandingkan
    dis = y1-m*x1
    if(dis>c):
        return 1 # berada di atas garis
    elif(dis<c):
        return -1 # berada di bawah garis
    else:
        return 0 # berada di garis

def distance(x1,y1,x2,y2,x3,y3):
    # menghitung jarak titik ke garis
    return abs((x2-x1)*(y1-y3)-(x1-x3)*(y2-y1))/math.sqrt((x2-x1)**2+(y2-y1)**2)

def create_bucket_updown(raw_bucket,P1,P2):
    # membagi titik menjadi bagian atas dan bawah atau kiri dan kanan dari garis P1Pn
    raw_bucket_up=np.ndarray([0,2])
    raw_bucket_down=np.ndarray([0,2])
    for i in range(len(raw_bucket)):
        if(P2[0]==P1[0]):
            break
        determinant = detpoint(raw_bucket[i,0],raw_bucket[i,1],P1[0],P1[1],P2[0],P2[1])
        if(determinant>0):
            raw_bucket_up=np.append(raw_bucket_up,[raw_bucket[i]],axis =0)
        elif(determinant<0):
            raw_bucket_down=np.append(raw_bucket_down,[raw_bucket[i]],axis =0)
        else:
            pass
    return raw_bucket_up,raw_bucket_down


def convex_hull_up(raw_bucket_up,P1,P2, arr):
    # convex hull untuk bagian atas
    if(len(raw_bucket_up)==0):
        # array kosong
        return arr
    elif (len(raw_bucket_up) == 1):
        # array satu elemen
        return np.append(arr,[raw_bucket_up[0]], axis=0)
    else:
        # set maks distance ke elemen ke-1
        maks_distance= distance(P1[0],P1[1],P2[0],P2[1],raw_bucket_up[0,0],raw_bucket_up[0,1])
        maks_indeks =0
        for i in range(len(raw_bucket_up)):
            distancepoint = distance(P1[0],P1[1],P2[0],P2[1],raw_bucket_up[i,0],raw_bucket_up[i,1])
            
            if (maks_distance*100 <= distancepoint*100):
                maks_distance=distancepoint
                maks_indeks = i
   
        maks_value =raw_bucket_up[maks_indeks]

        # mencari array atas dari garis P1Pn yang baru
        raw_next1,dummy = create_bucket_updown(raw_bucket_up,P1,maks_value)
        raw_next2,dummy = create_bucket_updown(raw_bucket_up,P2,maks_value)

        # rekursif array selanjutnya sebelah kanan
        arr = convex_hull_up(raw_next1,P1,maks_value,arr)

        # assign ke array dan delete pada raw_bucket
        
        arr = np.append(arr,[maks_value], axis=0)
        raw_bucket_up = np.delete(raw_bucket_up,maks_indeks,axis=0)
        
        # rekursif array selanjutnya sebelah kiri
        arr = convex_hull_up(raw_next2,P2,maks_value,arr)
        return arr

def convex_hull_down(raw_bucket_down,P1,P2, arr):
    # convex hull untuk bagian bawah
    if(len(raw_bucket_down)==0):
        return arr
    elif (len(raw_bucket_down) == 1):
        return np.append(arr,[raw_bucket_down[0]], axis=0)
    else:
        # set maks distance ke elemen ke-1
        maks_distance= distance(P1[0],P1[1],P2[0],P2[1],raw_bucket_down[0,0],raw_bucket_down[0,1])
        maks_indeks =0
        for i in range(len(raw_bucket_down)):
            distancepoint = distance(P1[0],P1[1],P2[0],P2[1],raw_bucket_down[i,0],raw_bucket_down[i,1])

            if (maks_distance*10000 <= distancepoint*10000):
                maks_distance=distancepoint
                maks_indeks = i

        maks_value =raw_bucket_down[maks_indeks]

        # mencari array bawah dari garis P1Pn yang baru
        dummy,raw_next1 = create_bucket_updown(raw_bucket_down,P1,maks_value)
        dummy,raw_next2 = create_bucket_updown(raw_bucket_down,P2,maks_value)

        # rekursif array selanjutnya sebelah kiri
        arr = convex_hull_down(raw_next2,P2,maks_value,arr)

        #assign ke array dan delete pada raw_bucket
        arr = np.append(arr,[maks_value], axis=0)
        raw_bucket_down = np.delete(raw_bucket_down,maks_indeks,axis=0)

        # rekursif array selanjutnya sebelah kanan
        arr = convex_hull_down(raw_next1,P1,maks_value,arr)
        
        return arr



def partition(array, low, high):
    # choose the rightmost element as pivot
    pivot = array[high,0]

    # pointer for greater element
    i = low - 1

    # bandingkan nilai elemen dengan pivot
    for j in range(low, high):
        if array[j,0] <= pivot:
            i = i + 1
            temp1 = array[i,0]
            temp2 = array[i,1]
            array[i]=array[j]
            array[j,0]=temp1
            array[j,1]=temp2

    temp1 = array[i+1,0]
    temp2 = array[i+1,1]
    array[i+1]=array[high]
    array[high,0]=temp1
    array[high,1]=temp2
    # return posisi partisi selesai dilakukan
    return i + 1

# function to perform quicksort
def quickSort(array, low, high):
    if low < high:
        # mencari pivot
        pi = partition(array, low, high)

        # rekursif sebelah kiri pivot
        quickSort(array, low, pi - 1)
        # recursive sebelah kanan pivot
        quickSort(array, pi + 1, high)

    return array