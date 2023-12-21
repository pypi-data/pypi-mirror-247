import os
from io import BytesIO

import openai
from faster_whisper import WhisperModel
from pydub import AudioSegment
from speech_recognition import AudioData
from torch.cuda import is_available as is_cuda_available
import wave
import speech_recognition as sr

from weathon.utils import Singleton, timed, LANGUAGE_CODE_MAPPING, OpenAIConfig, SetupError
from weathon.utils.audio.base import SpeechToText
from weathon.utils.logger import get_logger

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

logger = get_logger(__name__)


# class Whisper(Singleton):
#     def __init__(self, model_name_or_path=, prompt: str = "", use_local: bool = True, api_url: str = ""):
#         device = 'cuda' if is_cuda_available() else 'cpu'
#         self.model = WhisperModel(model_size_or_path=model_name_or_path, device=device, download_root="data/models",compute_type="float32")
#         self.prompt = prompt
#
#     def transcribe(self, audio):
#         segments, info = self.model.transcribe(audio.astype(np.float32), initial_prompt=self.prompt)
#         return segments, info


class Whisper(Singleton, SpeechToText):
    def __init__(self, model="tiny.en", use_local: bool = True, debug: bool = False):
        super().__init__()
        if use_local:
            device = 'cuda' if is_cuda_available() else 'cpu'
            logger.info(f"loading [Local Whisper] model: [{model}]({device})...")
            self.model = WhisperModel(model_size_or_path=model, device=device, compute_type="float32")
        self.recognizer = sr.Recognizer()
        self.use_local = use_local
        if debug:
            self.wf = wave.open("output.wav", "wb")
            self.wf.setnchannels(1)  # Assuming mono audio
            self.wf.setsampwidth(2)  # Assuming 16-bit audio
            self.wf.setframerate(44100)  # Assuming 44100Hz sample rate

    @timed
    def transcribe(self, audio_bytes, platform="", prompt="", language="en-US", suppress_tokens=[-1]):
        audio = self._convert_webm_to_wav(audio_bytes, self.use_local) if platform == "web" \
            else self._convert_bytes_to_wav(audio_bytes, self.use_local)

        return self._transcribe_local(audio, prompt, suppress_tokens=suppress_tokens) if self.use_local \
            else self._transcribe_api(audio, prompt)

    def _transcribe_local(self, audio, prompt="", language="en-US", suppress_tokens=[-1]):
        language = LANGUAGE_CODE_MAPPING.get(language, 'en')
        segs, _ = self.model.transcribe(audio, language=language, vad_filter=True,
                                        initial_prompt=prompt, suppress_tokens=suppress_tokens, )
        # for segment in segs:
        #   print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        text = " ".join([seg.text for seg in segs])
        return text

    def _transcribe_api(self, audio_data: AudioData, model: str = "whisper-1", api_key=OpenAIConfig.api_key,
                        api_base=OpenAIConfig.base_endpoint):
        if not isinstance(audio_data, AudioData):
            raise ValueError("``audio_data`` must be an ``AudioData`` instance")
        if api_key is None and os.environ.get("OPENAI_API_KEY") is None:
            raise SetupError("Set environment variable ``OPENAI_API_KEY``")
        wav_data = BytesIO(audio_data.get_wav_data())
        wav_data.name = "SpeechRecognition_audio.wav"
        transcript = openai.Audio.transcribe(model, wav_data, api_key=api_key, api_base=api_base)
        return transcript["text"]

    def _convert_webm_to_wav(self, webm_data, local=True):
        webm_audio = AudioSegment.from_file(BytesIO(webm_data), format="webm")
        wav_data = BytesIO()
        webm_audio.export(wav_data, format="wav")
        if local:
            return wav_data
        with sr.AudioFile(wav_data) as source:
            audio = self.recognizer.record(source)
        return audio

    def _convert_bytes_to_wav(self, audio_bytes, local=True):
        if local:
            audio = BytesIO(sr.AudioData(audio_bytes, 44100, 2).get_wav_data())
            return audio
        return sr.AudioData(audio_bytes, 44100, 2)
