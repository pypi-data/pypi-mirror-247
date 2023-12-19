import librosa
import numpy as np
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

def get_transcription(mic_data, sr=16000):
    
    target_sr = 16000
    if sr != target_sr:
        mic_data = librosa.resample(np.float32(mic_data), orig_sr=sr, target_sr = 16000)
        
    model_name = "facebook/wav2vec2-large-960h-lv60-self"
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    
    input_values = processor(mic_data, sampling_rate = target_sr,
                             return_tensors="pt").input_values.to(torch.float32)
    
    # Normalize: Gave better accuracy
    input_values = (input_values - input_values.mean())/input_values.std()
    
    with torch.no_grad():
        logits = model(input_values).logits
        
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    
    return transcription