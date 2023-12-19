import src.funcs as f
import pandas as pd
import numpy as np
from pydub import AudioSegment
from jiwer import cer

class Evaluate_Model():
    def __init__(self, wav, txt):
        self.txt_expected = txt
        self.audio = AudioSegment.from_wav(wav)
        self.char_error_rate = []

    def splice_audio(self):
        self.spliced_audio = []
        times = np.array(self.df.Time)

        for i, s in enumerate(times):
            start = s * 1000    #millisecond
            end = start + self.offset * 1000
           # print(start, end)
            audio_seg = self.audio[start:end]
            #audio_seg.export(f'spliced_audio/chunk{i}', format='wav')
            self.spliced_audio.append(audio_seg)
        #print(self.spliced_audio)

    def parse_txt(self):
        self.df = pd.read_csv(self.txt_expected, sep=',', header=None, names=['Time', 'TXT'], skiprows=1)
    
        try:
            self.df = self.df.iloc[range(0, self.df[self.df['Time'] == 'mike-off times'].index[0])]
            self.df['Time'] = pd.to_numeric(self.df['Time'])
            on = self.df.iloc[0]
            #print(on)
            self.df.drop(index=self.df.index[0], axis=0, inplace=True)
            self.df['Time'] = self.df['Time'] - (on['Time'] + pd.to_numeric(on['TXT']))/2
            #print(self.df)
        except:
            print("TXT files contain unexpected formatting")
        trials_time = self.df['Time']
        trials_time = trials_time.diff()
        metrics = {'Mean': trials_time.mean(), 'Std': trials_time.std(), 'Var': trials_time.var()}
        self.trial_length = metrics['Mean']
        self.offset = round(metrics['Mean'] / 3)
       # print(self.offset)
        if metrics['Var'] >= 0.1:
            print("Warning: variance of the trials length is high (>= 0.1)")

    def evaluate_transcript(self):
        file = open('transcripts', 'w')
        transcripts = []
        for index, chunk in enumerate(self.spliced_audio):
            #print(chunk)
            samples = chunk.get_array_of_samples()
            #print(samples)
            samples = np.array(samples).astype(np.float32)/32768 # 16 bit
            #print(self.df['TXT'].loc[index])
            try:
                transcript = f.get_transcription(samples, sr=chunk.frame_rate)
            except Exception as err:
                print(f"Could not proceed running the model in {index} due to: ", err)
                break
            else:
                self.char_error_rate.append( cer(self.df['TXT'].loc[index + 1], transcript))
                # print(transcript)
                transcripts.append(transcript + '\n')
            
        self.avg_error = sum(self.char_error_rate)/len(self.char_error_rate)
        print("Character Error Rate", self.avg_error)
        file.writelines(transcripts)
        file.close()
        
    def evaluate_phonemes(self):
        file = open('phoneme_alignment.txt', 'w')
        alignment = []
        for index, chunk in enumerate(self.spliced_audio):
            samples = chunk.get_array_of_samples()
            samples = np.array(samples).astype(np.float32)/32768 # 16 bit
            try:
                phonemes = f.get_phoneme_alignments(samples, sr=chunk.frame_rate)
            except Exception as err:
                print(f"Could not run model for test {index} due to {err}")
            else:
                alignment.append(phonemes)
        file.writelines(alignment)
        file.close()
