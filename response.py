from openai import OpenAI
import time
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
import requests
import io
from TTS.api import TTS
import wave
import traceback

client = OpenAI(api_key="YOUR-API-KEY")

# Initialize TTS model
tts = TTS(model_name="tts_models/en/ljspeech/vits", gpu=True)

lore = ''
try:
    with open('./lore.txt', 'r', encoding='utf-8') as file:
        lore = file.read()
except Exception:
    print("Error when reading lore.txt")
    print(traceback.format_exc())

# Normalize the lore text by removing newline characters
lore = lore.replace('\n', ' ')

message_log = [{"role": "system", "content": lore}, {"role": "user", "content": lore}]

def generate_response(text):
    print(f"Transcribed Text: {text}")
    global message_log
    ai_response = "I'm sorry, but I couldn't generate a response due to an error."  # Default response in case of error

    # Append user input to message_log
    message_log.append({"role": "user", "content": text})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_log
        )

        # Correct way to extract and process the response text
        ai_response = response.choices[0].message.content.strip().replace('\\n', '\n')

        # Append AI response to message_log correctly
        message_log.append({"role": "assistant", "content": ai_response})

        print(f"GPT: {ai_response}")

    except Exception as e:
        print("Error generating response:", e)
        traceback.print_exc()

    return ai_response


def text_to_speech(ai_response):
    output_path = "output.wav"
    text = ai_response
    tts.tts_to_file(text=text, file_path=output_path, emotion="Happy", speed=2.0)



def PlayAudio():
    VOICE_OUTPUT_FILENAME = "output.wav"
    wf = wave.open(VOICE_OUTPUT_FILENAME, 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    global output_device_id
    # length of data to read.
    chunk = 1024
    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=8)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

    # cleanup stuff.
    wf.close()
    stream.close()
    p.terminate()
