import os

from .utils.parse_block import parse_block
from .src.apply_transcriptions import apply_critical_error_transcriptions, apply_wav2vec_transcriptions
from .utils.run_mfa import run_mfa
from .utils.demarcate_to_json import demarcate_to_json
from .utils.clean_directories import clean_directories

def get_forced_alignments(block_label_path, block_wav_path, output_transcription_json_path, transcription_method="Critical_Error", Critical_Error=0.3, verbose=False, clean_trials=True):
    # Get the trials directory location 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    trials_directory = os.path.join(current_dir, "trials")

    trial_directory = parse_block(block_wav_path, block_label_path, trials_directory, verbose=verbose)

    if (transcription_method == "Critical_Error"):
        apply_critical_error_transcriptions(trial_directory, Critical_Error, verbose=verbose)
    elif (transcription_method == "Wav2Vec"):
        apply_wav2vec_transcriptions(trial_directory, verbose=verbose)
    elif (transcription_method != "Original"):
        raise Exception("Invalid transcription method.\n Valid Options: (Critical_Error, Wav2Vec, Original)")
    
    textgrid_directory = run_mfa(trial_directory, verbose=verbose)
    
    demarcate_to_json(trial_directory, block_label_path, textgrid_directory, output_transcription_json_path)
    # demarcate_to_json("C:\makin_temp_repo\\align_phonemes\\trials\speech_results_Aug_18_15_45_59", block_label_path,
    #                   "C:\makin_temp_repo\\align_phonemes\\trials\speech_results_Aug_18_15_45_59\\textgrids", output_transcription_json_path)

    if clean_trials:
        clean_directories([trial_directory])


if __name__ == "__main__":
    block_label_path = "C:\makin_temp_repo\original_dataset\speech_results_Aug_18_15.45.59.txt"
    block_wav_path = "C:\makin_temp_repo\original_dataset\speech_results_Aug_18_15.45.59.wav"
    output_transcription_json_path = "C:\\makin_temp_repo\\phoneme.json"  
    print(get_forced_alignments(block_label_path, block_wav_path, output_transcription_json_path, transcription_method="Critical_Error", verbose=True))
