import os
import torch
import torchaudio
from transformers import HubertForSequenceClassification, HubertProcessor
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import time

# Cihazı belirleyin: Eğer GPU varsa, CUDA'yı kullanın, yoksa CPU'yu kullanın.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Dataset Sınıfı
class AudioDataset(Dataset):
    def __init__(self, file_paths, labels, processor, max_length=96000):
        self.file_paths = file_paths
        self.labels = labels
        self.processor = processor
        self.max_length = max_length  # Max length for padding or trimming

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        file_path = self.file_paths[idx]
        label = self.labels[idx]
        waveform, sr = torchaudio.load(file_path)

        # Örnekleme hızını 16000 Hz'e dönüştür
        if sr != 16000:
            waveform = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(waveform)
            sr = 16000

        # Eğer mono ise (tek kanal), boyut (1, N) şeklinde olur
        # Eğer stereo ise (iki kanal), boyut (2, N) şeklinde olur
        waveform = waveform.squeeze()

        # Padding or trimming to max_length
        if waveform.size(0) < self.max_length:
            padding = self.max_length - waveform.size(1)  # Burada 1. boyut (zaman boyutu) ile uyumlu padding yapılır
            if waveform.size(0) == 1:  # Mono ses
                waveform = torch.cat([waveform, torch.zeros(1, padding).to(waveform.device)], dim=1)
            elif waveform.size(0) == 2:  # Stereo ses
                waveform = torch.cat([waveform, torch.zeros(2, padding).to(waveform.device)], dim=1)
        else:
            waveform = waveform[:, :self.max_length]  # Trim if it's longer than max_length

        # Feature Extractor ile girişleri hazırla
        inputs = self.processor(waveform, sampling_rate=sr, return_tensors="pt", padding=True)
        return inputs.input_values[0], label


# Veri Yükleme
def load_data(base_dir, notes, categories):
    file_paths, labels = [], []
    label_map = {note: idx for idx, note in enumerate(notes)}

    for category in categories:
        for note in notes:
            path = os.path.join(base_dir, category, note)
            files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".wav")]
            file_paths.extend(files)
            labels.extend([label_map[note]] * len(files))
    return file_paths, labels


# Model Kaydetme ve Metrikler
def save_model_and_metrics(model, epoch, metrics_history, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Modelin en iyi ve son halini kaydet
    output_path = os.path.join(output_dir, f"hubert_epoch_{epoch}.pt")
    torch.save(model.state_dict(), output_path)

    # Metrikleri kaydet
    metrics_path = os.path.join(output_dir, "metrics.pkl")
    with open(metrics_path, "wb") as f:
        pickle.dump(metrics_history, f)


# Eğitim Fonksiyonu
def train_model(train_loader, val_loader, model, processor, epochs=10, output_dir="model/hubert"):
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    loss_fn = torch.nn.CrossEntropyLoss()
    model.train()

    metrics_history = []

    for epoch in range(epochs):
        total_loss, total_accuracy = 0, 0
        num_batches = len(train_loader)
        epoch_start_time = time.time()

        for batch_idx, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)  # Modeli ve inputları cihaza gönder
            optimizer.zero_grad()
            outputs = model(inputs).logits
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            # Yüzdesel ilerleme yazdırma
            progress = (batch_idx + 1) / num_batches * 100
            epoch_elapsed_time = time.time() - epoch_start_time
            avg_time_per_batch = epoch_elapsed_time / (batch_idx + 1)
            remaining_batches = num_batches - (batch_idx + 1)
            remaining_time = remaining_batches * avg_time_per_batch
            remaining_time_str = str(time.strftime("%H:%M:%S", time.gmtime(remaining_time)))

            print(f"\rEpoch {epoch + 1}/{epochs} - {progress:.2f}% - Loss: {total_loss:.4f} - Remaining Time: {remaining_time_str}", end='')

        # Validation
        model.eval()
        val_targets, val_preds = [], []
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)  # Modeli ve inputları cihaza gönder
                outputs = model(inputs).logits
                val_preds.extend(torch.argmax(outputs, axis=1).cpu().numpy())
                val_targets.extend(labels.cpu().numpy())

        # Metrik Hesaplama
        accuracy = accuracy_score(val_targets, val_preds)
        precision = precision_score(val_targets, val_preds, average="weighted")
        recall = recall_score(val_targets, val_preds, average="weighted")
        f1 = f1_score(val_targets, val_preds, average="weighted")
        metrics = {"epoch": epoch + 1, "accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}
        metrics_history.append(metrics)

        # Model ve Metrikleri Kaydetme
        save_model_and_metrics(model, epoch, metrics_history, output_dir)

        print(f"\nEpoch {epoch + 1}/{epochs} - Loss: {total_loss:.4f} - Accuracy: {accuracy:.4f}")

    # Eğitim sonunda modelin son halini kaydediyoruz
    save_model_and_metrics(model, epochs, metrics_history, output_dir)


# Veri Setlerini Yükleme
train_files, train_labels = load_data("data/train", notes=["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"], categories=["akortlu", "akortsuz"])
val_files, val_labels = load_data("data/val", notes=["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"], categories=["akortlu", "akortsuz"])

processor = HubertProcessor.from_pretrained("facebook/hubert-base-ls960")
model = HubertForSequenceClassification.from_pretrained("facebook/hubert-base-ls960", num_labels=12)

train_dataset = AudioDataset(train_files, train_labels, processor)
val_dataset = AudioDataset(val_files, val_labels, processor)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

# Modeli Eğit
train_model(train_loader, val_loader, model, processor)
