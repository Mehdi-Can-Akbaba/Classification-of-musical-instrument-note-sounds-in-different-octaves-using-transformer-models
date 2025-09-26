import os
import shutil

# Ana klasörünüzün yolunu belirtin
main_folder = "all notes"

# Mi2'den Do7'ye kadar geçerli notalar
valid_notes = [
    "Mi2", "Fa2", "Fa#2", "Sol2", "Sol#2", "La2", "La#2", "Si2",
    "Do3", "Do#3", "Re3", "Re#3", "Mi3", "Fa3", "Fa#3", "Sol3", "Sol#3", "La3", "La#3", "Si3",
    "Do4", "Do#4", "Re4", "Re#4", "Mi4", "Fa4", "Fa#4", "Sol4", "Sol#4", "La4", "La#4", "Si4",
    "Do5", "Do#5", "Re5", "Re#5", "Mi5", "Fa5", "Fa#5", "Sol5", "Sol#5", "La5", "La#5", "Si5",
    "Do6", "Do#6", "Re6", "Re#6", "Mi6", "Fa6", "Fa#6", "Sol6", "Sol#6", "La6", "La#6", "Si6",
    "Do7"
]



# Log dosyasını temizle
with open(log_file, "w") as log:
    log.write("Kopyalama İşlemi Logları\n")
    log.write("=========================\n")

# Kopyalama işlemi
for file in os.listdir(main_folder):
    if file.endswith(".wav"):
        copied = False
        for note in valid_notes:
            if note in file:
                note_folder = os.path.join(main_folder, note)

                # Nota için klasör oluştur
                if not os.path.exists(note_folder):
                    os.makedirs(note_folder)

                try:
                    # Dosyayı ilgili klasöre kopyala
                    shutil.copy2(os.path.join(main_folder, file), os.path.join(note_folder, file))
                    copied = True
                    message = f"BAŞARILI: {file} -> {note_folder}"
                    print(message)
                    with open(log_file, "a") as log:
                        log.write(message + "\n")
                except Exception as e:
                    message = f"BAŞARISIZ: {file} -> {note_folder} | Hata: {e}"
                    print(message)
                    with open(log_file, "a") as log:
                        log.write(message + "\n")
                break

        # Eğer dosya bir notaya eşleşmediyse
        if not copied:
            message = f"BAŞARISIZ: {file} -> Eşleşen nota bulunamadı"
            print(message)
            with open(log_file, "a") as log:
                log.write(message + "\n")

print("Kopyalama işlemi tamamlandı! Sonuçlar ekrana ve 'kopyalama_log.txt' dosyasına kaydedildi.")
