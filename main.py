from groq import Groq
from dotenv import load_dotenv
import os
from litellm import speech
import litellm
from google import genai
from google.genai import types

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
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a cat question-answering bot. Answer to the user's message precisely and politely."),
            contents=transcript_text,
            max_tokens = 100
        )
        return response.text
    except Exception as e:
        return ("error",e)

def tts(text): 
    print("tts loading")

    if not isinstance(text, str):
        raise ValueError("TTS input must be a string")

    tts = litellm.speech(
        model = "groq/playai-tts",
        voice = "Arista-PlayAI",
        input = text,
        api_key = api_key,
        response_format = "wav",
        speech_file_path = "speech.wav"
    )

    return {"speech.wav", text}

def voice(audio_file):
    text = stt(audio_file)
    output = tts(text)
    return (f"Output saved as speech.wav : {output}")

if __name__ == "__main__":
    audio_file = open("audio_test.mp3", "rb")
    print(f"{voice(audio_file)}") 