from align_phonemes import get_forced_alignments

if __name__ == "__main__":
    block_label_path = "C:\makin_temp_repo\original_dataset\speech_results_Aug_18_15.45.59.txt"
    block_wav_path = "C:\makin_temp_repo\original_dataset\speech_results_Aug_18_15.45.59.wav"
    output_transcription_json_path = "C:\\makin_temp_repo\\phoneme.json"  
    get_forced_alignments(block_label_path, block_wav_path, output_transcription_json_path,
                           transcription_method="Original", verbose=True, clean_trials=False)