"""
    Classes to call the Replicate models
"""

import replicate
from dotenv import load_dotenv

# load env variables
load_dotenv()


class FastWhisper:
    """
    Class for whisper
    """

    def __init__(self) -> None:
        pass

    def run(self, audio_file) -> None:
        """
        run the model
        """
        # model input
        model_input = {
            "task": "transcribe",
            "audio": audio_file,
            "language": "None",
            "timestamp": "chunk",
            "batch_size": 64,
            "diarise_audio": False,
        }
        # call the model
        output = replicate.run(
            ref="vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
            input=model_input,
        )
        print(output)

        return output


class Xtts:
    """
    Class for xtts v2
    """

    def __init__(self) -> None:
        pass

    def run(self, text, speaker) -> None:
        """
        run the model
        """
        audio_input = {
            "speaker": speaker,
            "text": text,
            "language": "en",
        }

        # call the model
        output = replicate.run(
            ref="lucataco/xtts-v2:684bc3855b37866c0c65add2ff39c78f3dea3f4ff103a436465326e0f438d55e",
            input=audio_input,
        )
        print(output)

        return output


# this class should make his return as a stream for processing quickly
class Llama3:
    """
    Class for llama 3 8b instruct
    """

    def __init__(self, replicate_instance) -> None:
        pass

    def run(
        self,
        user_prompt,
        system_prompt,
        max_tokens=512,
        min_tokens=-1,
        temperature=0.7,
        top_p=0.95,
        top_k=0,
        stop_sequences="<|end_of_text|>,<|eot_id|>",
        length_penalty=1,
        presence_penalty=0,
        seed=42,
        prompt_template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>

            {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

            {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """,
        log_performance_metrics=False,
    ) -> None:
        """
        run the model
        """

        model_input = {
            "prompt": user_prompt,
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
            "min_tokens": min_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "stop_sequences": stop_sequences,
            "length_penalty": length_penalty,
            "presence_penalty": presence_penalty,
            "seed": seed,
            "prompt_template": prompt_template,
            "log_performance_metrics": log_performance_metrics,
        }
        # output list
        output = []

        for event in replicate.stream(
            ref="meta/meta-llama-3-8b-instruct",
            input=model_input,
        ):
            print(event, end="")
            output.append(event)

        return output
