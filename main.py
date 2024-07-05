"""
    API
"""

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import models

# create the instances of the classes for calling the models
fast_whisper = models.FastWhisperWrapper()
suno = models.SunoWrapper()
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
    return llama3.run(user_prompt, system_prompt=SYSTEM_PROMPT)


@app.post("/atom-ai/")
def atom_ai(user_prompt: UploadFile):
    """
    Llama endpoint
    """
    print("What comes from front")
    print(user_prompt)

    # return {}
    # from speech to text
    output = fast_whisper.run(user_prompt)["text"]["text"]
    # call llama3
    output = llama3.run(output, system_prompt=SYSTEM_PROMPT)["respond"]
    # from text to speech
    output = suno.run_with_speaker_as_string(output)
    # return the final output
    return {"response": output["speech"]}
