import numpy as np
import torch
import whisper
import speech_recognition as sr
from datetime import datetime, timedelta
from queue import Queue
from time import sleep

def is_audio_loud_enough(audio_data, volume_threshold=1000):
    """Determines if the audio data's volume exceeds a specified threshold."""
    volume = np.sqrt(np.mean(np.square(np.frombuffer(audio_data, dtype=np.int16).astype(np.float32))))
    return volume > volume_threshold

def select_microphone():
    """Prompts the user to select a microphone by listing all available microphones."""
    print("Available microphone devices:")
    mic_list = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mic_list):
        print(f"{index}: {name}")
    mic_index = int(input("Select a microphone by index: "))
    return mic_index

def transcribe_audio(mic_index):
    """Transcribes audio from the specified microphone index."""
    # Settings
    energy_threshold = 3000  # Adjust this based on your ambient noise
    record_timeout = 5  # Maximum seconds to record after recognizing speech
    phrase_timeout = 5  # Timeout to wait for speech to complete
    model_name = "medium.en"  # Whisper model variant

    # Initialize
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = energy_threshold
    recorder.dynamic_energy_threshold = True  # Enable dynamic adjustment to ambient noise
    source = sr.Microphone(sample_rate=16000, device_index=mic_index)
    audio_model = whisper.load_model(model_name)

    with source:
        recorder.adjust_for_ambient_noise(source, duration=1)  # Optional: adjust duration for ambient noise adjustment

    def record_callback(recognizer, audio):
        """Callback function to capture audio data and check if it's loud enough before queuing."""
        data = audio.get_raw_data()
        if is_audio_loud_enough(data):
            data_queue.put(data)

    # Start listening in the background
    stop_listening = recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    print("Transcription service started. Press Ctrl+C to stop.")

    try:
        while True:
            if not data_queue.empty():
                audio_data = b''.join(list(data_queue.queue))
                data_queue.queue.clear()

                # Convert raw data to numpy array for Whisper
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                # Basic post-processing to filter out unintended phrases
                if text and not text.lower() in ["thank you", "unwanted phrase"]:
                    yield text  # Yield text for further processing instead of printing

            sleep(0.1)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("\nTranscription service stopped.")
        stop_listening() 
