from faster_whisper import WhisperModel
import torch
import os


class whisperEngine:

    def __init__(self, size="large-v2", model="large-v2", language="zh"):
        self.model_size = size
        self.model_path = model
        self.context = None
        self.voice_path = None
        self.compute_type = "float16"
        self.mode = None
        self.language = language

        if language == 'zh':
            self.initial_prompt = "简体中文"
        else:
            self.initial_prompt = "English"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if torch.cuda.is_available() else "int8"


    def load_model(self):
        try:
            self.model = WhisperModel(self.model_path, device=self.device, compute_type=self.compute_type)
        except ValueError:
            self.model = WhisperModel(self.model_path, device=self.device, compute_type="int8")
        finally:
            print(f"load model complete")


    def do_transcribe(self, voice_path):
        self.context = ""
        self.voice_path = voice_path
        segments, info = self.model.transcribe(
             voice_path,
             language = self.language,
             vad_filter = True,
             vad_parameters = dict(min_silence_duration_ms=1000),
             word_timestamps = True,
             condition_on_previous_text = True,
             initial_prompt = self.initial_prompt,
        )
        if info.language != "zh":
            print(f"language : {info.language}")
        segments = list(segments)
        for segment in segments:
            self.context += segment.text
        return self.context
