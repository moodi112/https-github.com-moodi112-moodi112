"""
Wikipedia-style content generator for Oman events using OpenAI API.
"""
import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv


class WikiGenerator:
    """Generate Wikipedia-style content for Oman events."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the WikiGenerator.

        Args:
            api_key: OpenAI API key. If None, loads from environment.
            model: OpenAI model to use (default: gpt-4).
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in .env file "
                "or pass it as an argument."
            )

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.client = OpenAI(api_key=self.api_key)

    def generate_wiki_article(
        self, event_name: str, context: Optional[str] = None, style: str = "formal"
    ) -> str:
        """
        Generate a Wikipedia-style article for an Oman event.

        Args:
            event_name: Name of the event to generate content for.
            context: Additional context or details about the event.
            style: Writing style (formal, casual, detailed).

        Returns:
            Generated Wikipedia-style article text.
        """
        # Build the prompt
        prompt = self._build_prompt(event_name, context, style)

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Wikipedia article writer specializing in Omani history, culture, and events. Write comprehensive, well-structured, and factual articles.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

    def _build_prompt(
        self, event_name: str, context: Optional[str], style: str
    ) -> str:
        """Build the prompt for OpenAI API."""
        base_prompt = f"""Write a comprehensive Wikipedia-style article about '{event_name}' in Oman.

The article should include:
1. An introductory paragraph with a clear definition
2. Historical background and significance
3. Key details and information
4. Cultural or economic impact
5. Notable participants or figures (if applicable)
6. Related events or traditions
7. References section

Style: {style}
"""

        if context:
            base_prompt += f"\nAdditional context: {context}"

        base_prompt += "\n\nWrite the article in proper Wikipedia format with appropriate sections and subsections."

        return base_prompt

    def generate_summary(self, event_name: str, max_length: int = 200) -> str:
        """
        Generate a short summary of an Oman event.

        Args:
            event_name: Name of the event.
            max_length: Maximum length of summary in words.

        Returns:
            Brief summary of the event.
        """
        prompt = f"""Write a concise summary (max {max_length} words) about '{event_name}' in Oman. 
Focus on the most important facts and significance."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert on Omani events and history. Provide accurate, concise summaries.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=300,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def generate_infobox(self, event_name: str) -> str:
        """
        Generate a Wikipedia-style infobox for an event.

        Args:
            event_name: Name of the event.

        Returns:
            Formatted infobox content.
        """
        prompt = f"""Create a Wikipedia-style infobox for '{event_name}' in Oman.
Include relevant fields such as:
- Date/Time period
- Location
- Type of event
- Significance
- Participants
- Other relevant details

Format it as a text-based infobox."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating Wikipedia infoboxes.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
                max_tokens=500,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error generating infobox: {str(e)}")
