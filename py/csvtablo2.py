import pickle
import pandas as pd

# Metrik verisini 'metrics.pkl' dosyasından okuma ve istenilen formatta CSV'ye kaydetme
def extract_metrics_from_pkl(pkl_file, output_csv):
    # 'metrics.pkl' dosyasını aç ve yükle
    with open(pkl_file, "rb") as f:
        metrics_history = pickle.load(f)

    # İlgili metrikleri çıkarma
    metrics_list = []
    for metrics in metrics_history:
        epoch = metrics.get('epoch', None)
        precision = metrics.get('precision', None)
        recall = metrics.get('recall', None)
        f1 = metrics.get('f1', None)
        auc_value = metrics.get('auc', None)

        # Sayısal değerleri kontrol et ve 4 basamağa yuvarla
        if isinstance(precision, (int, float)):
            precision = round(precision, 4)
        if isinstance(recall, (int, float)):
            recall = round(recall, 4)
        if isinstance(f1, (int, float)):
            f1 = round(f1, 4)
        if isinstance(auc_value, (int, float)):
            auc_value = round(auc_value, 4)

        # Verileri bir satıra ekle
        metrics_list.append({
            "epoch": epoch,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "auc": auc_value
        })

    # Pandas DataFrame'e dönüştür
    metrics_df = pd.DataFrame(metrics_list)

    # CSV dosyasına kaydet
    metrics_df.to_csv(output_csv, index=False)
    print(f"Metrikler CSV dosyasına kaydedildi: {output_csv}")


# 'metrics.pkl' dosyasını ve kaydedilecek CSV dosyasının yolu
pkl_file = "sonuçlar/sew100/metrics.pkl"
output_csv = "sonuçlar/sew100/metrics3.csv"

# Fonksiyonu çağırma
extract_metrics_from_pkl(pkl_file, output_csv)
