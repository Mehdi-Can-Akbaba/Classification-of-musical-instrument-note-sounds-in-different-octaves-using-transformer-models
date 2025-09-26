import os
from pydub import AudioSegment

# Sabit frekans kayması değeri
TUNING_SHIFT = 1.1  # Sesin frekansını %10 artır


# Ses dosyalarını işleme fonksiyonu
def process_files(input_folder, output_folder, tuning_shift):
    # Klasörlerin var olup olmadığını kontrol et
    if not os.path.exists(input_folder):
        print(f"{input_folder} klasörü bulunamadı.")
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"{output_folder} klasörü oluşturuluyor.")

    print("Ses dosyaları işleniyor...")

    # Girdi klasöründeki dosyaları oku
    files = os.listdir(input_folder)
    note_files = [f for f in files if f.endswith(".wav")]

    print(f"{input_folder} klasöründe {len(note_files)} adet ses dosyası bulundu.")

    # Her bir nota dosyasını işleyelim
    for file in note_files:
        input_file = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, file)

        # Ses dosyasını yükle
        sound = AudioSegment.from_wav(input_file)

        # Yeni frekans kayması uygula
        sound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * tuning_shift)
        })
        sound = sound.set_frame_rate(44100)

        # İşlenmiş ses dosyasını kaydet
        sound.export(output_file, format="wav")
        print(f"{file} dosyası işlendi, yeni dosya {output_file} olarak kaydedildi.")


# Ana fonksiyon
def main():
    input_folder = 'bütün notalar'  # Buraya dosya yolunu sabit olarak yazıyoruz
    output_folder = "output_notes3/"

    # Dosyaları işle
    process_files(input_folder, output_folder, TUNING_SHIFT)


if __name__ == "__main__":
    main()
