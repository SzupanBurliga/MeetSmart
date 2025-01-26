from pathlib import Path
from pyannote.audio import Pipeline
import os
import json

def load_pipeline_from_pretrained(path_to_config: str | Path) -> Pipeline:
    path_to_config = Path(path_to_config)

    print(f"Loading pyannote pipeline from {path_to_config}...")

    cwd = Path.cwd().resolve()

    cd_to = path_to_config.parent.resolve()

    print(f"Expected directory to change to: {cd_to}")
    if not cd_to.exists():
        raise FileNotFoundError(f"Directory does not exist: {cd_to}")

    print(f"Changing working directory to {cd_to}")
    os.chdir(cd_to)

    pipeline = Pipeline.from_pretrained(path_to_config)

    print(f"Changing working directory back to {cwd}")
    os.chdir(cwd)

    return pipeline

PATH_TO_CONFIG = os.path.abspath("models/pyannote_diarization_config.yaml")
pipeline = load_pipeline_from_pretrained(PATH_TO_CONFIG)


def diarize_audio(wav_file_path):
    diarization = pipeline(wav_file_path)

    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        results.append({
            "speaker": speaker,
            "start_time": f"{turn.start:.1f}s",
            "end_time": f"{turn.end:.1f}s"
        })
    
    # Save results to a text file
    output_dir = '../outputs'
    os.makedirs(output_dir, exist_ok=True)
    diarization_file_path = os.path.join(output_dir, wav_file_path.rsplit('.', 1)[0] + '_diarization.json')
    with open(diarization_file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Diarization results saved to {diarization_file_path}")
    return results

# if __name__ == "__main__":
#     audio_file_path = "../outputs/output_audio.mp3"  # Update this path to the correct location of the audio file
#     diarize_audio(audio_file_path)