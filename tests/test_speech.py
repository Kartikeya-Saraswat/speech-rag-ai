from app.speech import transcribe_audio


audio_path = "data/test_audio.wav"

text = transcribe_audio(audio_path)

print("\n--- TRANSCRIPTION ---\n")
print(text)