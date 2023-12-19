import os
import json
import jiwer
import string


def find_textgrid_files(directory):
    textgrid_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".TextGrid"):
                textgrid_files.append(os.path.join(root, file))

    return textgrid_files


def extract_mike_times(file_path):
    with open(file_path, 'r') as file:
        print(file_path)
        lines = file.readlines()

        mike_on_index = lines.index("mike-on times\n") + 1
        mike_on_times = [float(num) for num in lines[mike_on_index].split(',')]

        mike_off_index = lines.index("mike-off times\n") + 1
        mike_off_times = [float(num) for num in lines[mike_off_index].split(',')]

    return mike_on_times, mike_off_times


def initialize_json(block_label_path, json_path):
    mike_on_times, mike_off_times = extract_mike_times(block_label_path)

    alignment_data = {
        "mike-on times": [],
        "mike-off times": [],
        "alignments": []
    }

    alignment_data["mike-on times"].extend(mike_on_times)
    alignment_data["mike-off times"].extend(mike_off_times)

    with open(json_path, 'w') as json_file:
        json.dump(alignment_data, json_file, indent=4)


def extract_phones_from_textgrid(textgrid_path):
    try:
        with open(textgrid_path, 'r') as file:
            lines = file.readlines()

        phones_tier_index = lines.index('    item [2]:\n')

        phone_intervals = []
        for line in lines[phones_tier_index + 5:]:
            if line.startswith('            xmin'):
                xmin = float(line.split('=')[1].strip())
            elif line.startswith('            xmax'):
                xmax = float(line.split('=')[1].strip())
            elif line.startswith('            text'):
                text = line.split('=')[1].strip().strip('"')
                phone_intervals.append((xmin, xmax, text))

        return phone_intervals

    except Exception as e:
        print(f"Error: {e}")
        return None


def clean_phones(phone_intervals):
    cleaned_phones = []

    for xmin, xmax, text in phone_intervals:
        cleaned_text = text.rstrip('012')
        cleaned_text = "[SIL]" if cleaned_text == "" else cleaned_text
        cleaned_phones.append((xmin, xmax, cleaned_text))

    return cleaned_phones


def get_transcript_word_list(transcript_file):
    try:
        with open(transcript_file, 'r', encoding='utf-8') as file:
            sentence = file.readline().strip()

            translator = str.maketrans("", "", string.punctuation)
            processed_sentence = sentence.translate(translator).lower()

            word_list = processed_sentence.split()

            return word_list

    except Exception as e:
        print(f"Error: {e}")

        return None


def find_split_index(input_list):
    lowest_wer = 1
    best_index = 0

    for index in range(len(input_list)):

        first_half = ' '.join(input_list[:index])
        second_half = ' '.join(input_list[index:])

        if first_half and second_half:
            test_wer = jiwer.wer(first_half, second_half)

            if test_wer < lowest_wer:
                lowest_wer = test_wer
                best_index = index

    return best_index, lowest_wer


def append_trial_to_json(json_path, base_filename, cleaned_phone_interval_list, phones_split_index,
                         transcript_word_list, words_split_index, sentence_method):
    first_sentence_words = ' '.join(transcript_word_list[:words_split_index])
    second_sentence_words = ' '.join(transcript_word_list[words_split_index:])

    first_sentence_phonemes = cleaned_phone_interval_list[:phones_split_index]
    second_sentence_phonemes = cleaned_phone_interval_list[phones_split_index:]

    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        new_alignment = {
            base_filename: {
                "used sentence method": sentence_method,
                "used-sentence 1": first_sentence_words,
                "phoneme list 1": first_sentence_phonemes,
                "used-sentence 2": second_sentence_words,
                "phoneme list 2": second_sentence_phonemes
            }
        }

        data["alignments"].append(new_alignment)

        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return True

    except Exception as e:
        print(f"Error appending alignment: {e}")
        return False


def get_sentence_method():
    pass


def demarcate_to_json(trial_directory, block_label_path, textgrid_directory, json_path):
    transcript_directory = os.path.join(trial_directory, "trials")
    textgrid_directory = os.path.join(trial_directory, "textgrids")
    method_json = os.path.join(trial_directory, "transcription_method.json")
    methods_by_filename = {}
    with open(method_json, "r") as f:
        methods_by_filename = json.load(f)

    initialize_json(block_label_path, json_path)

    textgrid_file_list = find_textgrid_files(textgrid_directory)

    for textgrid_file in textgrid_file_list:
        base_filename = os.path.splitext(os.path.basename(textgrid_file))[0]
        transcript_file = os.path.join(transcript_directory, base_filename + ".txt")

        if not os.path.exists(transcript_file):
            print(textgrid_file + " contains no corresponding .txt file in " + transcript_directory)

        else:
            cleaned_phone_interval_list = clean_phones(extract_phones_from_textgrid(textgrid_file))
            transcript_word_list = get_transcript_word_list(transcript_file)

            phone_list = [phone_interval[2] for phone_interval in cleaned_phone_interval_list]

            phones_split_index, phones_split_wer = find_split_index(phone_list)
            words_split_index, words_split_wer = find_split_index(transcript_word_list)

            sentence_method = methods_by_filename[base_filename.replace("-", ".")]

            append_trial_to_json(json_path, base_filename, cleaned_phone_interval_list, phones_split_index,
                                 transcript_word_list, words_split_index, sentence_method)
    
    return json_path