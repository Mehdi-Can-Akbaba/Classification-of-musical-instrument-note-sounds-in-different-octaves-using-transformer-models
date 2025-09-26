import os
import torch
import torchaudio
from torch.utils.data import Dataset, DataLoader
from transformers import Wav2Vec2Processor, Wav2Vec2ForSequenceClassification, Wav2Vec2Config
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
from tqdm import tqdm
import pickle
import time
import torch.nn.functional as F
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class AudioDataset(Dataset):
    def __init__(self, audio_paths, labels, processor, target_length=160000):
        self.audio_paths = audio_paths
        self.labels = labels
        self.processor = processor
        self.target_length = target_length

    def __len__(self):
        return len(self.audio_paths)

    def __getitem__(self, idx):
        file_path = self.audio_paths[idx]
        label = self.labels[idx]
        waveform, sr = torchaudio.load(file_path)
        waveform = waveform.squeeze()

        # Eğer ses uzunluğu `target_length`'den küçükse, padding ekle
        if waveform.size(0) < self.target_length:
            waveform = F.pad(waveform, (0, self.target_length - waveform.size(0)))
        else:
            waveform = waveform[:self.target_length]

        inputs = self.processor(waveform, sampling_rate=16000, return_tensors="pt", padding=True)
        return inputs.input_values[0], label

def load_data(base_dir, categories, notes):
    file_paths, labels = [], []
    label_map = {note: idx for idx, note in enumerate(notes)}

    for category in categories:
        for note in notes:
            path = os.path.join(base_dir, category, note)
            if not os.path.exists(path):
                print(f"Warning: {path} does not exist.")
                continue
            files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".wav")]
            file_paths.extend(files)
            labels.extend([label_map[note]] * len(files))
    return file_paths, labels

def collate_fn(batch):
    inputs = [item[0] for item in batch]
    labels = [item[1] for item in batch]
    inputs_padded = torch.nn.utils.rnn.pad_sequence(inputs, batch_first=True)
    return inputs_padded, torch.tensor(labels)

def train_model(train_loader, val_loader, model, processor, epochs=20, output_dir="model/wav2vec"):
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    loss_fn = torch.nn.CrossEntropyLoss()
    model.to(device)
    model.train()

    metrics_history = []

    for epoch in range(epochs):
        total_loss = 0
        with tqdm(total=len(train_loader), desc=f"Epoch {epoch + 1}/{epochs}") as pbar:
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = model(inputs).logits
                loss = loss_fn(outputs, labels)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                pbar.update(1)

        model.eval()
        val_targets, val_preds = [], []
        val_probs = []
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs).logits
                val_preds.extend(torch.argmax(outputs, axis=1).cpu().numpy())
                val_targets.extend(labels.cpu().numpy())
                val_probs.append(F.softmax(outputs, dim=1).cpu().numpy())  # Probabilities for all classes

        accuracy = accuracy_score(val_targets, val_preds)
        precision = precision_score(val_targets, val_preds, average="weighted")
        recall = recall_score(val_targets, val_preds, average="weighted")
        f1 = f1_score(val_targets, val_preds, average="weighted")

        # Calculate ROC curve and AUC for each class
        val_probs = np.array(val_probs)  # Convert list of probabilities to numpy array (num_samples x num_classes)
        fpr, tpr, roc_auc = {}, {}, {}

        for i in range(val_probs.shape[1]):  # Iterate over each class
            fpr[i], tpr[i], _ = roc_curve(val_targets, val_probs[:, i], pos_label=i)
            roc_auc[i] = auc(fpr[i], tpr[i])

        # Calculate micro-average ROC curve and AUC
        fpr["micro"], tpr["micro"], _ = roc_curve(val_targets, val_probs.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

        metrics = {"epoch": epoch + 1, "accuracy": accuracy, "precision": precision, "recall": recall,
                   "f1": f1, "roc_auc": roc_auc}
        metrics_history.append(metrics)
        print(f"Epoch {epoch + 1}: Loss: {total_loss:.4f}, Accuracy: {accuracy:.4f}, ROC AUC (micro): {roc_auc['micro']:.4f}")

        save_model_and_metrics(model, epoch, metrics_history, output_dir)



def save_model_and_metrics(model, epoch, metrics_history, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    torch.save(model.state_dict(), os.path.join(output_dir, f"wav2vec_epoch_{epoch}.pt"))
    with open(os.path.join(output_dir, "metrics.pkl"), "wb") as f:
        pickle.dump(metrics_history, f)

train_audio_paths, train_labels = load_data("processed/train", ["akortlu", "akortsuz"], ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"])
val_audio_paths, val_labels = load_data("processed/val", ["akortlu", "akortsuz"], ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"])

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
config = Wav2Vec2Config.from_pretrained("facebook/wav2vec2-base", num_labels=12)

model = Wav2Vec2ForSequenceClassification.from_pretrained("facebook/wav2vec2-base", config=config)

train_dataset = AudioDataset(train_audio_paths, train_labels, processor)
val_dataset = AudioDataset(val_audio_paths, val_labels, processor)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, collate_fn=collate_fn)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, collate_fn=collate_fn)

train_model(train_loader, val_loader, model, processor, epochs=20)
