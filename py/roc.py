import pickle
import matplotlib.pyplot as plt
import numpy as np

# metrics.pkl dosyasını yükle
metrics_file = "sew100/metrics.pkl"
with open(metrics_file, "rb") as f:
    metrics_history = pickle.load(f)

# Epoch'lara göre macro_roc_auc değerlerini al
epochs = [metrics["epoch"] for metrics in metrics_history]
macro_roc_auc_values = [metrics["macro_roc_auc"] for metrics in metrics_history]

# ROC eğrisi çizimi için ilk 5 epoch'un fpr ve tpr değerlerini al
fpr_tpr_epochs = metrics_history[:5]  # İlk 5 epoch

# Macro ROC AUC grafiği
plt.figure(figsize=(10, 6))

# Her epoch'un ROC eğrisi
for epoch_data in fpr_tpr_epochs:
    epoch = epoch_data["epoch"]
    fpr = np.unique(np.concatenate([epoch_data["fpr"][i] for i in epoch_data["fpr"].keys()]))
    mean_tpr = np.zeros_like(fpr)
    for i in epoch_data["fpr"].keys():
        mean_tpr += np.interp(fpr, epoch_data["fpr"][i], epoch_data["tpr"][i])
    mean_tpr /= len(epoch_data["fpr"].keys())
    plt.plot(fpr, mean_tpr, label=f"Epoch {epoch} (AUC = {epoch_data['macro_roc_auc']:.4f})")

# Genel ayarlar
plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
plt.title("ROC Curve for First 5 Epochs")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc="lower right")
plt.grid(True)
plt.show()

# Macro ROC AUC değerlerinin epoch'lara göre değişimi
plt.figure(figsize=(10, 6))
plt.plot(epochs, macro_roc_auc_values, marker='o', linestyle='-', color='b', label="Macro ROC AUC")
plt.title("Macro ROC AUC Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Macro ROC AUC")
plt.xticks(epochs)  # Epoch'ları x eksenine koy
plt.grid(True)
plt.legend()
plt.show()
