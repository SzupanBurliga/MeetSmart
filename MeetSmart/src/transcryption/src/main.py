import whisper
import os

# Ścieżka do pliku MP3
mp3_file_path = 'babka_1.mp3'

# Wczytanie modelu Whisper (model może być np. `base`, `small`, `medium`, `large`)
model = whisper.load_model("base")  # Możesz zmienić na inny rozmiar modelu, np. 'small', 'medium', 'large'

# Przeprowadzenie transkrypcji z pliku MP3
result = model.transcribe(mp3_file_path)

# Wynik transkrypcji
text = result['text']
print("Transkrypcja:\n", text)

# Zapisanie transkrypcji do pliku tekstowego
with open("transcription.txt", "w", encoding="utf-8") as file:
    file.write(text)