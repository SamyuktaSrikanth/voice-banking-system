import whisper

model = whisper.load_model("base")  # small for faster demo

def speech_to_text(audio_path):
    result = model.transcribe(audio_path)

    text = result["text"]
    language = result["language"]

    return text, language