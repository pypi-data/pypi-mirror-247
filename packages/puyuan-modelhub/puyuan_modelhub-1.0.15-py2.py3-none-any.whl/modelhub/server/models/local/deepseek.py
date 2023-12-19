from ....common.types import (
    TextGenerationOutput,
    TextGenerationStreamDetails,
)
from ...models.errors import *
from ...models.base import BaseChatModel
from ...lib.utils import torch_gc

from typing import Optional, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json


class DeepseekBaseModel(BaseChatModel):
    local_model_path: str
    tokenizer_path: str
    cuda_device: int = 0
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            print("Loading deepseek model")
            # os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.local_model_path,
                trust_remote_code=True,
                use_flash_attention_2=True,
                torch_dtype=torch.bfloat16,
            ).cuda(self.cuda_device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path, trust_remote_code=True
            )
            # os.environ["CUDA_VISIBLE_DEVICES"] = ""
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Failed to load Deepseek Model: {e}")

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=128,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        parameters.pop("history")
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            parameters = self.default_parameters | parameters
            outputs = self.model.generate(**inputs, **parameters)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            torch_gc(self.cuda_device)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )


class DeepseekModel(BaseChatModel):
    local_model_path: str
    tokenizer_path: str
    cuda_device: int = 0
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            print("Loading deepseek model")
            # os.environ["CUDA_VISIBLE_DEVICES"] = str(self.cuda_device)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.local_model_path,
                trust_remote_code=True,
                use_flash_attention_2=True,
                torch_dtype=torch.bfloat16,
            ).cuda(self.cuda_device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path, trust_remote_code=True
            )
            # os.environ["CUDA_VISIBLE_DEVICES"] = ""
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Failed to load Deepseek Model: {e}")

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=512,
            do_sample=False,
            top_k=50,
            top_p=0.95,
            num_return_sequences=1,
            eos_token_id=32021,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        messages = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        try:
            inputs = self.tokenizer.apply_chat_template(
                messages, return_tensors="pt"
            ).to(self.model.device)
            parameters = self.default_parameters | parameters
            outputs = self.model.generate(inputs, **parameters)
            response = self.tokenizer.decode(
                outputs[0][len(inputs[0]) :], skip_special_tokens=True
            )
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            torch_gc(self.cuda_device)
        if isinstance(response, dict):
            response = json.dumps(response, ensure_ascii=False)
        return TextGenerationOutput(
            generated_text=response,
            history=messages + [{"role": "assistant", "content": response}],
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )
