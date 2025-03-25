import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


class ReportPostprocessor:
    """
    A client for interacting with the Gemini Generative API using streaming responses.

    Attributes:
        model_name (str): The model to use (default 'gemini-pro').
        sys (str): A system-level prompt to prepend to every user prompt.
    """

    def __init__(self, model_name: str = "gemini-2.0-flash-lite", sys: str = None):
        self.model_name = model_name
        self.system_message = sys or ""
        self.model = genai.GenerativeModel(model_name)

    def process(self, prompt: str, stream: bool = False):
        """
        Generate content from Gemini API by combining the system message (if provided) with the user prompt.
        The response is streamed back chunk-by-chunk.

        Args:
            prompt (str): The prompt/question for content generation.
            stream (bool): Whether to stream the response. Defaults to True.

        Yields:
            str: The text of each chunk received from the API.
        """
        full_prompt = f"{self.system_message}\n{prompt}" if self.system_message else prompt
        response = self.model.generate_content(full_prompt, stream=stream)
        return response.text
