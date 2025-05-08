from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # ✅ Import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


website = 'https://portal-data.jemberkab.go.id/portal-9b6210921eaa1036dbd5acb87f049437.html#'
path = 'D:\chromedriver-win64\chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()

button_provinsi = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='leaflet-pane leaflet-overlay-pane']"))
    )
# button_path = button_provinsi.find_element(By.XPATH, "//*[@id='map']/div[1]/div[2]/svg]")
# button_path.click()

    

input("Tekan Enter untuk keluar...")
driver.quit()


