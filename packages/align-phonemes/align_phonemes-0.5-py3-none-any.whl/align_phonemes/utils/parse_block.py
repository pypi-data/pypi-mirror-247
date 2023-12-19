import librosa
import soundfile as sf  
import os
import shutil
import fnmatch
import json

def slice_wav_file(input_path, output_path, offset_time, start_time, end_time):
    # Load the WAV file
    audio, sample_rate = librosa.load(input_path, sr=None)

    # Convert the start and end times from seconds to samples
    offset = int(offset_time * sample_rate)
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)
    length_sample = int(end_time * sample_rate)

    # Slice the audio
    sliced_audio = audio[start_sample-offset:end_sample-offset]

    # Save the sliced audio as a new WAV file
    sf.write(output_path, sliced_audio, sample_rate)


def parse_block(sound_path, label_path, trials_dir, verbose=False):
    if (verbose):
        print("PARSING BLOCK")

    #Parse the label file into a list of sentences and start times
    lines = []
    with open(label_path, 'r') as file:
        for line in file.readlines():
            lines.append(line.strip().split(', '))  # Use strip() to remove leading and trailing whitespace
    mike_onset = float(lines[1][1]) 
    mike_offset = float(lines[-1][1])
    sentences = []
    for line in lines[2:-2]:
        sentences.append([line[0], line[1].strip()])

    # Splitting the path and getting the title
    title = os.path.basename(label_path)[:-4].replace(".", "_")

    # Creating the directory paths
    trial_dir = os.path.join(trials_dir, title)
    trial_subdir = os.path.join(trial_dir, "trials")

    # Checking if the directory exists and removing it if it does
    if os.path.exists(trial_dir):
        shutil.rmtree(trial_dir)

    # Creating the directories
    os.makedirs(trial_dir)
    os.makedirs(trial_subdir)


    #Slice Sentences
    for i in range(len(sentences) - 1):
        save_sentence_path = os.path.join(trial_subdir, sentences[i][0].replace(".", "-"))

        start = float(sentences[i][0])
        length = float(sentences[i+1][0]) - start
        slice_wav_file(sound_path, save_sentence_path + ".wav", mike_onset, start, start + length)
        with open(save_sentence_path + ".txt", "w") as f:
            f.write(f"{sentences[i][1]} {sentences[i][1]}")

    #for the last sentence, slice it using the offset
    save_sentence_path = os.path.join(trial_subdir, sentences[-1][0].replace(".", "-"))
    start = float(sentences[-1][0])
    length = mike_offset - start
    slice_wav_file(sound_path, save_sentence_path + ".wav", mike_onset, start, start + length)
    with open(save_sentence_path + ".txt", "w") as f:
        f.write(f"{sentences[-1][1]} {sentences[-1][1]}")

    #write the transcription method json
    transcription_method_path = os.path.join(trial_dir, "transcription_method.json")
    transcription_method_dict = {}
    for sentence in sentences:
        transcription_method_dict[sentence[0]] = "original"
    with open(transcription_method_path, "w") as f:
        json.dump(transcription_method_dict, f, indent=4)

    if (verbose):
        print("PARSING COMPLETE")

    return trial_dir



# def duplicate_sentence_strings(label_path):
#     #parse the file for information
#     lines = []
#     with open(label_path, 'r') as file:
#         for line in file:
#             lines.append(line.strip().split(', '))  # Use strip() to remove leading and trailing whitespace
        
#     sentences = [(line[0], line[1]) for line in lines[2:-2]]
#     with open(label_path, 'w') as file:
#         file.write("mike-on times\n")
#         file.write(lines[1][0] + ", " + lines[1][1] + "\n")

#         for sentence in sentences:
#             file.write(f"{sentence[0]}, {sentence[1]}, {sentence[1]}\n")

#         file.write("mike-off times\n")
#         file.write(lines[-1][0] + ", " + lines[-1][1] + "\n")

# def find_txt_files(directory):
#     wav_files = []

#     for root, _, files in os.walk(directory):
#         for file in files:
#             if fnmatch.fnmatch(file, '*.txt'):
#                 # Add the full path of the matching file to the list
#                 wav_files.append(os.path.join(root, file))

#     return wav_files

# label_files = find_txt_files(r"C:\makin_temp_repo\align_phonemes\data\human_data\speech")
# for file in label_files:
#     duplicate_sentence_strings(file)

#################### SLICE UP ONE BLOCK #########################################################
# path = r"C:\makin_temp_repo\align_phonemes\data\human_data\speech\speech_results_Aug_19_16.52.44"
# audio_path = path + ".wav"
# label_path = path + ".txt"
# slice_human_data(audio_path, label_path)


#################### GET ONE SLICE OF AN AUDIO FILE #########################################################
# offset = 17.011275900003966 #(16.998701000004075 + 17.011275900003966) / 2.0
# start = 71.156168800021987
# length = 3.0
# source_path = r"C:\makin_temp_repo\align_phonemes\data\human_data\speech\speech_results_Aug_18_15.45.59.wav"
# save_path = r"C:\makin_temp_repo\align_phonemes\data\human_data\cut_speech\cut2.wav"

# slice_wav_file(source_path, save_path, offset, start, length)