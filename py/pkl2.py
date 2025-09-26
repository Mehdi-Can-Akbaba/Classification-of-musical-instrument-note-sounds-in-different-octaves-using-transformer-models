import pickle

# Metriklerin kaydedildiği dosyanın yolu
metrics_path = "C:/Users/Mehdi/PycharmProjects/pythonProject4/sonuçlar/wav2vec2100/metrics.pkl"

# Dosyayı aç ve içeriğini yükle
with open(metrics_path, "rb") as f:
    metrics_history = pickle.load(f)

# İlk epoch'un yapısını incele
print(f"First Epoch Data Type: {type(metrics_history[0])}")
print(f"First Epoch Content: {metrics_history[0]}")
