import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_and_download_sounds(url, output_folder="downloads"):
    # Selenium WebDriver'i başlat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # Belirtilen URL'yi aç
        driver.get(url)

        # Sayfanın yüklenmesini bekle
        time.sleep(5)

        # Sayfadaki tüm ses çalar öğelerini bul
        players = driver.find_elements(By.CLASS_NAME, 'bw-player')

        # Eğer ses çalar öğesi bulunamazsa
        if not players:
            print("Sayfada ses dosyası bulunamadı.")
            return

        # Çıkış klasörünü oluştur
        os.makedirs(output_folder, exist_ok=True)

        # Her bir ses çalar öğesini işleyin
        for player in players:
            # MP3 ve OGG bağlantılarını al
            mp3_url = player.get_attribute('data-mp3')
            ogg_url = player.get_attribute('data-ogg')

            # Eğer bağlantılar yoksa, sonraki öğeye geç
            if not mp3_url and not ogg_url:
                continue

            # MP3 dosyasını indirip indirilmeyeceğini kontrol et
            download_url = mp3_url if mp3_url else ogg_url
            file_name = download_url.split("/")[-1]
            file_path = os.path.join(output_folder, file_name)

            # Dosyayı indir
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                print(f"Ses dosyası başarıyla indirildi: {file_path}")
            else:
                print(f"Ses dosyası indirilemedi. HTTP Durum Kodu: {response.status_code}")
    finally:
        # WebDriver'i kapat
        driver.quit()

# Kullanım
scrape_and_download_sounds("https://freesound.org/people/Teddy_Frost/sounds/334541/")
