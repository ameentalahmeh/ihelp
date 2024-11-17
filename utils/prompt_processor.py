import os
from dataclasses import dataclass
from typing import Optional
from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage, MessageRole
from dotenv import load_dotenv
from utils.logger import get_logger

log = get_logger(__name__)

# Load environment variables early on
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY or TOGETHER_API_KEY == "":
    log.error("TOGETHER_API_KEY is not set in the environment variables.")
    raise ValueError("TOGETHER_API_KEY is required but not found.")


@dataclass
class UserPrompt:
    text: str
    model: str = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"


# Singleton to reuse the TogetherLLM instance
class LLMClient:
    _instance: Optional[TogetherLLM] = None

    @classmethod
    def get_instance(cls, model: str) -> TogetherLLM:
        """Return the singleton instance of the LLM client."""
        if cls._instance is None or cls._instance.model != model:
            cls._instance = TogetherLLM(model=model, api_key=TOGETHER_API_KEY)
        return cls._instance


def process_prompt(input: UserPrompt):
    try:
        model = input.model
        llm = LLMClient.get_instance(model)
        messages = [ChatMessage(role=MessageRole.USER, content=input.text)]
        resp = llm.chat(messages)
        result = resp.message.content
        log.info(f"Raw response from LLM: {result}")
        return result
    except Exception as e:
        log.error(f"Error processing prompt: {e}")
        return None
