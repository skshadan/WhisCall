from voice import select_microphone, transcribe_audio
from response import generate_response, text_to_speech, PlayAudio

def main():
    mic_index = select_microphone()
    for text in transcribe_audio(mic_index):
        if text:
            gpt_response = generate_response(text)
            text_to_speech(gpt_response) 
            PlayAudio()


if __name__ == "__main__":
    main()
