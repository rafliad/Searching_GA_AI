import random
import math

def header(judul):
    print(f"\n======================================== {judul} ========================================")

# membuat kromosom random
def buatKromosom(kromosom):
    return [random.randint(0,1) for _ in range(kromosom)]

# menghitung individu dari biner menjadi bilangan real
def decodeKromosom(byte):
    n = len(byte)
    g = 0
    penyebut = 0 

    for i in range(n):
        g += byte[i] * (2 ** (-(i + 1)))
        penyebut += 2 ** (-(i + 1))
    
    return r_min + (((r_max - r_min) / penyebut) * g)

# menghitung fungsi objektif 
def fungsiObjektif(x1, x2):
    try: 
        nilai = math.sin(x1) * math.cos(x2) * math.tanh(x1 + x2)
        nilai2 = (3/4) * math.exp(1 - math.sqrt(x1**2))
        return (-(nilai + nilai2))
    except:
        return float('inf')

# menghitung fungsi fitnes
def fungsiFitnes(objektif):
    return 1 / ((objektif) + 0.1)

# fungsi untuk membuat parent 
def tournament_selection(populasi, fitness, tournament_size):
    best_index = None
    best_fitness = float('-inf')

    for _ in range(tournament_size):
        idx = random.randint(0, len(populasi) - 1)
        if best_index is None or fitness[idx] >= best_fitness:
            best_index = idx
            best_fitness = fitness[idx]

    return best_index

# fungsi untuk menghasilkan kromosom baru dengan cara crossover
def crossover(parent):
    pc = 0.7
    child = []
    for (parent1, parent2) in parent:
        r = random.uniform(0, 1)
        if r <= pc:
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
    
# def mutasi(anak):
#     pm = 0.1  # probabilitas mutasi
#     bits_to_mutate = round(pm * 32)  # jumlah bit yang akan dimutasi
    
#     # Iterasi untuk setiap pasangan anak
#     for child1, child2 in anak:
        
#         # Konversi tuple ke list agar bisa dimodifikasi
#         child1 = list(child1)
#         child2 = list(child2)
        
#         # Gabungkan kedua kromosom untuk kemudahan memilih bit secara acak
#         all_bits = [(0, j) for j in range(len(child1))] + [(1, j) for j in range(len(child2))]
        
#         # Pilih bits_to_mutate bit secara acak untuk dimutasi
#         mutation_indices = random.sample(all_bits, bits_to_mutate)
        
#         # Lakukan mutasi pada bit yang terpilih
#         for chromosome_idx, bit_idx in mutation_indices:
#             if chromosome_idx == 0:
#                 child1[bit_idx] = 1 - child1[bit_idx]  # Mutasi bit pada child1
#             else:
#                 child2[bit_idx] = 1 - child2[bit_idx]  # Mutasi bit pada child2
        
#         # Simpan kembali hasil mutasi
#         anak[0] = (tuple(child1), tuple(child2))
        
#         # Cetak hasil mutasi
#         print(f"Anak 1: {child1} dan Anak 2: {child2}")
    
#     return anak

def mutasi(anak):
    pm = 0.1  # probabilitas mutasi untuk setiap bit
    
    # Iterasi untuk setiap pasangan anak
    for i in range(len(anak)):
        child1, child2 = anak[i]
        
        # Konversi tuple ke list agar bisa dimodifikasi
        child1 = list(child1)
        child2 = list(child2)
        
        # Lakukan mutasi untuk setiap bit pada child1
        for j in range(len(child1)):
            if random.random() < pm:  # Jika nilai random < pm, lakukan mutasi
                child1[j] = 1 - child1[j]  # Mutasi bit pada child1
        
        # Lakukan mutasi untuk setiap bit pada child2
        for j in range(len(child2)):
            if random.random() < pm:  # Jika nilai random < pm, lakukan mutasi
                child2[j] = 1 - child2[j]  # Mutasi bit pada child2
        
        # Simpan kembali hasil mutasi
        anak[i] = (tuple(child1), tuple(child2))
        
        # Cetak hasil mutasi
        print(f"Anak 1: {child1} dan Anak 2: {child2}")
    
    return anak

kromosom_terbaik = []
nilai_objektif_terbaik = 0
nilai_fitnes_terbaik = 0
nilai_X1_terbaik = 0
nilai_X2_terbaik = 0
generasi_terbaik = -1  

