import os

# Bir oktavdaki tüm notalar
notes = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']

# Ana dizin (klasörlerin oluşturulacağı yer)
base_directory = 'akortlu'  # İstediğiniz ana dizin adı

# Ana dizini oluştur (eğer yoksa)
if not os.path.exists(base_directory):
    os.mkdir(base_directory)

# Her bir nota için klasör oluştur
for note in notes:
    folder_path = os.path.join(base_directory, note)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Klasör oluşturuldu: {folder_path}")
    else:
        print(f"Klasör zaten mevcut: {folder_path}")
