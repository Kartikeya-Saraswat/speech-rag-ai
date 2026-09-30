from app.tts import synthesize_speech


text = (
    "Students at Warwick are assessed through a mix of "
    "worksheets, essays, research reports, modelling and "
    "data analysis, class tests, exams, and presentations."
)

output_path = "data/test_output.wav"

synthesize_speech(
    text=text,
    output_path=output_path,
)

print(f"\nAudio generated: {output_path}")