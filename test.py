from utils.parse_nik import parse_nik
from utils.normalize_rule import normalisasi
from engine import nb_engine, c45_engine

# nik_number = "3302104104750003"

# nik_info = parse_nik(nik_number)
# if nik_info:
#     print("Kode Provinsi:", nik_info["province_id"])
#     print("Kode Kabupaten:", nik_info["regency_id"])
#     print("Kode Kecamatan:", nik_info["district_id"])
#     print("Tanggal Lahir:", nik_info["birthdate"])
# else:
#     print("Format NIK tidak valid.")
    
# nb_engine.savemodel()
# c45_engine.savemodel()
val=[11.60,84.00,30.00] #negatif
# val=[16.30,88.30,30.20] #negatif
# val=[12.70,79.20,25.50] #positif
val2 = normalisasi(val)
print(val)
print("nb", nb_engine.cekkemungkinan(val))
# print("c45", c45_engine.cekkemungkinan(val2))
# nb_engine.testtrain()
# c45_engine.testtrain()
