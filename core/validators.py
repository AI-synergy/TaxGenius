from abc import ABC, abstractmethod
from utils.llm_api import LLM_API

class Validator(ABC):
    """Abstract base class for all validators."""
    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        pass

class TaxModelValidator(Validator):
    """
    Uses an LLM to validate the logical relevance of a generated fact, a technique
    inspired by the advanced validation methods in the MuSR codebase.
   
    """
    def __init__(self, llm_api: LLM_API):
        self.llm_api = llm_api

    def validate(self, generated_fact: str, intended_purpose: str) -> bool:
        """
        Checks if a generated fact is logically relevant to its intended purpose.
        """
        prompt = f"""
        You are a precise German tax law expert acting as a validator.
        A fact was generated to support a specific tax deduction. Your task is to check if the fact is logically relevant.

        Intended Purpose / Deduction: "{intended_purpose}"
        Generated Fact: "{generated_fact}"

        Does the generated fact logically and directly support the intended purpose ONLY?
        The fact is INVALID if it strays into proving a different kind of deduction.

        Answer with a single word: VALID or INVALID.
        """.strip()

        response = self.llm_api.generate(prompt, system_prompt="You are a logical validator.")
        return "valid" in response.lower()