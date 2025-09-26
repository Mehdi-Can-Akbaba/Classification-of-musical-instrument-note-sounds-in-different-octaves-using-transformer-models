import os
import subprocess

# Notaların frekansları (örnek olarak bazı frekanslar verilmiştir)
notes_with_freq = {
    'Mi2': 82.41, 'Fa2': 87.31, 'Fa#2': 92.50, 'Sol2': 98.00, 'Sol#2': 103.83,
    'La2': 110.00, 'La#2': 116.54, 'Si2': 123.47, 'Do3': 130.81, 'Do#3': 138.59,
    'Re3': 146.83, 'Re#3': 155.56, 'Mi3': 164.81, 'Fa3': 174.61, 'Fa#3': 185.00,
    'Sol3': 196.00, 'Sol#3': 207.65, 'La3': 220.00, 'La#3': 233.08, 'Si3': 246.94,
    'Do4': 261.63, 'Do#4': 277.18, 'Re4': 293.66, 'Re#4': 311.13, 'Mi4': 329.63,  # Mi4 frekansı
    'Fa4': 349.23,  # Fa4 frekansı
    'Fa#4': 369.99, 'Sol4': 392.00, 'Sol#4': 415.30, 'La4': 440.00, 'La#4': 466.16,
    'Si4': 493.88, 'Do5': 523.25, 'Do#5': 554.37, 'Re5': 587.33, 'Re#5': 622.25,
    'Mi5': 659.25, 'Fa5': 698.46, 'Fa#5': 739.99
}


# Bozuk frekans oluşturma fonksiyonu
def create_wrong_frequency(note1, note2):
    """ İki nota arasındaki farkı hesapla ve bozuk bir frekans oluştur. """
    f1 = notes_with_freq[note1]
    f2 = notes_with_freq[note2]

    # İki nota arasındaki farkı hesapla
    freq_diff = abs(f1 - f2)

    # Ortalama frekans
    avg_freq = (f1 + f2) / 2

    # Frekansın bozulmuş hali: Ortalamadan dışarıda, ama yine de iki nota arasında.
    # Farkın bir kısmını, ortalamanın dışına ekleyerek bozuk frekans oluşturulacak.
    wrong_frequency = avg_freq + (freq_diff * 0.25)  # Ortalamanın dışına, küçük bir fark ekleyerek
    return wrong_frequency


# Klasör yolları
input_folder = 'elektro gitar/eg4lük'  # Ses dosyalarının bulunduğu klasör
output_folder = 'testakorsuzeg4lük'  # İşlenmiş ses dosyalarının kaydedileceği klasör


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

            # Dosya adıyla nota eşlemesi yap (örnek: Mi2, Fa#3, vb.)
            notes = file.split('_')  # Dosya adından notaları ayırıyoruz
            if len(notes) < 2:
                continue  # Dosya adı geçerli formatta değilse atla

            note1 = notes[0]  # İlk nota
            note2 = notes[1]  # İkinci nota

            # Eğer notaların her ikisi de geçerli ise bozuk frekans oluştur
            if note1 in notes_with_freq and note2 in notes_with_freq:
                wrong_frequency = create_wrong_frequency(note1, note2)

                # Orijinal dosya adı ve frekans farkı ile yeni dosya adı
                new_file_name = file.replace(".wav", f"_wrong_{int(wrong_frequency)}Hz.wav")

                # Yeni dosya yolunu oluştur
                output_file_path = os.path.join(output_folder, new_file_name)

                # FFmpeg komutunu oluştur (frekans değişikliği)
                command = [
                    'ffmpeg',
                    '-i', file_path,  # Giriş dosyası
                    '-af', f'asetrate=44100*(1 + {wrong_frequency / 44100})',  # Bozuk frekansı uygula
                    output_file_path  # Çıkış dosyası
                ]

                # Frekans değişikliğini uygula ve dosyayı kaydet
                run_ffmpeg(command)
            else:
                print(f"Geçersiz dosya adı veya notalar: {file}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


# Ana işlem
if __name__ == "__main__":
    try:
        print("Ses dosyaları işleniyor...")
        process_files()
        print("İşlem tamamlandı.")
    except Exception as e:
        print(f"Program sırasında hata oluştu: {e}")
