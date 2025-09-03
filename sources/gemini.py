from google import genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv
import os

load_dotenv()

class Gemini:
    api_key = os.getenv("GEMINI_API_KEY")

    def __init__(self, model="gemini-2.5-flash"):
        self.client = genai.Client(http_options=HttpOptions(api_version="v1"), )
        self.model = model

    def chat(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text

# Example usage
if __name__ == "__main__":
    bot = Gemini()
    print(bot.chat("Explain how AI works in a few sentences."))
