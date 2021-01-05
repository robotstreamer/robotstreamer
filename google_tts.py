from google.cloud import texttospeech
import os
import argparse

#parser.add_argument('--cred', help='google application credentials json file', default="/home/pi/google_app_cred.json")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/google_app_cred.json"

def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

def text_to_wav(voice_name, text):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = f"/tmp/tts.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')



def speak(message, audioOutputNumber):
    text_to_wav("en-US-Wavenet-D", message)
    os.system("ffmpeg -y -i /tmp/tts.wav -ac 2 -ar 48000 /tmp/tts2.wav;aplay /tmp/tts2.wav --device=hw:%d,0" % audioOutputNumber)

#list_voices()


if __name__ == "__main__":
    # execute only if run as a script
    speak("hello I am a robot", 1)
