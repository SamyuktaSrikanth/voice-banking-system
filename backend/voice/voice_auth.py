import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.spatial.distance import cosine
from pydub import AudioSegment

encoder = VoiceEncoder()

# Convert audio → embedding
def get_embedding(audio_path):
    # Convert webm → wav
    if audio_path.endswith(".webm"):
        wav_path = audio_path.replace(".webm", ".wav")
        
        audio = AudioSegment.from_file(audio_path, format="webm")
        audio.export(wav_path, format="wav")
        
        audio_path = wav_path  # use converted file

    wav = preprocess_wav(audio_path)
    embedding = encoder.embed_utterance(wav)
    return embedding

# Compare embeddings
def compare_embeddings(emb1, emb2, threshold=0.5):
    similarity = 1 - cosine(emb1, emb2)
    return similarity > threshold, similarity

# Convert embedding → bytes (store in DB)
def embedding_to_bytes(embedding):
    return embedding.tobytes()

# Convert bytes → embedding
def bytes_to_embedding(byte_data):
    return np.frombuffer(byte_data, dtype=np.float32)