import noisereduce as nr
import librosa
import numpy as np

def preprocess_audio(file_path):
    # Load audio
    audio, sr = librosa.load(file_path, sr=16000)

    # Noise reduction
    reduced = nr.reduce_noise(y=audio, sr=sr)

    # Normalize
    normalized = reduced / np.max(np.abs(reduced))

    return normalized, sr