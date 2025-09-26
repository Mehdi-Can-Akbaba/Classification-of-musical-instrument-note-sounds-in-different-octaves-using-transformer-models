# Notaların frekansları
notes_frequencies = {
    'Mi2': 82.41, 'Fa2': 87.31, 'Fa#2': 92.50, 'Sol2': 98.00, 'Sol#2': 103.83,
    'La2': 110.00, 'La#2': 116.54, 'Si2': 123.47, 'Do3': 130.81, 'Do#3': 138.59,
    'Re3': 146.83, 'Re#3': 155.56, 'Mi3': 164.81, 'Fa3': 174.61, 'Fa#3': 185.00,
    'Sol3': 196.00, 'Sol#3': 207.65, 'La3': 220.00, 'La#3': 233.08, 'Si3': 246.94,
    'Do4': 261.63, 'Do#4': 277.18, 'Re4': 293.66, 'Re#4': 311.13, 'Mi4': 329.63,
    'Fa4': 349.23, 'Fa#4': 369.99, 'Sol4': 392.00, 'Sol#4': 415.30, 'La4': 440.00,
    'La#4': 466.16, 'Si4': 493.88, 'Do5': 523.25, 'Do#5': 554.37, 'Re5': 587.33,
    'Re#5': 622.25, 'Mi5': 659.26, 'Fa5': 698.46, 'Fa#5': 739.99, 'Sol5': 783.99,
    'Sol#5': 830.61, 'La5': 880.00, 'La#5': 932.33, 'Si5': 987.77, 'Do6': 1046.50,
    'Do#6': 1108.73, 'Re6': 1174.66, 'Re#6': 1244.51, 'Mi6': 1318.51, 'Fa6': 1396.91,
    'Fa#6': 1479.98, 'Sol6': 1567.98, 'Sol#6': 1661.22, 'La6': 1760.00, 'La#6': 1864.66,
    'Si6': 1975.53, 'Do7': 2093.00, 'Do#7': 2217.46, 'Re7': 2349.32, 'Re#7': 2489.02,
    'Mi7': 2637.02
}

# %10 artışla yeni frekanslar hesaplanır
increased_frequencies = {note: freq * 1.1 for note, freq in notes_frequencies.items()}

# 3 Hz'lik yakınlık sınırına göre kontrol yapalım
close_notes = {}

# 3 Hz'lik farkı kabul etmiyoruz
for note, increased_freq in increased_frequencies.items():
    close_notes[note] = []
    for other_note, other_freq in increased_frequencies.items():
        if note != other_note and abs(increased_freq - other_freq) <= 3:
            # Eğer frekans farkı 3 Hz'den küçükse, bu iki notayı ayırt edilemez kabul et
            close_notes[note].append(other_note)

# Debug: artan frekansları ekrana yazdıralım
print("Artan Frekanslar:")
for note, increased_freq in increased_frequencies.items():
    print(f"{note}: {increased_freq:.2f} Hz")
print("\n")

# Yakın notaları yazdırma
print("Yakın Notalar:")
for note, close in close_notes.items():
    if close:
        print(f"{note} - Yeni Frekans: {increased_frequencies[note]:.2f} Hz")
        print(f"Yakın Notalar: {', '.join(close)}")
        print('-' * 50)
