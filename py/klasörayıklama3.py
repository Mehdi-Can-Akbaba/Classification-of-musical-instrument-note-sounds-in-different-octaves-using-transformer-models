import os
import shutil

# Ana dizin
base_dir = '//'

# Kaynak klasör (kontrbas1lik)
source_dir = os.path.join(base_dir, 'elektrobas4lük')

# "notalar" klasörü var mı kontrol et, yoksa oluştur
notalar_dir = os.path.join(base_dir, 'notalar')
if not os.path.exists(notalar_dir):
    os.makedirs(notalar_dir)

# Nota türleri
orijinal_notalar = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']
diyezli_notalar = ['Do#', 'Re#', 'Fa#', 'Sol#', 'La#']

# Nota klasörlerini oluşturma
for nota in orijinal_notalar + diyezli_notalar:
    nota_dir = os.path.join(notalar_dir, nota)
    if not os.path.exists(nota_dir):
        os.makedirs(nota_dir)

# Dosyaları kopyalama işlemi
if os.path.exists(source_dir):  # Kaynak klasör varsa
    print(f'{source_dir} klasörü bulundu. Dosyalar işleniyor...')
    for filename in os.listdir(source_dir):
        # Sadece "kb1_" ile başlayan ve ".wav" uzantılı dosyaları seç
        if filename.startswith('eb4_') and filename.endswith('.wav'):
            print(f'İşlenen dosya: {filename}')
            nota_name = filename[4:].split('.')[0]  # "kb1_" kısmını çıkart
            target_folder = None

            # Diyezli notalar için kontrol
            for nota in diyezli_notalar:
                if nota_name.startswith(nota):
                    target_folder = os.path.join(notalar_dir, nota)
                    break

            # Orijinal notalar için kontrol
            if not target_folder:
                for nota in orijinal_notalar:
                    if nota_name.startswith(nota) and not any(d in nota_name for d in diyezli_notalar):
                        target_folder = os.path.join(notalar_dir, nota)
                        break

            # Uygun klasöre kopyalama
            if target_folder:
                source_file = os.path.join(source_dir, filename)
                target_file = os.path.join(target_folder, filename)

                if not os.path.exists(target_file):  # Dosya daha önce kopyalanmamışsa
                    try:
                        shutil.copy(source_file, target_file)
                        print(f'{filename} -> {target_folder} klasörüne kopyalandı.')
                    except Exception as e:
                        print(f'Hata: {filename} kopyalanamadı. {e}')
                else:
                    print(f'{filename} zaten {target_folder} klasöründe mevcut.')
else:
    print(f'{source_dir} klasörü bulunamadı.')
