import json

from app.core.errors import ParserError
from app.core.config import Settings


class LLMClient:
    """Thin OpenAI-compatible client shared by extraction and grounded Q&A."""

    def __init__(self, settings: Settings):
        from openai import OpenAI

        kwargs = {"api_key": settings.LLM_API_KEY}
        if settings.LLM_BASE_URL:
            kwargs["base_url"] = settings.LLM_BASE_URL
        self.client = OpenAI(**kwargs)
        self.model = settings.LLM_MODEL

    def complete_json(self, system_prompt: str, user_prompt: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            if not content:
                raise ParserError()
            return json.loads(content)
        except ParserError:
            raise
        except Exception as exc:
            raise ParserError() from exc

    def complete_text(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
            )
            content = response.choices[0].message.content
            if not content:
                raise ParserError()
            return content.strip()
        except ParserError:
            raise
        except Exception as exc:
            raise ParserError() from exc