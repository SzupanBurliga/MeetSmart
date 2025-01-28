import transcryption.speechtotext as speechtotext
import transcryption.speakerDiarization as speakerDiarization

def transcribe_audio(input_audio, output_file):
    speakerDiarization.diarize_audio(input_audio)
    speechtotext.convert_audio_to_text(input_audio, output_file)

#transcribe_audio("outputs/output_audio.mp3", "outputs/transcription_with_diarization.txt")