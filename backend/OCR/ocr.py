import time
import requests
from dotenv import load_dotenv
import os

# Załaduj zmienne z pliku .env
load_dotenv()

# Pobierz klucz API z pliku .env
api_key = os.getenv("LLAMACLOUD_KEY")

# Funkcja do wysyłania pliku
def upload_file(api_key, file_path):
    url = "https://api.cloud.llamaindex.ai/api/parsing/upload"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "language": "pl",
    }
    files = {
        "file": ("test.png", open(file_path, "rb"), "image/png"),
    }
    response = requests.post(url, headers=headers, data=data, files=files)
    if response.status_code == 200:
        print("Upload Successful:", response.json())
        return response.json().get("id")  # Zwraca ID z odpowiedzi
    else:
        print("Upload Failed:", response.status_code, response.text)
        return None

# Funkcja do sprawdzania statusu zadania
def check_job_status(api_key, job_id):
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
def get_job_result(api_key, job_id):
    url = f"https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}/result/markdown"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        job_result = response.json()
        markdown_content = job_result.get("markdown")  # Przechwytujemy tylko sekcję markdown
        print("Markdown Content:")
        print(markdown_content)  # Można teraz użyć tej zmiennej w kodzie
        return markdown_content
    else:
        print("Failed to Get Job Result:", response.status_code, response.text)
        return None

# Główna część skryptu
if __name__ == "__main__":
    if api_key is None:
        print("API key not found. Please check your .env file.")
    else:
        file_path = "./test.png"  # Ścieżka do pliku

        # 1. Wysyłanie pliku
        job_id = upload_file(api_key, file_path)
        
        if job_id:
            # 2. Oczekiwanie na zakończenie przetwarzania
            while True:
                if check_job_status(api_key, job_id):
                    # 3. Jeśli status jest "SUCCESS", odbieramy wynik
                    markdown_content = get_job_result(api_key, job_id)
                    break
                time.sleep(5)  # Czekaj 5 sekund przed ponownym sprawdzeniem statusu
