import json
import logging
import time

from google import genai
from google.genai.types import GenerateContentConfig
from groq import Groq

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLM:

    def __init__(self):

        self.gemini = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.groq = Groq(
            api_key=settings.GROQ_API_KEY,
        )

    # =====================================================
    # Gemini
    # =====================================================

    def _gemini(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.4,
        json_mode: bool = False,
    ):

        config = GenerateContentConfig(
            temperature=temperature,
        )

        if system:
            config.system_instruction = system

        if json_mode:
            config.response_mime_type = "application/json"

        response = self.gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        return response.text

    # =====================================================
    # Groq
    # =====================================================

    def _groq(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.4,
        json_mode: bool = False,
    ):

        messages = []

        if system:
            messages.append(
                {
                    "role": "system",
                    "content": system,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        kwargs = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": temperature,
        }

        if json_mode:
            kwargs["response_format"] = {
                "type": "json_object"
            }

        response = self.groq.chat.completions.create(
            **kwargs
        )

        return response.choices[0].message.content

    # =====================================================
    # Public Generate
    # =====================================================

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.4,
        json_mode: bool = False,
        retries: int = 2,
    ):

        last_error = None

        # -----------------------------
        # Gemini First
        # -----------------------------

        for attempt in range(retries):

            try:

                logger.info(
                    "Using Gemini"
                )

                result = self._gemini(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    json_mode=json_mode,
                )

                if json_mode:
                    json.loads(result)

                return result

            except Exception as e:

                last_error = e

                logger.warning(
                    f"Gemini failed: {e}"
                )

                time.sleep(1)

        # -----------------------------
        # Groq Backup
        # -----------------------------

        for attempt in range(retries):

            try:

                logger.info(
                    "Using Groq Backup"
                )

                result = self._groq(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    json_mode=json_mode,
                )

                if json_mode:
                    json.loads(result)

                return result

            except Exception as e:

                last_error = e

                logger.warning(
                    f"Groq failed: {e}"
                )

                time.sleep(1)

        raise Exception(
            f"All AI providers failed.\n{last_error}"
        )

    # =====================================================
    # JSON Helper
    # =====================================================

    def generate_json(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.2,
    ):

        return json.loads(
            self.generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                json_mode=True,
            )
        )


llm = LLM()