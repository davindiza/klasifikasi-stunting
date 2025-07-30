# import pandas as pd


# def hitung_zscore(nilai, median, sd_minus1, sd_plus1):
#     """
#     Menghitung Z-score berdasarkan nilai, median, dan SD.
#     WHO menggunakan rumus yang berbeda untuk nilai < median dan >= median.
#     """
#     if nilai >= median:
#         sd = sd_plus1 - median
#         z = (nilai - median) / sd
#     else:
#         sd = median - sd_minus1
#         z = (nilai - median) / sd
#     return round(z, 2)

def hitung_zs_tbu(tinggi, umur_bulan, jenis_kelamin, data_who):
    # Ambil data WHO sesuai umur dan jenis kelamin
    data = data_who[(data_who['Umur'] == umur_bulan) & (data_who['JK'] == jenis_kelamin)]
    # return hitung_zscore(tinggi, data['Median'].values[0], data['SD-1'].values[0], data['SD+1'].values[0])

file_path = 'E:\web-puskesmas\app\data\bbu_who.xlsx'  # Ganti sesuai lokasi file kamu
sheet_name = 'tbu'              # Ganti sesuai nama sheet
data_who = pandas.read_excel(file_path, sheet_name=sheet_name)

# Contoh penggunaan
tinggi = 78.0

umur_bulan = 24
jenis_kelamin = 'L'  # 'L' atau 'P'

zscore = hitung_zs_tbu(tinggi, umur_bulan, jenis_kelamin, data_who)
print("Z-score TB/U:", zscore)