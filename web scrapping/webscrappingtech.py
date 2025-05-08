
from bs4 import BeautifulSoup as sop
import requests as req
import pandas as pd

# local web
# with open('index.html', 'r') as html:
#     content =  html.read()

#     # soup = sop(content, 'lxml')
#     # # print(soup.prettify()) 
#     # tags = soup.find_all('h5')
#     # # print(tags)
#     # for course in tags:
#     #     print(course.text)
#     soup = sop(content, 'lxml')
#     course = soup.find_all('div', class_='card')
#     for kursus in course:
#         # print(kursus.h5 )
#         nama_kursus = kursus.h5.text
#         harga_kursus = kursus.a.text.split()[-1]
#         # print(nama_kursus)
#         # print(harga_kursus)
#         print(f'{nama_kursus} costs {harga_kursus}')


# real web 


# html = req.get('https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=python&cboWorkExp1=-1&txtLocation=').text
# # print(html)
# soup = sop(html, 'lxml')
# job_data = [] 
# cards = soup.find('ul')
# for card in cards.find_all('li'):
#     # job_exp = card.find('div', class_='srp-exp')
    
#     # job_loc = card.find('div', class_='srp-loc')
#     # job_sal = card.find('div', class_='srp-sal')
#     # print(f"Job Experience : {job_exp.text}\nJob Location   : {job_loc.text}\nJob Salary     : {job_sal.text}\n")

#     tes = card.find('div', class_='srp-job-bx')
#     if tes :  # Cek apakah 'srp-job-bx' ditemukan
#         location = tes.find('div', class_='srp-loc')
#         experience = tes.find('div', class_='srp-exp')
#         salary = tes.find('div', class_='srp-sal')

#             # Gunakan .text.strip() jika ditemukan, jika tidak, ganti dengan "None"
#         location_text = location.text.strip() if location and location.text.strip() else "None"
#         experience_text = experience.text.strip() if experience else "None"
#         salary_text = salary.text.strip() if salary else "None"
#         # print(f"Location: {location_text}\nExperience: {experience_text}\nSalary: {salary_text}\n")
#         job_data.append([location_text, experience_text, salary_text])

#     df = pd.DataFrame(job_data, columns=['Location', 'Experience', 'Salary'])
#     df.to_csv('timesjobs_python_jobs.csv', index=False, encoding='utf-8')



url = "https://jemberkab.bps.go.id/id/statistics-table/1/MzUxIzE=/banyaknya-desa-kelurahan-dan-jatah-beras-program-raskin--kg--menurut-kecamatan-di-kabupaten-jember--2023.html"

# Mengambil halaman HTML
response = req.get(url)

# Cek apakah halaman berhasil diakses
if response.status_code == 200:
    soup = sop(response.text, "html.parser")

    # Cari elemen tabel dalam HTML
    table = soup.find("table")  # Cari elemen <table>

    if table:
        rows = table.find_all("tr")  # Ambil semua baris dalam tabel

        # Loop melalui baris untuk mengambil data
        for row in rows:
            columns = row.find_all(["td", "th"])  # Ambil semua kolom (termasuk header)
            row_data = [col.text.strip() for col in columns]  # Bersihkan teks setiap kolom
            print(" | ".join(row_data))  # Cetak data dengan format yang rapi
    else:
        print("Tabel tidak ditemukan di halaman.")
else:
    print("Gagal mengakses halaman. Status code:", response.status_code)