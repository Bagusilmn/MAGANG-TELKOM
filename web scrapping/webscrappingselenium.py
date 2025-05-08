from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # ✅ Import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


website = 'https://jemberkab.bps.go.id/id/statistics-table/1/MzUxIzE=/banyaknya-desa-kelurahan-dan-jatah-beras-program-raskin--kg--menurut-kecamatan-di-kabupaten-jember--2023.html'
path = 'D:\chromedriver-win64\chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)

button_path = driver.find_element(By.XPATH, "//button[@class='rounded-lg bg-main-light px-6 py-2 transition-colors hover:bg-main-light-hover text-white font-semibold']")
button_path.click()

# tables = driver.find_elements(By.TAG_NAME, 'tr')
# for table in tables:
#     print(table.text)

data_list = []
# try:
#     table = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "table"))
#     )

#     # Ambil semua baris dalam tabel
#     rows = table.find_elements(By.TAG_NAME, "tr")
#     for row in rows:
#         columns = row.find_elements(By.TAG_NAME, "td")  # Ambil semua kolom dalam baris
#         row_text = [col.text for col in columns]  # Ambil teks dari setiap kolom
#         print(" | ".join(row_text))  # Cetak hasil dengan format yang lebih rapi
# except:
#     print("Elemen tabel tidak ditemukan atau masih loading.")

try:
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )

    # Ambil semua baris dalam tabel
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")  # Ambil semua kolom dalam baris
        row_text = [col.text for col in columns]  # Simpan teks dalam list
        if row_text:  # Hanya simpan jika tidak kosong
            data_list.append(row_text)
except:
    print("Elemen tabel tidak ditemukan atau masih loading.")

csv_filename = "csv1.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # # Tambahkan header jika ada
    # header = ["Kecamatan", "Banyaknya Desa/Kelurahan", "Jatah Beras (Kg)"]  # Sesuaikan dengan data tabel
    # writer.writerow(header)
    
    # Tambahkan data
    writer.writerows(data_list)

print(f"✅ Data berhasil disimpan ke {csv_filename}")

input("Tekan Enter untuk keluar...")
driver.quit()