for generasi in range(500):
    # range nilai 
    r_min = -2
    r_max = 3 
    populasi = []
    a = []
    b = []
    obj = []
    fits = []

    header("Data Awal")
    for i in range(20):
        # membuat kromosom dengan populasi 40 individu
        bit = 16
        # membuat kromosom random dengan panjang 10 bit
        kromosom = buatKromosom(bit)
        populasi.append(kromosom)

        # membagi kromosom menjadi x1 dan x2
        individu = len(kromosom) // 2  
        kromosom_x1 = kromosom[:individu]  
        kromosom_x2 = kromosom[individu:] 

        # mengubah setiap individu menjadi nilai real
        x1 = decodeKromosom(kromosom_x1)
        x2 = decodeKromosom(kromosom_x2)
        a.append(x1)
        b.append(x2)

        # menghitung fungsi objektif dan fitness
        nilai_obj = fungsiObjektif(x1, x2)
        obj.append(nilai_obj)

        nilai_fitnes = fungsiFitnes(nilai_obj)
        fits.append(nilai_fitnes)
        print(f"kromosom ke-{i+1} memiliki kromosom {kromosom} nilai x1 = {round(x1, 4)} dan x2 = {round(x2, 4)} dengan nilai objektif {round(nilai_obj, 4)} dan fitness {round(nilai_fitnes, 4)}")

    header("Pemilihan Orang Tua")
    parent = []

    # pemanggilan untuk parent baru dalam bentuk index
    parent1_idx = tournament_selection(populasi, fits, 3)
    parent2_idx = tournament_selection(populasi, fits, 3)
    while parent1_idx == parent2_idx:
        parent1_idx = tournament_selection(populasi, fits, 3)
        parent2_idx = tournament_selection(populasi, fits, 3)

    kromosom_parent1 = populasi[parent1_idx]
    kromosom_parent2 = populasi[parent2_idx]

    parent.append((kromosom_parent1, kromosom_parent2))
         
    # Decode nilai x1 dan x2 dari kromosom terbaik
    individu_len = len(kromosom_parent1) // 2
    individu_len2 = len(kromosom_parent2) // 2
    x1 = decodeKromosom(kromosom_parent1[:individu_len])
    x2 = decodeKromosom(kromosom_parent1[individu_len:])
    x1_2 = decodeKromosom(kromosom_parent2[:individu_len2])
    x2_2 = decodeKromosom(kromosom_parent2[individu_len2:])
    nilai_objektif = fungsiObjektif(x1, x2)
    nilai_objektif2 = fungsiObjektif(x1_2, x2_2)

    print(f"parent 1:{kromosom_parent1} dan parent 2: {kromosom_parent2}")
    print(f"nilai 1 {nilai_objektif}")
    print(f"nilai 2 {nilai_objektif2}")

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

    # Temukan kromosom terbaik dari populasi akhir
    best_idx = fits.index(max(fits))
    best_kromosom = seluruh_populasi[best_idx]
    best_fitness = fits[best_idx]
        
    # Decode nilai x1 dan x2 dari kromosom terbaik
    individu_len = len(best_kromosom) // 2
    x1 = decodeKromosom(best_kromosom[:individu_len])
    x2 = decodeKromosom(best_kromosom[individu_len:])
    nilai_objektif = fungsiObjektif(x1, x2)
    nilai_fts = fungsiFitnes(nilai_objektif)

    i = 1
    for individu in seluruh_populasi:
        print(f"Kromosom ke-{i}: {individu}")
        i+=1

    if nilai_objektif_terbaik > nilai_objektif:
        kromosom_terbaik = best_kromosom
        nilai_objektif_terbaik = nilai_objektif
        nilai_fitnes_terbaik = nilai_fts
        nilai_X1_terbaik = x1
        nilai_X2_terbaik = x2
        generasi_terbaik = generasi + 1
        
    print(f"\nIndex kromosom terbaik dari generasi ke-{generasi+1}: {best_idx + 1}")
    print(f"Kromosom terbaik dari generasi ke-{generasi+1}: {best_kromosom}")
    print(f"x1 = {round(x1, 4)}, x2 = {round(x2, 4)}")
    print(f"Nilai objektif: {round(nilai_objektif, 4)}")
    print(f"Fitness: {round(best_fitness, 4)}")

header("Hasil Akhir")
print(f"Generasi ke-{generasi_terbaik}")
print(f"kromosom terbaik: {kromosom_terbaik}")
print(f"x1 = {round(nilai_X1_terbaik, 4)}, x2 = {round(nilai_X2_terbaik, 4)}")
print(f"Nilai objektif: {round(nilai_objektif_terbaik, 4)}")
print(f"Nilai fitness: {round(nilai_fitnes_terbaik, 4)}")