from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # ✅ Import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


website = 'https://www.telkomsel.com/landingpage/regular/nasional/paket'
path = 'D:\chromedriver-win64\chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()

button_pilih_lokasi = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='w-100 quickWin_buttonPrimaryLp__CPw0q']"))
    )
driver.execute_script("arguments[0].click();", button_pilih_lokasi)

input("Tekan Enter untuk keluar...")
driver.quit()