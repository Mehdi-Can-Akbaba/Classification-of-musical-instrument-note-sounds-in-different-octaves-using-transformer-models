from matplotlib import pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize

# Gerçek etiketler ve modelin tahmin skorları
y_true = [0, 1, 2, 2, 0, 1]  # Gerçek etiketler
y_score = [
    [0.8, 0.1, 0.1],
    [0.2, 0.7, 0.1],
    [0.1, 0.2, 0.7],
    [0.1, 0.3, 0.6],
    [0.9, 0.05, 0.05],
    [0.05, 0.8, 0.15]
]  # Modelin tahmin ettiği olasılıklar

# Sınıf sayısını ve binarize edilmiş etiketleri hazırlayın
num_classes = 3
y_true_bin = label_binarize(y_true, classes=[i for i in range(num_classes)])

# ROC eğrisini hesaplayın ve çizdirin
fpr = {}
tpr = {}
roc_auc = {}

for i in range(num_classes):
    fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], [score[i] for score in y_score])
    roc_auc[i] = auc(fpr[i], tpr[i])

# ROC eğrisini çiz
plt.figure(figsize=(8, 8))
for i in range(num_classes):
    plt.plot(fpr[i], tpr[i], lw=2, label=f'Class {i} ROC curve (AUC = {roc_auc[i]:.2f})')

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.grid()
plt.tight_layout()
plt.savefig('roc_curve.png')
plt.show()
