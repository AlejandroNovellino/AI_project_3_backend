"""
    API
"""

from fastapi import FastAPI, UploadFile

import models

# create the instances of the classes for calling the models
fast_whisper = models.FastWhisperWrapper()
xtts = models.XttsWrapper()
llama3 = models.Llama3Wrapper()

app = FastAPI()


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


@app.post("/llama/")
def llama_model(user_prompt: str):
    """
    Llama endpoint
    """
    return llama3.run(user_prompt)


@app.post("/vita-ai/")
def vita_ai(user_prompt: UploadFile):
    """
    Llama endpoint
    """
    # from speech to text
    output = fast_whisper.run(user_prompt)["text"]["text"]
    # call llama3
    output = llama3.run(output)["respond"]
    # from text to speech
    output = xtts.run_with_speaker_as_string("ScarlettSpeaker2.mp3", output)
    # return the final output
    return {"respond": output["speech"]}
