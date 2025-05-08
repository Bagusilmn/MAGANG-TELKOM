from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # ✅ Import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv


website = 'https://gis.dukcapil.kemendagri.go.id/peta/'
# website = 'https://gis.dukcapil.kemendagri.go.id/arcgis/apps/experiencebuilder/experience/?id=7d1ab9b69ded40ca97e82fc9b2bdd50c'
path = 'D:\chromedriver-win64\chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()


try:
    # Temukan elemen <object>
    object_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'preview-frame'))
    )

    # Dapatkan URL dari atribut 'data'
    object_data_url = object_element.get_attribute('data')

    # Arahkan driver ke URL tersebut
    driver.get(object_data_url)

    driver.switch_to.default_content()

    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@role='checkbox' and @type='checkbox' and contains(@class, 'form-check-input')]"))
    )
    driver.execute_script("arguments[0].click();", checkbox)

    button_tutup = driver.find_element(By.XPATH, "//button[@class='jimu-btn app-root-emotion-cache-ltr-1ab90ae icon-btn btn btn-primary']")
    button_tutup.click()


    
    button_provinsi = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='jimu-btn  jimu-dropdown-button dropdown-button app-root-emotion-cache-ltr-1bxd4fj btn btn-default']"))
    )
    driver.execute_script("arguments[0].click();", button_provinsi)
    
    button_provinsiselect = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='flex-grow-1 text-truncate' and @title='JAWA TIMUR']"))
    )
    driver.execute_script("arguments[0].click();", button_provinsiselect)


    button_Kabupaten = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='page_0']/div/div/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/button"))
    )
    driver.execute_script("arguments[0].click();", button_Kabupaten)
    
    button_Kabupatenselect = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='flex-grow-1 text-truncate' and @title='KAB. JEMBER']"))
    )
    driver.execute_script("arguments[0].click();",button_Kabupatenselect)


    button_APPLY = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='jimu-btn active ml-auto app-root-emotion-cache-ltr-15rucwl btn btn-default']"))
    )
    driver.execute_script("arguments[0].click();",button_APPLY)



    button_data_kel = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@class='jimu-btn p-0 app-root-emotion-cache-ltr-5u9ltf icon-btn btn btn-tertiary btn-sm']"))
    )
    for button_data in button_data_kel:
        driver.execute_script("arguments[0].click();",button_data)

    
    # Mengambil data dari tabel
    data_list = []

    table_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    # Ambil header tabel
    headers = []
    header_elements = table_header.find_elements(By.TAG_NAME, "th")
    for header in header_elements:
        headers.append(header.text.strip())
    data_list.append(headers)

    table = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
    )
    for tables in table:
        # Extract rows
        col = []
        columns = tables.find_elements(By.TAG_NAME, "td")
        for column in columns:
            col.append(column.text.strip())
        data_list.append(col)



        # Write data to CSV
        csv_filename = "data_output.csv"
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data_list)

        print(f"✅ Data has been successfully saved to {csv_filename}")

    

    
    button_next = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@title='Next' and @aria-label='Next' and @class='page-link']"))
    )
    driver.execute_script("arguments[0].click();",button_next)



    button_data_ke2 = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@class='jimu-btn p-0 app-root-emotion-cache-ltr-5u9ltf icon-btn btn btn-tertiary btn-sm']"))
    )
    for button_data2 in button_data_ke2:
        driver.execute_script("arguments[0].click();",button_data2)

    all_data=[]
    table2 = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
    )
    data_listkedua = []
    for tables2 in table2:
        # Extract rows
        col2 = []
        columns2 = tables2.find_elements(By.TAG_NAME, "td")
        for column2 in columns2:
            col2.append(column2.text.strip())
        data_listkedua.append(col2)
    all_data.extend(data_listkedua)


            # Write data to CSV
    csv_filename = "data_output.csv"
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as file2:
        writer = csv.writer(file2)
        writer.writerows(all_data)

    print(f"✅ Data has been successfully saved to 2 {csv_filename}")





    button_next2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Page 3' and @class='page-link']"))
    )
    driver.execute_script("arguments[0].click();",button_next2)



    button_data_ke3 = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@class='jimu-btn p-0 app-root-emotion-cache-ltr-5u9ltf icon-btn btn btn-tertiary btn-sm']"))
    )
    for button_data3 in button_data_ke3:
        driver.execute_script("arguments[0].click();",button_data3)

    all_data2=[]
    table3 = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
    )
    data_listtiga = []
    for tables3 in table3:
        # Extract rows
        col3 = []
        columns3 = tables3.find_elements(By.TAG_NAME, "td")
        for column3 in columns3:
            col3.append(column3.text.strip())
        data_listtiga.append(col3)
    all_data2.extend(data_listtiga)


            # Write data to CSV
    csv_filename = "data_output.csv"
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as file3:
        writer = csv.writer(file3)
        writer.writerows(all_data2)

    print(f"✅ Data has been successfully saved to 3 {csv_filename}")



finally:
    # Tunggu input dari pengguna sebelum menutup
    input("Tekan Enter untuk keluar...")
    driver.quit()

    