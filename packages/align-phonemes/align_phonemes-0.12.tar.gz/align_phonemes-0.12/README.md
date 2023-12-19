# Phoneme Forced Aligner

This package was designed to intake human data from Makin Lab (.txt and .wav file from the block needed phoneme alignment) and ouput a JSON file with the mike-on and mike-off times and the alignments (start time, transcription method, production 1, phoneme list 1, production 2, phoneme list 2).

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes.

### Installing

This is a pip installable package. Therefore, run the following command:
____________________________________________________

## Functions

### get_forced_aligment()
  input: block txt path, block wav path, output transcription json path, transcription method, critical error threshold, verbose
  functionality: 
    - determine which transcript will be used based on transcription method input (Critical Error, Wav2Vec, Original)
    - run Montreal Forced aligner (input trials directory and verbose and returns text grid)
    - demarcate JSON
    - clean directories
   ____________________________________________________
    
### demarcate_to_json()
  input: trial directory, block path, text grid directory, output json file path
  functionality: 
  - read textgrid 
  - use ER-demarcation Algorithm to denote phoneme split
  - use ER-demarcation to denote transcript split
  - write to Phoneme Json (see output format)
  ____________________________________________________
  
### clean_directories()
  input: list of temp directories created
  functionality: clean and remove directory
  ____________________________________________________
  
### parse_block()
  input: wav file path, txt file path, trials directory, verbose
  functionality: 
  - create a Trial Directory (same name as the label): each trial is a .wav and a .txt
  - Trial Directory:
	Trials dir:
		trial.wav
		trial.txt
		...
	Trial transcription method .json

  TranscriptionMethod.json format:
  {
    trial start-time (float): method ('wav2vec' or 'original'),
    ...
  }
  ____________________________________________________
  
## Notes
For a more in depth explanation in the methods used in this package, as well as the reasoning behind, refer back to the paper.

## Authors

  - **James Willian Stonebridge** 
  - **Herbert Alexander de Bruyn**
  - **Tyler Dierckman**

## License

This project is licensed under the MIT License.

## Acknowledgments

  - Varun implemented the original code for Wav2Vec2 based transcription used in this package.
