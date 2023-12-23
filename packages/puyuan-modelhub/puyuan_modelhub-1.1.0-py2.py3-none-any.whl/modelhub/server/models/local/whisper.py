from modelhub.common.types import Transcription
from openai.types.audio.transcription_create_params import TranscriptionCreateParams
from ..base import BaseModelhubModel
import torch
from transformers import pipeline
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from loguru import logger


class BaseAudioModel(BaseModelhubModel):
    is_chat_model = False
    is_audio_model = True

    def transcribe(self, req: TranscriptionCreateParams) -> Transcription:
        raise NotImplementedError("transcribe is not supported for this model")


class Whisper(BaseAudioModel):
    local_model_path: str
    cuda_device: int = 0
    pipeline: object = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Loading model...")
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.local_model_path, torch_dtype=torch.float16, trust_remote_code=True
        ).to(self.cuda_device)
        processer = AutoProcessor.from_pretrained(
            self.local_model_path, trust_remote_code=True
        )
        self.pipeline = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processer.tokenizer,
            feature_extractor=processer.feature_extractor,
            max_new_tokens=512,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch.float16,
            device=self.cuda_device,
        )
        logger.info("Model loaded")

    def transcribe(self, req: TranscriptionCreateParams) -> Transcription:
        return Transcription(text=self.pipeline(req["file"])["text"])
