import os
import torch
import torchaudio
from torch.utils.data import Dataset, DataLoader


# Dataset oluşturma
class AudioDataset(Dataset):
    def __init__(self, audio_paths, labels, target_length=160000):
        self.audio_paths = audio_paths
        self.labels = labels
        self.target_length = target_length  # Sesin hedef uzunluğu (pad yapılacak uzunluk)

    def __len__(self):
        return len(self.audio_paths)

    def __getitem__(self, idx):
        # Ses dosyasını yükleme
        waveform, sample_rate = torchaudio.load(self.audio_paths[idx])

        # Eğer mono ses ise, 2 boyutlu olacaktır, 2 kanallıysa 3 boyutlu olur.
        if len(waveform.shape) == 1:
            waveform = waveform.unsqueeze(0)  # [1, length] şeklinde yapar
        elif len(waveform.shape) == 2:
            # 2 kanallı ses dosyası varsa, her iki kanalı alırız ve [2, length] olur
            pass
        elif len(waveform.shape) > 2:
            # Eğer daha fazla kanal varsa, 3 boyutlu hale getirmek için slice yapabiliriz.
            waveform = waveform[:2, :]  # İlk 2 kanalı alarak sınırlama yapıyoruz

        # Hedef uzunluğa padding ekleme (uzunluk yetersizse pad ekleriz)
        if waveform.size(1) < self.target_length:
            padding = self.target_length - waveform.size(1)
            waveform = torch.cat([waveform, torch.zeros(waveform.size(0), padding)], dim=1)

        # Etiket (label) al
        label = self.labels[idx]

        return waveform, label


# Custom collate_fn for dynamic padding
def collate_fn(batch):
    waveforms, labels = zip(*batch)

    lengths = [waveform.size(1) for waveform in waveforms]
    max_length = max(lengths)

    padded_waveforms = []
    for waveform in waveforms:
        padding = max_length - waveform.size(1)
        padded_waveform = torch.cat([waveform, torch.zeros(waveform.size(0), padding)], dim=1)
        padded_waveforms.append(padded_waveform)

    padded_waveforms = torch.stack(padded_waveforms, dim=0)
    labels = torch.tensor(labels)
    return padded_waveforms, labels


# Ses dosyalarını ve etiketleri hazırlamak
def load_data(data_dir, categories, notes):
    audio_paths = []
    labels = []

    # Kategoriler ve notalar üzerinden geçerek dosyaları filtreleme
    for category in categories:
        for note in notes:
            category_dir = os.path.join(data_dir, category, note)
            if os.path.isdir(category_dir):
                for file in os.listdir(category_dir):
                    if file.endswith('.wav'):
                        audio_paths.append(os.path.join(category_dir, file))
                        labels.append(categories.index(category))

    return audio_paths, labels


# Veri hazırlama
data_dir = "data"  # Ana veri dizini
categories = ["akortsuz", "akortlu"]  # Kategoriler
notes = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]  # Notalar

# Eğitim ve doğrulama verisi için
train_audio_paths, train_labels = load_data(os.path.join(data_dir, "train"), categories, notes)
val_audio_paths, val_labels = load_data(os.path.join(data_dir, "val"), categories, notes)

# Eğitim ve doğrulama setini oluşturma
train_dataset = AudioDataset(train_audio_paths, train_labels)
val_dataset = AudioDataset(val_audio_paths, val_labels)

# Veri yükleyicileri
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, collate_fn=collate_fn)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, collate_fn=collate_fn)

# Eğitim verisi örnekleme
for waveform, label in train_loader:
    print(f"Waveform shape: {waveform.shape}, Label: {label}")
    break
