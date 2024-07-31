from dataclasses import dataclass

@dataclass(frozen=True)
class IndieStoryConfigDefaults:
    MAX_NEW_TOKENS: int = 50
    WRITER_MODEL: str = "@hf/nousresearch/hermes-2-pro-mistral-7b"
    PAINTER_MODEL: str = "@cf/bytedance/stable-diffusion-xl-lightning"
    SPEAKER_MODEL: str = "tts_models/en/ljspeech/glow-tts"
    WRITER_DEVICE: str = "cpu"
    PAINTER_DEVICE: str = "cpu"
    SPEAKER_DEVICE: str = "cpu"
    WRITER_DTYPE: str = "float32"
    PAINTER_DTYPE: str = "float32"
    ENABLE_ATTENTION_SLICING: bool = False
    USE_DPM_SOLVER: bool = True
    NUM_PAINTER_STEPS: int = 20
    CF_HOST: str = "https://api.cloudflare.com/client/v4/accounts/eddba7a7b15791b1b94d1b08b7817f92/ai/run/"
    CF_TOKEN: str = "your_cloudflare_token_here"

@dataclass
class IndieStoryConfig:
    max_new_tokens: int = IndieStoryConfigDefaults.MAX_NEW_TOKENS
    writer: str = IndieStoryConfigDefaults.WRITER_MODEL
    painter: str = IndieStoryConfigDefaults.PAINTER_MODEL
    speaker: str = IndieStoryConfigDefaults.SPEAKER_MODEL
    writer_device: str = IndieStoryConfigDefaults.WRITER_DEVICE
    painter_device: str = IndieStoryConfigDefaults.PAINTER_DEVICE
    speaker_device: str = IndieStoryConfigDefaults.SPEAKER_DEVICE
    writer_dtype: str = IndieStoryConfigDefaults.WRITER_DTYPE
    painter_dtype: str = IndieStoryConfigDefaults.PAINTER_DTYPE
    enable_attention_slicing: bool = IndieStoryConfigDefaults.ENABLE_ATTENTION_SLICING
    use_dpm_solver: bool = IndieStoryConfigDefaults.USE_DPM_SOLVER
    num_painter_steps: int = IndieStoryConfigDefaults.NUM_PAINTER_STEPS
    cf_host: str = IndieStoryConfigDefaults.CF_HOST
    cf_token: str = IndieStoryConfigDefaults.CF_TOKEN