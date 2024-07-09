"""
    API
"""

from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import models
import os

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
''''
#Revisar y probar
@app.post("/suno/") 
def suno_model(text_to_speech: str):
    """
    suno endpoint
    """
    return suno.run(text_to_speech)
'''

@app.post("/suno/")
def suno_model(text_to_speech: str, request: Request):
    result = suno.run(text_to_speech)
    base_url = str(request.base_url)
    full_url = f"{base_url.rstrip('/')}{result['speech']}"
    return {"speech": full_url}


@app.post("/llama/")
def llama_model(user_prompt: str):
    """
    Llama endpoint
    """
    return llama3.run(user_prompt, system_prompt=SYSTEM_PROMPT)


@app.post("/atom-ai/")
def atom_ai(user_prompt: UploadFile, request: Request):
    """
    Atom AI endpoint
    """
    # from speech to text
    outputWhisper = fast_whisper.run(user_prompt)["text"]["text"]
    
    # call llama3
    outputLlama = llama3.run(outputWhisper, system_prompt=SYSTEM_PROMPT)["respond"]
    
    # from text to speech
    outputSuno = suno.run(outputLlama)
    base_url = str(request.base_url)
    
    # Construct the URL for the audio file
    url_audio_suno =  f"{base_url.rstrip('/')}{outputSuno['speech']}"
    
    # return the final output
    return {
        "input_text": outputWhisper,
        "response_text": outputLlama,
        "speech_url": url_audio_suno
    }

@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join("downloads", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, media_type='audio/wav', filename=filename, headers={"Content-Disposition": "inline"})
    else:
        return {"error": "File not found"}
