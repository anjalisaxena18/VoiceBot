from groq import Groq
from dotenv import load_dotenv
import os
from litellm import completion, speech
import litellm

load_dotenv()

client= Groq()
api_key = os.environ['GROQ_API_KEY']

def stt(audio_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=audio_file,
        prompt="Specify context or spelling accurately"
    )

    transcript_text = transcript.text
    print("text", transcript_text)

    response = completion(
        model="groq/llama-3.1-8b-instant", 
        messages=[
            {"role": "user", "content": transcript_text}
        ],
        stream=True
    )
    full_response = ""
    for chunk in response:
        content_part = chunk["choices"][0]["delta"].get("content", "")
        # print(content_part, end="", flush=True)
        full_response += content_part

    print("Content Part is ", content_part)
    return content_part

def tts(chunk):
    print("tts loading")

    if not isinstance(text, str):
        raise ValueError("TTS input must be a string")

    tts = litellm.speech(
        model = "groq/playai-tts",
        voice = "Arista-PlayAI",
        input = chunk,
        api_key = api_key,
        response_format = "wav",
        speech_file_path = "speech.wav"
    )

def voice(audio_file):
    text = stt(audio_file)
    output = tts(text)
    return (f"Output saved as speech.wav : {output}")

if __name__ == "__main__":
    audio_file = open("audio_test.mp3", "rb")
    print(f"{voice(audio_file)}")