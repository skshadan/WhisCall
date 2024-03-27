
![Logo](https://github.com/skshadan/WhisCall/blob/main/images/logo.png?raw=true)
# WhisCall
A framework for AI WhatsApp calls using Whisper, Coqui TTS, GPT-3.5 Turbo, Virtual Audio Cable, and the WhatsApp Desktop App.

https://github.com/skshadan/WhisCall/assets/118248053/e882d09b-c058-4f61-b6d9-626839205595

## Tools used in this framework
- Whisper (Speech to Text)
- OpenAI GPT 3.5 Turbo
- Coqui TTS
- Virtual Audio Cable
- WhatsApp Desktop App


## Installation

### Install Build Tools from Visual Studio 2022

[Download Visual Studio Installer](https://visualstudio.microsoft.com/downloads/)

![App Screenshot](https://github.com/skshadan/WhisCall/blob/main/images/build%20tools.png?raw=true)

### Install CUDA Toolkit 12.4

[Download CUDA Toolkit 12.4](https://developer.nvidia.com/cuda-downloads)

![App Screenshot](https://github.com/skshadan/WhisCall/blob/main/images/cuda.png?raw=true)

### Install Espeak

[Download Espeak from here](http://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/setup_espeak-1.48.04.exe)

![App Screenshot](https://github.com/skshadan/WhisCall/blob/main/images/espeak.png?raw=true)

### Install VB-Audio Cable

Note: You need two separate Virtual Audio Cables. I am using VB Audio Cable and (VAC) Virtual Audio Cable. Install both.

- [Download VB-Audio Cable](https://vb-audio.com/Cable/)

- [Download VAC](https://vac.muzychenko.net/en/download.htm)

![App Screenshot](https://github.com/skshadan/WhisCall/blob/main/images/vb-audio.png?raw=true)

### Install Whatsapp Desktop Version

[Download Whatsapp](ms-windows-store://pdp/?productid=9NKSQGP7F2NH&mode=mini&cid=sideload_experiment_control)


![App Screenshot](https://github.com/skshadan/WhisCall/blob/main/images/whatsapp.png?raw=true)









    
## Now Clone the Repo

```bash
  https://github.com/skshadan/WhisCall.git
```
```bash
  pip install -r requirements.txt
```


### Find Speaker And Microphone Index

Run the below code to find the index of your virtual audio cable for the microphone and speaker.

```python
import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    # Lists of devices to return
    speakers = []
    microphones = []

    # Scan through devices and add to list
    for i in range(0, num_devices):
        device = p.get_device_info_by_index(i)
        if device.get('maxInputChannels') > 0:
            microphones.append((i, device.get('name')))
        if device.get('maxOutputChannels') > 0:
            speakers.append((i, device.get('name')))

    p.terminate()
    return microphones, speakers

microphones, speakers = list_audio_devices()

print("Microphones:")
for idx, name in microphones:
    print(f"Index: {idx}, Name: {name}")

print("\nSpeakers:")
for idx, name in speakers:
    print(f"Index: {idx}, Name: {name}")

```

## Select Input & Output for Microphone and Speaker in WhatsApp App

![App Screenshot](https://github.com/skshadan/WhisCall/blob/main/images/input%20and%20output.png?raw=true)

##  Run the code
## main.py


```python
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
```

## Select the Microphone Index. The TTS & Whisper will load, and that's it!!!
![App Screenshot](https://github.com/skshadan/WhisCall/blob/main/images/run%20the%20code.png?raw=true)

If you want different voices, you need to change the TTS model as follows:

Download Models From Here:
- https://huggingface.co/sk0032
- https://huggingface.co/youmebangbang/vits_tts_models/tree/main




## Facing Any Issues?

Feel free to ask if you are having any issues. Also, feel free to contribute.


## fin.

