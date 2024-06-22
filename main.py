"""
    API
"""

from typing import Union
from replicate.exceptions import ReplicateError
from fastapi import FastAPI, UploadFile, HTTPException

import models
from utils import save_file_to_directory

# create the instances of the classes for calling the models
fast_whisper = models.FastWhisper()
xtts = models.Xtts()


app = FastAPI()


@app.get("/")
def read_root():
    """
    endpoint 1
    """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    endpoint 2
    """
    return {"item_id": item_id, "q": q}


@app.post("/whisper/")
def whisper_model(sound_file: UploadFile):
    """
    Whisper endpoint
    """
    # print the file name
    print("Uploaded file name: ", sound_file.filename)
    # file path
    uploaded_file_path = ""

    # try to save the file
    try:
        # try to save the uploaded file and save the directory
        uploaded_file_path = save_file_to_directory(
            uploaded_file=sound_file, directory="user_audios"
        )
    except Exception as exc:
        # print the exception
        print(exc)
        # if something failed raise a internal error
        raise HTTPException(status_code=500, detail="Error uploading the file") from exc
    else:
        print("Upload file name: ", uploaded_file_path)

    try:
        # open the file
        with open(uploaded_file_path, "rb") as audio_file:
            # call the model
            fast_whisper_output = fast_whisper.run(audio_file=audio_file)
            # print the output
            print("Model output: ", fast_whisper_output)
        # return the text
        return {"text": fast_whisper_output}
    except ReplicateError as e:
        print(f"An error occurred with the model: {e.status} - {e.detail}")
        raise HTTPException(
            status_code=500, detail={"status": e.status, "detail": e.detail}
        ) from e
    except Exception as exc:
        # print the exception
        print(exc)
        # if something failed raise a internal error
        raise HTTPException(
            status_code=500, detail="Something bad happened in our end"
        ) from exc


@app.post("/xtts/")
def xtts_model(sound_file: UploadFile, text_to_speech: str):
    """
    Xtts endpoint
    """
    # print the text to convert to speech
    print("Text to transform to speech:", text_to_speech)
    # print the file name
    print("Uploaded file name: ", sound_file.filename)
    # file path
    uploaded_file_path = ""

    # try to save the file
    try:
        # try to save the uploaded file and save the directory
        uploaded_file_path = save_file_to_directory(
            uploaded_file=sound_file, directory="speakers"
        )
    except Exception as exc:
        # print the exception
        print(exc)
        # if something failed raise a internal error
        raise HTTPException(
            status_code=500, detail="Error uploading the speaker file"
        ) from exc
    else:
        print("Upload file name: ", uploaded_file_path)

    try:
        # open the file
        with open(uploaded_file_path, "rb") as speaker_file:
            # call the model
            xtts_whisper_output = xtts.run(text=text_to_speech, speaker=speaker_file)
            # print the output
            print("Model output: ", xtts_whisper_output)
        # return the text
        return {"speech": xtts_whisper_output}
    except ReplicateError as e:
        print(f"An error occurred with the model: {e.status} - {e.detail}")
        raise HTTPException(
            status_code=500, detail={"status": e.status, "detail": e.detail}
        ) from e
    except Exception as exc:
        # print the exception
        print(exc)
        # if something failed raise a internal error
        raise HTTPException(
            status_code=500, detail="Something bad happened in our end"
        ) from exc
