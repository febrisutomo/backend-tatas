import datetime

def parse_nik(nik):
    if len(nik) == 16:
        province_id = nik[:2].zfill(2)
        regency_id = nik[:4].zfill(4)
        district_id = nik[:6].zfill(6)
        birth_date = int(nik[6:8])
        birth_month = int(nik[8:10])
        birth_year = int(nik[10:12])
        
        # Cek apakah tahun lahir melebihi tahun sekarang
        current_year = datetime.datetime.now().year % 100
        birth_year_full = 1900 + birth_year if birth_year > current_year else 2000 + birth_year
        
        # Periksa apakah NIK milik perempuan
        if birth_date > 40:
            birth_date -= 40


        birthdate_str = f"{birth_year_full:04d}-{birth_month:02d}-{birth_date:02d}"

        nik_info = {
            "province_id": province_id,
            "regency_id": regency_id,
            "district_id": district_id,
            "birthdate": birthdate_str
        }

        return nik_info
    else:
        return "Format NIK tidak valid."



  

