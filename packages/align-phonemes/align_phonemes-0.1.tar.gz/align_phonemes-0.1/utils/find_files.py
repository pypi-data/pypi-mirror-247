import os
import fnmatch
import librosa

def find_files(directory, regex):
    matching_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, regex):
                # Add the full path of the matching file to the list
                matching_files.append(os.path.join(root, file))

    return matching_files


def find_total_wer_files(directory):
    return find_files(directory, '*TOTAL_WER.txt')
    

def find_wav_files(directory):
    return find_files(directory, '*.wav')

def find_label_files(directory):
    return find_files(directory, '*-*.txt')
