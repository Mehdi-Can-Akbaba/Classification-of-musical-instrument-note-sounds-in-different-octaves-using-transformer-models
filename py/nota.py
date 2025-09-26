import os

from pydub import AudioSegment


def extract_notes(input_wav_file, output_folder, note_duration_ms=6000, silence_duration_ms=3000):
    """
    WAV dosyasındaki sesli notaları 6 saniye aralıklarla alıp, 3 saniye sessizliği atma.
    :param input_wav_file: İşlenecek input WAV dosyasının yolu
    :param output_folder: Çıktı dosyalarının kaydedileceği klasör yolu
    :param note_duration_ms: Bir notanın süresi (milisaniye)
    :param silence_duration_ms: Sessizlik süresi (milisaniye)
    """
    # WAV dosyasını yükle
    audio = AudioSegment.from_wav(input_wav_file)

    # Çıktı dosya yolunun var olup olmadığını kontrol et, yoksa oluştur
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Sesli kısımları tespit et
    current_position = 0
    note_index = 1

    while current_position + note_duration_ms <= len(audio):
        # 6 saniye sesli bölüm al
        chunk = audio[current_position:current_position + note_duration_ms]

        # Sesli parçayı kaydet
        output_wav_file = os.path.join(output_folder, f"note_{note_index}.wav")
        chunk.export(output_wav_file, format="wav")

        # Kaydettikten sonra bilgilendirme mesajı
        print(f"Notayı kaydettim: {output_wav_file}")

        # 3 saniye sessizlik kısmını atla
        current_position += note_duration_ms + silence_duration_ms
        note_index += 1

# Kullanım örneği
input_wav_file = "elektrobas4lük.wav"  # Kaydedilen WAV dosyasının tam yolunu belirtin
output_folder = "elektrobas4lük"  # Çıktı dosyalarının kaydedileceği klasörün yolu belirtin

# Fonksiyonu çalıştır
extract_notes(input_wav_file, output_folder)
