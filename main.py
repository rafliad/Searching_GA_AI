import random
import math
import copy

# range nilai 
r_min = -10
r_max = 10 

# membuat kromosom random
def buatKromosom(kromosom):
    return [random.randint(0,1) for _ in range(kromosom)]

# menghitung individu dari biner menjadi bilangan real
def decodeKromosom(byte):
    n = len(byte)
    kromosom = 0

    for i in range(n):
        kromosom += byte[i] * (2 ** (n - i - 1))
    
    return kromosom

# menghitung fungsi objektif 
def fungsiObjektif(x1, x2):
    return abs(-(math.sin(x1) * 
               math.cos(x2) * 
               math.tan(x1 + x2) + 
               3 * (math.exp(1 - math.sqrt(x1**2))) / 4))

# menghitung fungsi fitnes
def fungsiFitnes(objektif):
    return 1 / ((objektif) + 0.1)

# menghitung nilai normalisasi dari fungsi fitnes
def fungsiNormalisasi(fitness):
    total = sum(fitness)
    return [f / total for f in fitness]

semua_kromosom = []
a = []
b = []
obj = []
fits = []
populasi = 20

print("=================data awal=================")
# membuat kromosom dengan populasi 40 individu
for i in range(populasi):
    panjang_kromosom = 10
    # membuat kromosom random dengan panjang 10 bit
    hasil_kromosom = buatKromosom(panjang_kromosom)
    semua_kromosom.append(hasil_kromosom)

    # membagi kromosom menjadi x1 dan x2
    individu = len(hasil_kromosom) // 2  
    kromosom_x1 = hasil_kromosom[:individu]  
    kromosom_x2 = hasil_kromosom[individu:] 

    # mengubah setiap individu menjadi nilai real
    x1 = decodeKromosom(kromosom_x1)
    x2 = decodeKromosom(kromosom_x2)
    a.append(x1)
    b.append(x2)

    # menghitung fungsi objektif dan fitness
    nilai_obj = fungsiObjektif(x1, x2)
    nilai_fitnes = fungsiFitnes(nilai_obj)
    obj.append(nilai_obj)
    fits.append(nilai_fitnes)

normalisasi = fungsiNormalisasi(fits)
cumulative = 0.0
cumfit = []

# membuat nilai cumulative sesuai dengan nilai fitnes yang sudah di nomalisasikan
for c in normalisasi:
    cumulative += c
    cumfit.append(round(cumulative, 3))

interval = []
offset = 0.001

# membuat interval dari nilai cumulative
for i, value in enumerate(cumfit):
    if i == 0:
        awal = 0.0
    else:
        awal = cumfit[i - 1] + offset

    akhir = value
    interval.append((awal, akhir))
    print(f"no. kromosom: {i + 1} | a: {a[i]} | b: {b[i]} | kromosom: {semua_kromosom[i]} | Fungsi Objektif: {obj[i]} | Fungsi Fitnes: {fits[i]} | cumulative: {cumfit[i]} | interval: {interval[i]}")

print(" ")
print("===================pemilihan orang tua===================")
# fungsi untuk membuat parent 
def RouletteWheelSelection(fitness):
    r = random.uniform(0, 1)
    index = 0
    while r > 0:
        r -= fitness[index]
        index += 1
    return index - 1

parent = []

# me looping selama populasinya masih dalam range populasi dibagi 2
for _ in range(populasi//2):
    normalisasi_fitnes = fungsiNormalisasi(fits)

    # pemanggilan untuk parent baru dalam bentuk index
    parent1 = RouletteWheelSelection(normalisasi_fitnes)
    parent2 = RouletteWheelSelection(normalisasi_fitnes)

    # perulangan jika terjadi parent 1 dan 2 itu sama 
    while parent1 == parent2:
        parent2 = RouletteWheelSelection(normalisasi_fitnes)

    # mengubah parent dari index menjadi kromosom biner
    kromosom_parent1 = semua_kromosom[parent1]
    kromosom_parent2 = semua_kromosom[parent2]
    parent.append((kromosom_parent1, kromosom_parent2))

    print(f"parent 1:{kromosom_parent1} dan parent 2: {kromosom_parent2}")

print(" ")
print("===================Crossover===================")
# fungsi untuk menghasilkan kromosom baru dengan cara crossover
def crossover(parent):
    pc = 0.8
    child = []
    for (parent1, parent2) in parent:
        r = random.uniform(0, 1)
        if r < pc:
            # merandom nilai titik potong
            tipot = random.randint(1, 9)
            child1 = parent1[:tipot] + parent2[tipot:]
            child2 = parent2[:tipot] + parent1[tipot:]
        else:
            child1 = parent1
            child2 = parent2
        print(f"child 1:{child1} dan child 2: {child2}")
        child.append((child1, child2))
    return child
    
anak = crossover(parent)

print(" ")
print("==========mutasi==========")
def mutasi(anak):
    pm = 0.1
    total_kromosom = len(anak)
    panjang_kromosom = len(anak[0][0])
    jumlah_bit = total_kromosom * 2 * panjang_kromosom
    jumlah_mutasi = int(jumlah_bit * pm) 

    for _ in range(jumlah_mutasi):
        pasangan_index = random.randint(0, total_kromosom - 1)
        r_kromosom = random.randint(0, 1)
        r_bit = random.randint(0, panjang_kromosom - 1)

        # Ambil pasangan anak
        child1, child2 = anak[pasangan_index]

        # Ubah ke list supaya bisa dimutasi
        child1 = list(child1)
        child2 = list(child2)

        # Mutasi bit pada child1 atau child2
        if r_kromosom == 0:
            child1[r_bit] = 1 - child1[r_bit]  # Balikkan bit
        else:
            child2[r_bit] = 1 - child2[r_bit]  # Balikkan bit

        # Simpan kembali hasil mutasi ke pasangan anak
        anak[pasangan_index] = (child1, child2)

    for i, (child1, child2) in enumerate(anak):
        print(f"Pasangan {i + 1} setelah mutasi:")
        print(f"Anak 1: {child1} dan Anak 2: {child2}")
    return anak

m = mutasi(anak)