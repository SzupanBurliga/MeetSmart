import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("LLAMACLOUD_KEY")

def upload_file(file_path):
    url = "https://api.cloud.llamaindex.ai/api/parsing/upload"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {"language": "pl"}
    files = {"file": (os.path.basename(file_path), open(file_path, "rb"), "image/png")}
    response = requests.post(url, headers=headers, data=data, files=files)
    
    if response.status_code == 200:
        print(f"Upload Successful for {file_path}: {response.json()}")
        return response.json().get("id")  
    else:
        print(f"Upload Failed for {file_path}: {response.status_code} {response.text}")
        return None

def check_job_status(job_id):
    url = f"https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            status = response.json().get("status")
            print(f"Job {job_id} status: {status}")
            if status == "SUCCESS":
                return True
            elif status == "FAILED":
                print(f"Job {job_id} failed.")
                return False
        else:
            print(f"Failed to check job status: {response.status_code}")
            return False
        print("Retrying in 5 seconds...")
        time.sleep(5)

def get_job_result(job_id):
    url = f"https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}/result/markdown"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Job {job_id} result retrieved successfully.")
        return response.json().get("markdown")
    else:
        print(f"Failed to get job result for {job_id}: {response.status_code} {response.text}")
        return None

def numeric_sort_key(file_name):
    return float(file_name.split('_')[1].split('s')[0])

def process_frames(input_folder, output_file):
    if api_key is None:
        print("API key not found. Please check your .env file.")
        return
    
    all_markdown = []
    file_names = sorted(
        [f for f in os.listdir(input_folder) if f.endswith(".png")],
        key=numeric_sort_key
    )
    
    job_map = {}
    for file_name in file_names:
        file_path = os.path.join(input_folder, file_name)
        print(f"Uploading {file_path}...")
        job_id = upload_file(file_path)
        if job_id:
            job_map[job_id] = file_name
    
    for job_id, file_name in job_map.items():
        print(f"Checking status for job {job_id}...")
        if check_job_status(job_id):
            print(f"Fetching result for job {job_id}...")
            markdown_content = get_job_result(job_id)
            if markdown_content:
                timestamp = file_name.split('_')[1].split('s')[0]
                all_markdown.append(f"Timestamp: {timestamp}s\n\n{markdown_content}\n")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(all_markdown)
    
    print(f"Results saved to {output_file}")

# if __name__ == "__main__":
#     input_folder = "./outputs/unique_frames"
#     output_file = "./outputs/result.md"
#     process_frames(input_folder, output_file)
