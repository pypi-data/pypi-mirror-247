import json
from scipy.io import wavfile
import numpy as np
from jiwer import wer
import os

from ..utils.find_files import find_wav_files, find_label_files
from .wav2vec import get_transcription

def apply_wav2vec_transcriptions(trial_directory, verbose=False):
    if (verbose):
        print("APPLYING TRANSCRIPTIONS")

    label_paths = sorted(find_label_files(trial_directory))
    wav_paths = sorted(find_wav_files(trial_directory))
    transcription_methods = {}
    with open(os.path.join(trial_directory, "transcription_method.json"), "r") as f:
        json_string = f.read()
        transcription_methods = json.loads(json_string)

    for wav_path, label_path in zip(wav_paths, label_paths):
        original_transcript = ""
        with open(label_path, "r") as f:
            original_transcript = f.readline()

        samplerate, data = wavfile.read(wav_path)
        data = data.astype(np.float32)
        wav2vec_transcript = get_transcription(data, sr=samplerate).lower()

        start_time = os.path.basename(label_path)[:-4].replace("-", ".")
        transcription_methods[start_time] = "wav2vec"

        with open(label_path, "w") as f:
            f.write(wav2vec_transcript)
        
    with open(os.path.join(trial_directory, "transcription_method.json"), "w") as f:
        json.dump(transcription_methods, f, indent=4)
    
    if (verbose):
        print("TRANSCRIPTIONS APPLIED")


def apply_critical_error_transcriptions(trial_directory, critical_error, verbose=False):
    if (verbose):
        print("APPLYING TRANSCRIPTIONS")

    label_paths = sorted(find_label_files(trial_directory))
    wav_paths = sorted(find_wav_files(trial_directory))
    transcription_methods = {}
    
    with open(os.path.join(trial_directory, "transcription_method.json"), "r") as f:
        json_string = f.read()
        transcription_methods = json.loads(json_string)

    for wav_path, label_path in zip(wav_paths, label_paths):
        original_transcript = ""
        with open(label_path, "r") as f:
            original_transcript = f.readline()

        samplerate, data = wavfile.read(wav_path)
        data = data.astype(np.float32)
        wav2vec_transcript = get_transcription(data, sr=samplerate).lower()

        if wer(wav2vec_transcript, original_transcript) > critical_error:
            start_time = os.path.basename(label_path)[:-4].replace("-", ".")
            print(label_path)
            print(start_time)
            print(transcription_methods[start_time])
            transcription_methods[start_time] = "wav2vec"

            with open(label_path, "w") as f:
                f.write(wav2vec_transcript)
        
    with open(os.path.join(trial_directory, "transcription_method.json"), "w") as f:
        json.dump(transcription_methods, f, indent=4)
    
    if (verbose):
        print("TRANSCRIPTIONS APPLIED")
        


        