import subprocess
from functools import wraps
from typing import Callable
import nltk
import shutil

def require_ffmpeg(func: Callable) -> Callable:
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "`ffmpeg` not found. Please install `ffmpeg` and try again."
            )
        return func(*args, **kwargs)
    return wrapper_func

def require_punkt(func: Callable) -> Callable:
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")
        return func(*args, **kwargs)
    return wrapper_func

def subprocess_run(command: str) -> None:
    subprocess.run(
        command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def make_timeline_string(start: int, end: int) -> str:
    start = format_time(start)
    end = format_time(end)
    return f"{start} --> {end}"

def format_time(time: int):
    mm, ss = divmod(time, 60)
    hh, mm = divmod(mm, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d},000"