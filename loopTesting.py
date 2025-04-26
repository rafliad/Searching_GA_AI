import random
import math
import copy

def header(judul):
    print(f"\n======================================== {judul} ========================================")

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


# fungsi untuk membuat parent 
def RouletteWheelSelection(fitness):
    r = random.uniform(0, 1)
    index = 0
    while r > 0:
        r -= fitness[index]
        index += 1
    return index - 1


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
    
def mutasi(anak):
    pm = 0.1  # probabilitas mutasi
    
    # Iterasi untuk setiap pasangan anak
    for i in range(len(anak)):
        child1, child2 = anak[i]
        
        # Konversi tuple ke list agar bisa dimodifikasi
        child1 = list(child1)
        child2 = list(child2)
        
        # Lakukan mutasi untuk setiap bit pada child1
        for j in range(len(child1)):
            r = random.uniform(0, 1)
            if r < pm:
                child1[j] = 1 - child1[j]  # Mutasi dengan membalik bit (0→1 atau 1→0)
        
        # Lakukan mutasi untuk setiap bit pada child2
        for j in range(len(child2)):
            r = random.uniform(0, 1)
            if r < pm:
                child2[j] = 1 - child2[j]  # Mutasi dengan membalik bit (0→1 atau 1→0)
        
        # Simpan kembali hasil mutasi
        anak[i] = (child1, child2)
        
        # Cetak hasil mutasi
        print(f"Pasangan {i + 1} setelah mutasi:")
        print(f"Anak 1: {child1} dan Anak 2: {child2}")
    
    return anak 

kromosom_terbaik = []
nilai_objektif_terbaik = 0
nilai_X1_terbaik = 0
nilai_X2_terbaik = 0
generasi_terbaik = -1  

for generasi in range(10000):
    # range nilai 
    r_min = -10
    r_max = 10 
    semua_kromosom = []
    a = []
    b = []
    obj = []
    fits = []

    header("Data Awal")
    for i in range(5):
        # membuat kromosom dengan populasi 40 individu
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

    header("Pemilihan Orang Tua")
    parent = []
    
    # me looping selama populasinya masih dalam range populasi dibagi 2
    normalisasi_fitnes = fungsiNormalisasi(fits)

    # pemanggilan untuk parent baru dalam bentuk index
    parent1 = RouletteWheelSelection(normalisasi_fitnes)
    parent2 = RouletteWheelSelection(normalisasi_fitnes)

    # perulangan jika terjadi parent 1 dan 2 itu sama 
    while parent1 == parent2:
        parent1 = RouletteWheelSelection(normalisasi_fitnes)
        parent2 = RouletteWheelSelection(normalisasi_fitnes)

    # mengubah parent dari index menjadi kromosom biner
    kromosom_parent1 = semua_kromosom[parent1]
    kromosom_parent2 = semua_kromosom[parent2]
    parent.append((kromosom_parent1, kromosom_parent2))

    print(f"parent 1:{kromosom_parent1} dan parent 2: {kromosom_parent2}")

    header("Crossover")

    anak = crossover(parent)

    header("Mutasi")
    m = mutasi(anak)

    header("Pergantian Generasi")
    seluruh_populasi = []
    for child1, child2 in m:
            seluruh_populasi.append(child1)
            seluruh_populasi.append(child2)
    # Update nilai fitness populasi baru
    a = []
    b = []
    obj = []
    fits = []
            
    for individu in seluruh_populasi:
        individu_len = len(individu) // 2
        kromosom_x1 = individu[:individu_len]
        kromosom_x2 = individu[individu_len:]
                
        x1 = decodeKromosom(kromosom_x1)
        x2 = decodeKromosom(kromosom_x2)
        a.append(x1)
        b.append(x2)
                
        nilai_obj = fungsiObjektif(x1, x2)
        nilai_fitnes = fungsiFitnes(nilai_obj)
        obj.append(nilai_obj)
        fits.append(nilai_fitnes)

    fitness_normalisasi = fungsiNormalisasi(fits)

    # Temukan kromosom terbaik dari populasi akhir
    best_idx = fitness_normalisasi.index(max(fitness_normalisasi))
    best_kromosom = seluruh_populasi[best_idx]
    best_fitness = fitness_normalisasi[best_idx]
        
    # Decode nilai x1 dan x2 dari kromosom terbaik
    individu_len = len(best_kromosom) // 2
    x1 = decodeKromosom(best_kromosom[:individu_len])
    x2 = decodeKromosom(best_kromosom[individu_len:])
    nilai_objektif = fungsiObjektif(x1, x2)

    i = 1
    for individu in seluruh_populasi:
        print(f"Kromosom ke-{i}: {individu}")
        i+=1

    if nilai_objektif_terbaik < nilai_objektif and x1 > r_min and x1 < r_max and x2 > r_min and x2 < r_max:
        kromosom_terbaik = best_kromosom
        nilai_objektif_terbaik = nilai_objektif
        nilai_X1_terbaik = x1
        nilai_X2_terbaik = x2
        generasi_terbaik = generasi + 1
        
    print(f"\nIndex kromosom terbaik dari generasi ke-{generasi+1}: {best_idx + 1}")
    print(f"Kromosom terbaik dari generasi ke-{generasi+1}: {best_kromosom}")
    print(f"x1 = {x1}, x2 = {x2}")
    print(f"Nilai objektif: {nilai_objektif:.6f}")
    print(f"Fitness: {best_fitness:.6f}")

header("Hasil Akhir")
print(f"Generasi ke-{generasi_terbaik}")
print(f"kromosom terbaik: {kromosom_terbaik}")
print(f"x1 = {nilai_X1_terbaik}, x2 = {nilai_X2_terbaik}")
print(f"Nilai objektif: {nilai_objektif_terbaik:.6f}")

