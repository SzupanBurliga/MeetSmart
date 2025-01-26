def convert_audio_to_text(audio_file_path, diarization_file_path, tolerance=0.15):
    import whisper # type: ignore
    import os
    import json

    model = whisper.load_model("medium")
    language = "pl"
    
    # Read diarization results from the text file
    with open(diarization_file_path, 'r', encoding='utf-8') as f:
        diarization_results = json.load(f)
    
    processed_diarization = []
    for speaker in diarization_results:
        processed_diarization.append({
            'speaker': speaker['speaker'],
            'start': float(speaker['start_time'].replace('s', '')),
            'end': float(speaker['end_time'].replace('s', ''))
        })

    result = model.transcribe(audio_file_path, word_timestamps=True)
    output_dir = '../media_manager/outputs'
    os.makedirs(output_dir, exist_ok=True)
    text_file_path = os.path.join(output_dir, audio_file_path.rsplit('.', 1)[0] + '_transcription_with_diarization.txt')
    transcription_text = "" 
    with open(text_file_path, 'w', encoding='utf-8') as f:
        for segment in result["segments"]:
            segment_text = segment["text"]
            start_time = segment["start"]
            end_time = segment["end"]
            
            active_speakers = []
            for speaker_info in processed_diarization:
                if (start_time >= speaker_info['start'] - tolerance and 
                    start_time <= speaker_info['end'] + tolerance) or \
                   (end_time >= speaker_info['start'] - tolerance and 
                    end_time <= speaker_info['end'] + tolerance) or \
                   (start_time <= speaker_info['start'] and 
                    end_time >= speaker_info['end']):
                    active_speakers.append(speaker_info['speaker'])
            
            if active_speakers:
                speakers_str = " & ".join(sorted(set(active_speakers)))
            else:
                speakers_str = "Unknown"
            
            f.write(f"{speakers_str} | {start_time:.2f}s | {end_time:.2f}s | {segment_text}\n")
            transcription_text += f"{speakers_str} | {segment_text}\n"

    print(f"Pomyślnie utworzono transkrypcję z diarizacją: {text_file_path}")
    return transcription_text

if __name__ == "__main__":
    audio_file_path = "D:/Studia/IO/MeetSmart/backend/transcryption/plik2.mp3"  # Update this path to the correct location of the audio file
    diarization_file_path = "D:/Studia/IO/MeetSmart/backend/transcryption/plik2_diarization.json"  # Update this path to the correct location of the diarization file
    convert_audio_to_text(audio_file_path, diarization_file_path)