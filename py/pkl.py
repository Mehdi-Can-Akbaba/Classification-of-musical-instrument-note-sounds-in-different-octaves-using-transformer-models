
import pickle


# .pkl dosyasının yolu
file_path = 'sonuçlar/wav2vec2100/metrics.pkl'  # Dosya yolu

# Dosyayı yükle
with open(file_path, 'rb') as f:
    data = pickle.load(f)

# İçeriği yazdır
print(data)