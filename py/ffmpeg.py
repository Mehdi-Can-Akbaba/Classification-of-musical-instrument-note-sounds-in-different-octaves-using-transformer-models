import os
import subprocess

def process_audio_dataset(input_base_dir, output_base_dir):
    """
    Veri setindeki ses dosyalarını FFmpeg ile işleyip çıktı klasörüne kaydeder.
    - 16kHz örnekleme hızı
    - Mono kanal
    """
    for split in ['train', 'val']:
        split_input_dir = os.path.join(input_base_dir, split)
        split_output_dir = os.path.join(output_base_dir, split)

        for label in ['akortlu', 'akortsuz']:
            label_input_dir = os.path.join(split_input_dir, label)
            label_output_dir = os.path.join(split_output_dir, label)

            for note in ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']:
                note_input_dir = os.path.join(label_input_dir, note)
                note_output_dir = os.path.join(label_output_dir, note)
                os.makedirs(note_output_dir, exist_ok=True)

                # Tüm ses dosyalarını işle
                for file_name in os.listdir(note_input_dir):
                    if file_name.endswith('.wav'):
                        input_path = os.path.join(note_input_dir, file_name)
                        output_path = os.path.join(note_output_dir, file_name)

                        # FFmpeg komutunu çalıştır
                        command = [
                            "ffmpeg", "-i", input_path,  # Giriş dosyası
                            "-ar", "16000",             # Örnekleme hızı 16kHz
                            "-ac", "1",                 # Mono kanal
                            output_path                # Çıkış dosyası
                        ]
                        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        print(f"Processed: {input_path} -> {output_path}")

# Veri setini işlemek için yolları tanımlayın
input_base_dir = "data"            # Girdi veri seti ana klasörü
output_base_dir = "processed"      # İşlenmiş veri seti ana klasörü

# İşleme fonksiyonunu çağır
process_audio_dataset(input_base_dir, output_base_dir)
