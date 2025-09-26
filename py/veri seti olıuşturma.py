import os
import shutil
from sklearn.model_selection import train_test_split

# Kaynak dizin
base_dir = "data"  # Ana klasör yolu
categories = ["akortlu", "akortsuz"]
notes = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]

# Hedef dizinler
train_dir = os.path.join(base_dir, "data/train")
val_dir = os.path.join(base_dir, "data/val")

# Klasör yapısını oluşturma
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

for category in categories:
    for note in notes:
        os.makedirs(os.path.join(train_dir, category, note), exist_ok=True)
        os.makedirs(os.path.join(val_dir, category, note), exist_ok=True)

# Verileri bölme
for category in categories:
    for note in notes:
        source_dir = os.path.join(base_dir, category, note)
        files = [f for f in os.listdir(source_dir) if f.endswith(".wav")]
        train_files, val_files = train_test_split(files, test_size=0.2, random_state=42)

        for file in train_files:
            shutil.copy(os.path.join(source_dir, file), os.path.join(train_dir, category, note))
        for file in val_files:
            shutil.copy(os.path.join(source_dir, file), os.path.join(val_dir, category, note))
