import groq
import os
from config import GROQ_API_KEY, WHISPER_MODEL


client = groq.Groq(api_key=GROQ_API_KEY)

def transcribe_audio(audio_file_path):
    """
    Takes an audio file path and returns transcribed text.
    """
    try:
        
        with open(audio_file_path, "rb") as audio_file:
            
            
            transcription = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
                response_format="text"
            )
        
        return transcription
    
    except Exception as e:
        return f"Error in transcription: {str(e)}"


def save_recorded_audio(audio_data, sample_rate=44100):
    """
    Saves recorded microphone audio to a temporary wav file.
    """
    try:
        import scipy.io.wavfile as wav
        import numpy as np
        
        temp_path = "temp_audio.wav"
        
        
        audio_array = np.array(audio_data, dtype=np.int16)
        
        
        wav.write(temp_path, sample_rate, audio_array)
        
        return temp_path
    
    except Exception as e:
        return f"Error saving audio: {str(e)}"