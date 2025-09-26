import os
import subprocess
import random

# Keman notaları listesi
notes = [
    ('Sol3'), ('Sol#3'), ('La3'), ('La#3'), ('Si3'),
    ('Do4'), ('Do#4'), ('Re4'), ('Re#4'), ('Mi4'),
    ('Fa4'), ('Fa#4'), ('Sol4'), ('Sol#4'), ('La4'),
    ('La#4'), ('Si4'), ('Do5'), ('Do#5'), ('Re5'),
    ('Re#5'), ('Mi5'), ('Fa5'), ('Fa#5'), ('Sol5'),
    ('Sol#5'), ('La5'), ('La#5'), ('Si5'), ('Do6'),
    ('Do#6'), ('Re6'), ('Re#6'), ('Mi6'), ('Fa6'),
    ('Fa#6'), ('Sol6'), ('Sol#6'), ('La6'), ('La#6'),
    ('Si6'), ('Do7'), ('Do#7'), ('Re7'), ('Re#7'), ('Mi7')
]

# Klasör yolları
input_folder = 'keman/k4lük'  # Ses dosyalarının bulunduğu klasör
output_folder = 'akortsuzk4'  # İşlenmiş ses dosyalarının kaydedileceği klasör

# FFmpeg komutunu çalıştıracak fonksiyon
def run_ffmpeg(command):
    try:
        print(f"Komut çalıştırılıyor: {command}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"FFmpeg Çıkışı: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg komutu hata verdi: {e.stderr}")
        raise  # Hata meydana gelirse, hatayı yükselt

# Klasör kontrolü
def check_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"{folder_path} klasörü mevcut değil. Klasör oluşturuluyor...")
        os.makedirs(folder_path)
        print(f"{folder_path} klasörü başarıyla oluşturuldu.")
    else:
        print(f"{folder_path} klasörü zaten mevcut.")

# Frekans değiştirme ve dosya isimlendirme
def process_files():
    try:
        # Giriş ve çıkış klasörlerinin varlığını kontrol et
        check_folder(input_folder)
        check_folder(output_folder)

        # Klasördeki dosyaları listele
        files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
        if not files:
            print("Klasörde işlenecek .wav dosyası bulunamadı.")
            return

        for file in files:
            file_path = os.path.join(input_folder, file)

            # Rastgele frekans değişikliği
            pitch_up_change = random.randint(-10, -5)  # Tiz bozuk frekans (-5 ile -10 arasında)
            pitch_down_change = random.randint(5, 10)  # Pes bozuk frekans (+5 ile +10 arasında)

            # Orijinal dosya adı ve frekans farkı ile yeni dosya adı
            new_file_name_up = file.replace(".wav", f"_{pitch_up_change:+.2f}Hz_tiz.wav")
            new_file_name_down = file.replace(".wav", f"_{pitch_down_change:+.2f}Hz_pes.wav")

            # Yeni dosya yolunu oluştur
            output_file_path_up = os.path.join(output_folder, new_file_name_up)
            output_file_path_down = os.path.join(output_folder, new_file_name_down)

            # FFmpeg komutunu oluştur (artış)
            command_up = [
                'ffmpeg',
                '-i', file_path,  # Giriş dosyası
                '-af', f'asetrate=44100*(1 + {pitch_up_change / 44100})',  # Artış işlemi
                output_file_path_up  # Çıkış dosyası
            ]

            # FFmpeg komutunu oluştur (azalış)
            command_down = [
                'ffmpeg',
                '-i', file_path,  # Giriş dosyası
                '-af', f'asetrate=44100*(1 - {abs(pitch_down_change) / 44100})',  # Azalış işlemi
                output_file_path_down  # Çıkış dosyası
            ]

            # Frekans değişikliğini uygula ve dosyayı kaydet (tiz)
            run_ffmpeg(command_up)

            # Frekans değişikliğini uygula ve dosyayı kaydet (pes)
            run_ffmpeg(command_down)

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Ana işlem
if __name__ == "__main__":
    try:
        print("Keman ses dosyaları işleniyor...")
        process_files()
        print("İşlem tamamlandı.")
    except Exception as e:
        print(f"Program sırasında hata oluştu: {e}")
