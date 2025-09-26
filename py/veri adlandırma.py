import os

# Akortlu klasörü yolunu belirt
akortlu_dir = 'yedek/akortsuz/Do/'

# Dosyaları al
files = [f for f in os.listdir(akortlu_dir) if f.endswith('.wav')]

# Dosyaları sıralayın (alfabetik sıraya göre)
files.sort()

# Dosyaları yeniden adlandır
for i, file in enumerate(files, 1):
    # Yeni dosya adını oluştur
    new_name = f"akortsuz_Do_{i}.wav"

    # Eski dosya yolu ve yeni dosya yolu
    old_file_path = os.path.join(akortlu_dir, file)
    new_file_path = os.path.join(akortlu_dir, new_name)

    # Dosyayı yeniden adlandır
    os.rename(old_file_path, new_file_path)

print("Akortlu dosyalar başarıyla sıralandı ve adlandırıldı.")
