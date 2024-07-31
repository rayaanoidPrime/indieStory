import os
from typing import List
import torch
from nltk.tokenize import sent_tokenize
from PIL.Image import Image
from config import IndieStoryConfig
from services.writer import WriterService
from services.painter import PainterService
from services.speaker import SpeakerService
from utils.helpers import require_ffmpeg, require_punkt, subprocess_run, make_timeline_string

class IndieStory:
    @require_ffmpeg
    @require_punkt
    def __init__(self, config: IndieStoryConfig):
        self.config = config
        self.writer = WriterService(config)
        self.painter = PainterService(config)
        self.speaker = SpeakerService(config)
        self.sample_rate = self.speaker.sample_rate
        self.output_dir = None

    def generate(
        self,
        writer_prompt: str,
        painter_prompt_prefix: str,
        num_images: int,
        output_dir: str,
    ) -> None:
        video_paths = []
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        sentences = self.write_story(writer_prompt, num_images)
        for i, sentence in enumerate(sentences):
            video_path = self._generate(i, sentence, painter_prompt_prefix)
            video_paths.append(video_path)
        self.concat_videos(video_paths)

    def concat_videos(self, video_paths: List[str]) -> None:
        files_path = self.get_output_path("files.txt")
        output_path = self.get_output_path("out.mp4")
        with open(files_path, "w+") as f:
            for video_path in video_paths:
                f.write(f"file {os.path.split(video_path)[-1]}\n")
        subprocess_run(f"ffmpeg -f concat -i {files_path} -c copy {output_path}")

    def _generate(self, id_: int, sentence: str, painter_prompt_prefix: str) -> str:
        image_path = self.get_output_path(f"{id_}.png")
        audio_path = self.get_output_path(f"{id_}.wav")
        subtitle_path = self.get_output_path(f"{id_}.srt")
        video_path = self.get_output_path(f"{id_}.mp4")
        
        image = self.painter.paint(f"{painter_prompt_prefix} {sentence}")
        image.save(image_path)
        
        audio = self.speaker.speak(sentence)
        duration = len(audio) / self.sample_rate
        self.speaker.save_audio(audio_path, audio)
        
        subtitle = f"0\n{make_timeline_string(0, int(duration))}\n{sentence}"
        with open(subtitle_path, "w+") as f:
            f.write(subtitle)
        
        subprocess_run(
            f"ffmpeg -loop 1 -i {image_path} -i {audio_path} -vf subtitles={subtitle_path} -tune stillimage -shortest {video_path}"
        )
        return video_path

    def write_story(self, writer_prompt: str, num_sentences: int) -> List[str]:
        sentences = []
        while len(sentences) < num_sentences + 1:
            writer_prompt = self.writer.write(writer_prompt)
            sentences = sent_tokenize(writer_prompt)
        while len(sentences) > num_sentences:
            sentences.pop()
        return sentences

    def get_output_path(self, file: str) -> str:
        return os.path.join(self.output_dir, file)