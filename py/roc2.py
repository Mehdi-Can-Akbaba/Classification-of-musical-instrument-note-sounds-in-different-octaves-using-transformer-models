import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc

# Metriklerin kaydedildiği dizin
output_dir = ""
metrics_path = os.path.join(output_dir, "sonuçlar/wav2vec2100/metrics.pkl")

# Metrikleri yükle
with open(metrics_path, "rb") as f:
    metrics_history = pickle.load(f)

# Macro ROC AUC grafiği çizme fonksiyonu
def plot_macro_roc_auc(epoch_metrics, epoch_number):
    fpr_dict = epoch_metrics["fpr"]
    tpr_dict = epoch_metrics["tpr"]
    valid_labels = fpr_dict.keys()

    # Tüm sınıfların FPR ve TPR'sini birleştir
    all_fpr = np.unique(np.concatenate([fpr_dict[label] for label in valid_labels]))
    mean_tpr = np.zeros_like(all_fpr)

    for label in valid_labels:
        mean_tpr += np.interp(all_fpr, fpr_dict[label], tpr_dict[label])

    mean_tpr /= len(valid_labels)
    macro_auc = auc(all_fpr, mean_tpr)

    # Grafiği çiz
    plt.figure()
    plt.plot(all_fpr, mean_tpr, color="blue", label=f"Macro ROC AUC (AUC={macro_auc:.4f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title(f"Epoch {epoch_number} - Macro ROC AUC")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.show()

# İlk 5 epoch için grafikleri çiz
for epoch in range(99, 100):  # 1'den 5'e kadar
    epoch_metrics = metrics_history[epoch - 1]  # Epoch 1 için 0. index
    plot_macro_roc_auc(epoch_metrics, epoch)
