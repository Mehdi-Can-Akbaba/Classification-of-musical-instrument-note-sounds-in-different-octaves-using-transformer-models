import os
import shutil
import re

# Ana klasörün yolunu belirtin
main_folder = "output_notes"

# 12 ana nota (diyezli ve diyezsiz)
valid_notes = [
    "Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"
]

# Klasörleri oluştur
for note in valid_notes:
    note_folder = os.path.join(main_folder, note)
    if not os.path.exists(note_folder):
        os.makedirs(note_folder)
        print(f"Klasör oluşturuldu: {note_folder}")

# Dosyaları ilgili klasörlere kopyala
for file in os.listdir(main_folder):
    if file.endswith(".wav"):
        copied = False

        # Dosya adındaki notayı bulmak için kontrol et
        for note in valid_notes:
            # Regex ile dosya adında notayı kontrol et
            # Örnek dosya adları: a1_Do#3.wav, v4_Sol4.wav, eg2_La#6.wav
            match = re.search(rf'_(Do#|Do|Re#|Re|Mi|Fa#|Fa|Sol#|Sol|La#|La|Si)(\d+)?\b', file)
            if match and match.group(1) == note:  # Bulunan nota ile kontrol edilen notayı eşleştir
                note_folder = os.path.join(main_folder, note)

                try:
                    # Dosyayı ilgili klasöre kopyala
                    shutil.copy2(os.path.join(main_folder, file), os.path.join(note_folder, file))
                    copied = True
                    print(f"BAŞARILI: {file} -> {note_folder}")
                except Exception as e:
                    print(f"BAŞARISIZ: {file} -> {note_folder} | Hata: {e}")
                break

        # Eğer dosya bir notaya eşleşmediyse
        if not copied:
            print(f"BAŞARISIZ: {file} -> Eşleşen nota bulunamadı")

print("Kopyalama işlemi tamamlandı!")
