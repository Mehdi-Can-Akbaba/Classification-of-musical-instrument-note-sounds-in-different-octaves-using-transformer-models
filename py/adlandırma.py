import os

# Dosya yolu ve dosyaların bulunduğu dizin
directory = 'elektrobas4lük'  # Dosyaların bulunduğu dizin. Gerekirse burayı güncelleyin.

# Dosyaları listele
file_list = [f for f in os.listdir(directory) if f.endswith(".wav")]

# Dosyaları yeniden adlandırma
for filename in file_list:
    # Dosya adı şu formatta: "note_1 (Sol3).wav"
    if ' (' in filename:
        # Parantez içindeki kısmı al ve yeni dosya adı oluştur
        note_name = filename.split('(')[1].replace(')', '').strip()  # Örneğin "Sol3"
        new_name = f"eb4_{note_name}"  # Yeni ad: k4_Sol3.wav
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
        print(f"Dosya {filename} yeniden adlandırıldı: {new_name}")
