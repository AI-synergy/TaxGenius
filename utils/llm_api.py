import os
import yaml
from groq import Groq

class LLM_API:
    """A wrapper for the Groq API to use open-source language models."""
    def __init__(self, config_path: str = "configs/config.yaml"):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.api_key = config['llm'].get('groq_api_key') or os.environ.get("GROQ_API_KEY")
        self.model = config['llm']['model']
        self.temperature = config['llm']['temperature']
        self.max_tokens = config['llm']['max_tokens']
        if not self.api_key or self.api_key == "YOUR_GROQ_API_KEY":
            raise ValueError("Groq API key is not configured. Please check configs/config.yaml")
        self.client = Groq(api_key=self.api_key)

    def generate(self, prompt: str, system_prompt: str = "You are an expert financial storyteller.") -> str:
        """Generates text using the configured Groq model."""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return f"Error: Could not generate content. Details: {e}"