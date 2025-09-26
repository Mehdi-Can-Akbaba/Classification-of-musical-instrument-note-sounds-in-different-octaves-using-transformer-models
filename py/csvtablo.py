import pickle
import pandas as pd
from sklearn.metrics import auc


# Metrik verisini 'metrics.pkl' dosyasından okuma ve istenilen formatta CSV'ye kaydetme
def extract_metrics_from_pkl(pkl_file, output_csv):
    # 'metrics.pkl' dosyasını aç ve yükle
    with open(pkl_file, "rb") as f:
        metrics_history = pickle.load(f)

    # İlgili metrikleri çıkarma
    metrics_list = []
    for metrics in metrics_history:
        epoch = metrics['epoch']

        # Sayısal olmayan değerleri kontrol etmeden önce, yalnızca sayısal veriye yuvarlama yap
        precision = metrics.get('precision', None)
        recall = metrics.get('recall', None)
        f1 = metrics.get('f1', None)
        macro_roc_auc = metrics.get('macro_roc_auc', None)

        # Eğer değer sayısal ise, 4 basamağa yuvarlaa
        if isinstance(precision, (int, float)):
            precision = round(precision, 4)
        if isinstance(recall, (int, float)):
            recall = round(recall, 4)
        if isinstance(f1, (int, float)):
            f1 = round(f1, 4)
        if isinstance(macro_roc_auc, (int, float)):
            macro_roc_auc = round(macro_roc_auc, 4)

        # Verileri bir satıra ekle
        metrics_list.append({
            "epoch": epoch,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "macro_roc_auc": macro_roc_auc

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
