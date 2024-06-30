"""
    API
"""

from fastapi import FastAPI, UploadFile

import models

# create the instances of the classes for calling the models
fast_whisper = models.FastWhisperWrapper()
suno = models.SunoWrapper()
llama3 = models.Llama3Wrapper()
app = FastAPI()


@app.post("/whisper/")
def whisper_model(sound_file: UploadFile):
    """
    Whisper endpoint
    """
    return fast_whisper.run(sound_file)

#Revisar y probar
@app.post("/suno/") 
def suno_model(text_to_speech: str):
    """
    suno endpoint
    """
    return suno.run(text_to_speech)


@app.post("/llama/")
def llama_model(user_prompt: str):
    """
    Llama endpoint
    """
    return llama3.run(user_prompt)

#Revisar y probar
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
    output = suno.run_with_speaker_as_string(output)
    # return the final output
    return {"respond": output["speech"]}
