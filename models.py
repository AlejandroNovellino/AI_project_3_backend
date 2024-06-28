"""
Models wrapper to handle errors
"""

from fastapi import HTTPException
from replicate.exceptions import ReplicateError

import models_api
from utils import save_file_to_directory

# create the instances of the classes for calling the models
fast_whisper = models_api.FastWhisper()
xtts = models_api.Xtts()
llama3 = models_api.Llama3()


class FastWhisperWrapper:
    """
    Class for whisper
    """

    def __init__(self) -> None:
        pass

    def run(self, sound_file):
        """
        Run the model
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
            raise HTTPException(
                status_code=500, detail="Error uploading the file"
            ) from exc
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


class XttsWrapper:
    """
    Class for xtts
    """

    def __init__(self) -> None:
        pass

    def run(self, sound_file, text_to_speech):
        """
        Run the model
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
                xtts_whisper_output = xtts.run(
                    text=text_to_speech, speaker=speaker_file
                )
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

    def run_with_speaker_as_string(self, sound_file_name, text_to_speech):
        """
        Run the model
        """
        # print the text to convert to speech
        print("Text to transform to speech:", text_to_speech)
        # print the file name
        print("Speaker name: ", sound_file_name)

        try:
            # open the file
            with open(f"./static/speakers/{sound_file_name}", "rb") as speaker_file:
                # call the model
                xtts_whisper_output = xtts.run(
                    text=text_to_speech, speaker=speaker_file
                )
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


class Llama3Wrapper:
    """
    Class for xtts
    """

    def __init__(self) -> None:
        pass

    def run(self, user_prompt):
        """
        Run the model
        """
        # print the text to convert to speech
        print("Text to transform to respond:", user_prompt)

        try:
            # call the model
            llama3_output = llama3.run(
                user_prompt=user_prompt,
                system_prompt="Please respond like a english professor",
            )
            # print the output
            print("Model output: ", llama3_output)
            # modify the output
            completed_respond = ""
            for respond in llama3_output:
                if respond.data == "{}":
                    continue
                completed_respond += respond.data
            # print the respond to return
            print(completed_respond)
            # return the text
            return {"respond": completed_respond}
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
