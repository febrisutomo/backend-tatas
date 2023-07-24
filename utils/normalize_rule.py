def normalisasi(val):
    hasil=[0,0,0]
    if val[0]<12:       #hb
        hasil[0]=1
    if val[1]<80:       #mcv
        hasil[1]=1
    if val[2]<27:       #mch
        hasil[2]=1
    return hasil
