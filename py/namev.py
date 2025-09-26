import os

# Do3'ten La6'ya kadar olan notalar (viola için)
notes = [
    'Do3', 'Do#3', 'Re3', 'Re#3', 'Mi3', 'Fa3', 'Fa#3', 'Sol3', 'Sol#3', 'La3',
    'La#3', 'Si3', 'Do4', 'Do#4', 'Re4', 'Re#4', 'Mi4', 'Fa4', 'Fa#4', 'Sol4',
    'Sol#4', 'La4', 'La#4', 'Si4', 'Do5', 'Do#5', 'Re5', 'Re#5', 'Mi5', 'Fa5',
    'Fa#5', 'Sol5', 'Sol#5', 'La5', 'La#5', 'Si5', 'Do6', 'Do#6', 'Re6', 'Re#6',
    'Mi6', 'Fa6', 'Fa#6', 'Sol6', 'Sol#6', 'La6'
]

# Dosya yolu ve dosyaların bulunduğu dizin
directory = 'viola4lük'  # Dosyaların bulunduğu dizin. Gerekirse burayı güncelleyin.

# Dosyaları listele ve sırasıyla yeniden adlandır
file_list = [f for f in os.listdir(directory) if f.endswith(".wav")]
file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))  # note_1.wav, note_2.wav gibi dosyalar sıralanır.

# Dosya adlarını yeniden adlandırma
for i, filename in enumerate(file_list):
    if i >= len(notes):  # Eğer dosya sayısı notalardan fazlaysa döngüyü sonlandır
        print("Tüm notalar atandı, ancak dosyalar daha fazla. Kontrol edin!")
        break
    # Yeni adın, eski adın yanına parantez içinde eklenmesi
    new_name = f"{filename.split('.')[0]} ({notes[i]}).wav"
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
    print(f"Dosya {filename} yeniden adlandırıldı: {new_name}")
