from pydub import AudioSegment
import os

def extract_notes(input_wav_file, output_folder, note_duration_ms=6000, silence_duration_ms=6000):
    """
    Ses dosyasındaki sesli notaları belirli bir düzenle çıkartır:
    - İlk 6 saniye sesli
    - Sonraki 6 saniye sessizlik
    :param input_wav_file: İşlenecek input WAV dosyasının yolu
    :param output_folder: Çıktı dosyalarının kaydedileceği klasör yolu
    :param note_duration_ms: Her sesli notanın süresi (milisaniye)
    :param silence_duration_ms: Her sessizlik süresi (milisaniye)
    """
    # Ses dosyasını yükle
    audio = AudioSegment.from_wav(input_wav_file)

    # Çıktı klasörünü kontrol et, yoksa oluştur
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    current_position = 0
    note_index = 1

    while current_position + note_duration_ms <= len(audio):
        # İlk 6 saniye sesli kısmı al
        chunk = audio[current_position:current_position + note_duration_ms]

        # Çıktı dosyasını oluştur
        output_wav_file = os.path.join(output_folder, f"note_{note_index}.wav")
        chunk.export(output_wav_file, format="wav")

        print(f"Notayı kaydettim: {output_wav_file}")

        # Pozisyonu güncelle: sesli ve sessizlik süresi
        current_position += note_duration_ms + silence_duration_ms
        note_index += 1

    # Dosyanın sonunda do7 sesi var, bu kısmı ayrıca işle
    if current_position < len(audio):
        last_note = audio[current_position:]
        output_wav_file = os.path.join(output_folder, f"note_{note_index}_do7.wav")
        last_note.export(output_wav_file, format="wav")
        print(f"Son notayı kaydettim (do7): {output_wav_file}")

# Kullanım örneği
input_wav_file = "piyano4l.wav"  # Giriş dosyası
output_folder = "piyano4lük"  # Çıkış klasörü

# Fonksiyonu çalıştır
extract_notes(input_wav_file, output_folder)
