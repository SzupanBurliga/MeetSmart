import whisper
import os
import sys

def transcribe_audio(audio_file_path):
    try:
        # Check if input file exists
        if not os.path.exists(audio_file_path):
            print(f"Error: Input file '{audio_file_path}' not found")
            return False

        # Create output directory
        output_dir = './transcriptions'
        os.makedirs(output_dir, exist_ok=True)

        print("Loading Whisper model...")
        model = whisper.load_model("medium")
        
        print(f"Transcribing {audio_file_path}...")
        result = model.transcribe(audio_file_path)

        # Generate output filename based on input filename
        base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        output_file_path = os.path.join(output_dir, f"{base_name}_transcription.txt")

        # Save transcription
        with open(output_file_path, "w", encoding='utf-8') as file:
            file.write(result['text'])

        print(f"Transcription successfully saved to: {output_file_path}")
        return True

    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return False

if __name__ == "__main__":
    audio_file = "wyklad_audio.mp3"
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    
    success = transcribe_audio(audio_file)
    if not success:
        sys.exit(1)