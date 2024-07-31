import torch
from TTS.api import TTS
import soundfile as sf
from config import IndieStoryConfig

class SpeakerService:
    def __init__(self, config: IndieStoryConfig):
        self.config = config
        self.speaker = TTS(config.speaker).to(config.speaker_device)
        self.sample_rate = self.speaker.synthesizer.output_sample_rate

    @torch.inference_mode()
    def speak(self, prompt: str) -> torch.Tensor:
        return self.speaker.tts(prompt)

    def save_audio(self, path: str, audio: torch.Tensor) -> None:
        sf.write(path, audio, self.sample_rate)