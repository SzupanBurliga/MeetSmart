import os
import re

def process_and_merge_files(transcription_file, ocr_file, output_file):
    # Funkcja do parsowania danych z pliku transcryption.txt
    def parse_transcription(file_path):
        transcription_data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r"Timestamp: ([\d.]+)s \| (.+)", line)
                if match:
                    timestamp = float(match.group(1))
                    content = match.group(2)
                    transcription_data.append((timestamp, content))
        return transcription_data

    # Funkcja do parsowania danych z pliku ocr.md
    def parse_ocr(file_path):
        ocr_data = []
        current_content = []
        current_timestamp = None

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r"Timestamp: ([\d.]+)s", line)
                if match:
                    if current_timestamp is not None:
                        ocr_data.append((current_timestamp, "\n".join(current_content)))
                    current_timestamp = float(match.group(1))
                    current_content = []
                else:
                    current_content.append(line.strip())

            if current_timestamp is not None:
                ocr_data.append((current_timestamp, "\n".join(current_content)))

        return ocr_data

    # Funkcja do łączenia danych na podstawie timestampów
    def merge_data(transcription_data, ocr_data):
        combined_data = sorted(transcription_data + ocr_data, key=lambda x: x[0])
        return combined_data

    # Funkcja do zapisu wyników do pliku w formacie Markdown
    def save_to_file(output_path, combined_data):
        with open(output_path, 'w', encoding='utf-8') as file:
            for _, content in combined_data:
                file.write(f"{content}\n\n")

    # Sprawdzenie, czy pliki istnieją
    if not os.path.exists(transcription_file):
        print(f"Plik {transcription_file} nie istnieje!")
        return

    if not os.path.exists(ocr_file):
        print(f"Plik {ocr_file} nie istnieje!")
        return

    # Parsowanie danych
    transcription_data = parse_transcription(transcription_file)
    ocr_data = parse_ocr(ocr_file)

    # Łączenie danych
    combined_data = merge_data(transcription_data, ocr_data)

    # Zapis wyników
    save_to_file(output_file, combined_data)

    print(f"Dane zostały połączone i zapisane w pliku {output_file}.")


#process_and_merge_files("outputs/output_audio_transcription_with_diarization.txt", "outputs/result.md", "outputs/merged_output.md")