from ....common.types import (
    TextGenerationOutput,
    TextGenerationStreamDetails,
)
from ...models.errors import *
from ...models.base import BaseChatModel
from typing import Optional, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from ...lib.utils import torch_gc


class YiChatModel(BaseChatModel):
    local_model_path: str
    tokenizer_path: str
    cuda_device: int = 0
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            print("Loading Yi model")
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
            raise ModelLoadError(f"Failed to load Yi Model: {e}")

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=256,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        messages = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        try:
            input_ids = self.tokenizer.apply_chat_template(
                conversations=messages,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt",
            ).to(self.model.device)
            parameters = self.default_parameters | parameters
            outputs = self.model.generate(input_ids, **parameters)
            response = self.tokenizer.decode(
                outputs[0][input_ids.shape[1] :], skip_special_tokens=True
            )
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            torch_gc(self.cuda_device)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )


class YiBaseModel(BaseChatModel):
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
            max_new_tokens=256,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        parameters.pop("history")
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            parameters = self.default_parameters | parameters
            outputs = self.model.generate(inputs.input_ids, **parameters)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate response: {e}")
        finally:
            torch_gc(self.cuda_device)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationStreamDetails(finish_reason="complete"),
        )
