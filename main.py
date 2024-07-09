"""
    API
"""

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import models

# create the instances of the classes for calling the models
fast_whisper = models.FastWhisperWrapper()
xtts = models.XttsWrapper()
llama3 = models.Llama3Wrapper()

# system prompt fot llama3
SYSTEM_PROMPT = """
                Please respond like a english teacher, but keep the responses simple and short please. 
                Please if i speak to you in another language different than english try to make me speak to you in english.
                If i try to speak about something politically inappropriate try to change the subject.
                """

app = FastAPI()

# CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/whisper/")
def whisper_model(sound_file: UploadFile):
    """
    Whisper endpoint
    """
    return fast_whisper.run(sound_file)


@app.post("/xtts/")
def xtts_model(sound_file: UploadFile, text_to_speech: str):
    """
    Xtts endpoint
    """
    return xtts.run(sound_file, text_to_speech)


@app.post("/xtts-sample-speaker/")
def xtts_model_width_sample_speaker(text_to_speech: str):
    """
    Xtts endpoint with sample speaker
    """
    return xtts.run_with_sample_speaker(text_to_speech)


@app.post("/llama/")
def llama_model(user_prompt: str):
    """
    Llama endpoint
    """
    return llama3.run(user_prompt, system_prompt=SYSTEM_PROMPT)


@app.post("/atom-ai/custom-voice/")
def atom_ai_custom_voice(user_prompt: UploadFile):
    """
    Llama endpoint
    """
    print("What comes from front")
    print(user_prompt)

    # from speech to text
    input_text = fast_whisper.run(user_prompt)["text"]["text"]
    # call llama3
    text_output = llama3.run(input_text, system_prompt=SYSTEM_PROMPT)["respond"]
    # from text to speech
    audio_output = xtts.run_with_custom_speaker("MorganSpeaker2.mp3", text_output)
    # return the final output
    return {
        "input_text": input_text,
        "response_text": text_output,
        "speech_url": audio_output["speech"],
    }


@app.post("/atom-ai/sample-voice/")
def atom_ai_sample_voice(user_prompt: UploadFile):
    """
    Llama endpoint
    """
    print("What comes from front")
    print(user_prompt)

    # from speech to text
    input_text = fast_whisper.run(user_prompt)["text"]["text"]
    # call llama3
    text_output = llama3.run(input_text, system_prompt=SYSTEM_PROMPT)["respond"]
    # from text to speech
    audio_output = xtts.run_with_sample_speaker(text_output)
    # return the final output
    return {
        "input_text": input_text,
        "response_text": text_output,
        "speech_url": audio_output["speech"],
    }
