import time
import requests
from dotenv import load_dotenv
import os

# Załaduj zmienne z pliku .env
load_dotenv()

# Pobierz klucz API z pliku .env
api_key = os.getenv("LLAMACLOUD_KEY")

# Funkcja do wysyłania pliku
def upload_file(file_path):
    url = "https://api.cloud.llamaindex.ai/api/parsing/upload"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "language": "pl"
    }
    files = {
        "file": (os.path.basename(file_path), open(file_path, "rb"), "image/png"),
    }
    response = requests.post(url, headers=headers, data=data, files=files)
    if response.status_code == 200:
        print(f"Upload Successful for {file_path}: {response.json()}")
        return response.json().get("id")  # Zwraca ID z odpowiedzi
    else:
        print(f"Upload Failed for {file_path}: {response.status_code} {response.text}")
        return None

# Funkcja do sprawdzania statusu zadania
def check_job_status(job_id):
    url = f"https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        status = response.json().get("status")
        if status == "SUCCESS":
            print("Job is complete, result can be fetched.")
            return True
        else:
            print(f"Job status: {status}. Retrying in 5 seconds...")
            return False
    else:
        print(f"Failed to check job status: {response.status_code}")
        return False

# Funkcja do odbierania wyniku
def get_job_result(job_id):
    url = f"https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}/result/markdown"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        job_result = response.json()
        markdown_content = job_result.get("markdown")  # Przechwytujemy tylko sekcję markdown
        return markdown_content
    else:
        print(f"Failed to Get Job Result: {response.status_code} {response.text}")
        return None

# Funkcja do sortowania plików numerycznie
def numeric_sort_key(file_name):
    # Wyciągamy numer z nazwy pliku (np. frame_10.png -> 10)
    return int(file_name.split('_')[1].split('.')[0])

# Główna funkcja przetwarzająca obrazy
def process_frames(input_folder, output_file):
    if api_key is None:
        print("API key not found. Please check your .env file.")
        return

    all_markdown = []  # Lista na wszystkie markdowny

    # Pobierz listę plików i posortuj numerycznie
    file_names = [file_name for file_name in os.listdir(input_folder) if file_name.endswith(".png")]
    sorted_file_names = sorted(file_names, key=numeric_sort_key)

    # Iteracja po posortowanych plikach
    for i, file_name in enumerate(sorted_file_names):
        file_path = os.path.join(input_folder, file_name)

        print(f"Processing {file_path}...")

        # 1. Wysyłanie pliku
        job_id = upload_file(file_path)

        if job_id:
            # 2. Oczekiwanie na zakończenie przetwarzania
            while True:
                if check_job_status(job_id):
                    # 3. Jeśli status jest "SUCCESS", odbieramy wynik
                    markdown_content = get_job_result(job_id)
                    if markdown_content:
                        all_markdown.append(f"## Slajd {i + 1}\n\n{markdown_content}\n")
                    break
                time.sleep(5)  # Czekaj 5 sekund przed ponownym sprawdzeniem statusu

    # Zapisz wszystkie wyniki do pliku wynikowego
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(all_markdown)

    print(f"Results saved to {output_file}")

# Przykład wywołania funkcji w innym pliku
if __name__ == "__main__":
    input_folder = "./outputs/unique_frames"  # Folder wejściowy z obrazami
    output_file = "./outputs/result.md"  # Plik wynikowy

    process_frames(input_folder, output_file)
