import subprocess
import os

def convert_to_wav(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Nie znaleziono pliku: {file_path}")
    
    output_file_path = file_path.rsplit('.', 1)[0] + '.wav'
    
    try:
        command = [
            'ffmpeg',
            '-i', file_path,
            '-vn',
            '-acodec', 'pcm_s32le',      # 32-bit depth for maximum quality
            '-ar', '96000',              # 96 kHz sampling rate
            '-ac', '2',                  # Stereo
            '-af', 'highpass=200,lowpass=3000,volume=1.5',  # Audio filters for speech enhancement
            '-q:a', '0',                 # Highest quality
            output_file_path
        ]
        
        subprocess.run(command, check=True, capture_output=True)
        
        print(f"Pomyślnie przekonwertowano {file_path} na {output_file_path}")
        return output_file_path
        
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas konwersji: {e.stderr.decode()}")
        raise
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
        raise


# tu do testów jak trzeba tego użyć w innym pliku
if __name__ == "__main__":
    input_path = "meeting_recording.webm"  
    try:
        convert_to_wav(input_path)
    except Exception as e:
        print(f"Error: {e}")