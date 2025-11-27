"""
Wikipedia-style content generator for Oman events using OpenAI API.
"""
import os
import re
from typing import Optional, List, Dict
from openai import OpenAI
from dotenv import load_dotenv


class WikiGenerator:
    """Generate Wikipedia-style content for Oman events."""

    SUPPORTED_LANGUAGES = {
        "en": "English",
        "ar": "Arabic"
    }

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
        self, 
        event_name: str, 
        context: Optional[str] = None, 
        style: str = "formal",
        language: str = "en"
    ) -> str:
        """
        Generate a Wikipedia-style article for an Oman event.

        Args:
            event_name: Name of the event to generate content for.
            context: Additional context or details about the event.
            style: Writing style (formal, casual, detailed).
            language: Output language (en: English, ar: Arabic).

        Returns:
            Generated Wikipedia-style article text.
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(self.SUPPORTED_LANGUAGES.keys())}")

        # Build the prompt
        prompt = self._build_prompt(event_name, context, style, language)

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(language),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on language."""
        if language == "ar":
            return "أنت كاتب مقالات ويكيبيديا خبير متخصص في التاريخ والثقافة والأحداث العمانية. اكتب مقالات شاملة ومنظمة وواقعية."
        return "You are an expert Wikipedia article writer specializing in Omani history, culture, and events. Write comprehensive, well-structured, and factual articles."

    def _build_prompt(
        self, event_name: str, context: Optional[str], style: str, language: str
    ) -> str:
        """Build the prompt for OpenAI API."""
        if language == "ar":
            base_prompt = f"""اكتب مقالة شاملة على نمط ويكيبيديا عن '{event_name}' في عمان.

يجب أن تتضمن المقالة:
1. فقرة تمهيدية بتعريف واضح
2. الخلفية التاريخية والأهمية
3. التفاصيل والمعلومات الرئيسية
4. التأثير الثقافي أو الاقتصادي
5. المشاركون أو الشخصيات البارزة (إن وجد)
6. الأحداث أو التقاليد ذات الصلة
7. قسم المراجع

الأسلوب: {style}
"""
        else:
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
            if language == "ar":
                base_prompt += f"\nسياق إضافي: {context}"
            else:
                base_prompt += f"\nAdditional context: {context}"

        if language == "ar":
            base_prompt += "\n\nاكتب المقالة بتنسيق ويكيبيديا المناسب مع الأقسام والأقسام الفرعية."
        else:
            base_prompt += "\n\nWrite the article in proper Wikipedia format with appropriate sections and subsections."

        return base_prompt

    def generate_summary(
        self, event_name: str, max_length: int = 200, language: str = "en"
    ) -> str:
        """
        Generate a short summary of an Oman event.

        Args:
            event_name: Name of the event.
            max_length: Maximum length of summary in words.
            language: Output language (en: English, ar: Arabic).

        Returns:
            Brief summary of the event.
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")

        if language == "ar":
            prompt = f"""اكتب ملخصاً موجزاً (بحد أقصى {max_length} كلمة) عن '{event_name}' في عمان. 
ركز على أهم الحقائق والأهمية."""
        else:
            prompt = f"""Write a concise summary (max {max_length} words) about '{event_name}' in Oman. 
Focus on the most important facts and significance."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(language),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=300,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def generate_infobox(self, event_name: str, language: str = "en") -> str:
        """
        Generate a Wikipedia-style infobox for an event.

        Args:
            event_name: Name of the event.
            language: Output language (en: English, ar: Arabic).

        Returns:
            Formatted infobox content.
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")

        if language == "ar":
            prompt = f"""أنشئ صندوق معلومات على نمط ويكيبيديا لـ '{event_name}' في عمان.
يجب أن يتضمن الحقول ذات الصلة مثل:
- التاريخ/الفترة الزمنية
- الموقع
- نوع الحدث
- الأهمية
- المشاركون
- تفاصيل أخرى ذات صلة

قم بتنسيقه كصندوق معلومات نصي."""
        else:
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
                        "content": self._get_system_prompt(language),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
                max_tokens=500,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error generating infobox: {str(e)}")

    def batch_generate(
        self, 
        event_names: List[str], 
        output_type: str = "article",
        language: str = "en",
        **kwargs
    ) -> Dict[str, str]:
        """
        Generate content for multiple events in batch.

        Args:
            event_names: List of event names to generate content for.
            output_type: Type of content (article, summary, infobox).
            language: Output language.
            **kwargs: Additional arguments passed to generation methods.

        Returns:
            Dictionary mapping event names to generated content.
        """
        results = {}
        
        for event_name in event_names:
            try:
                if output_type == "article":
                    content = self.generate_wiki_article(event_name, language=language, **kwargs)
                elif output_type == "summary":
                    content = self.generate_summary(event_name, language=language, **kwargs)
                elif output_type == "infobox":
                    content = self.generate_infobox(event_name, language=language)
                else:
                    raise ValueError(f"Unknown output type: {output_type}")
                
                results[event_name] = content
            except Exception as e:
                results[event_name] = f"Error: {str(e)}"
        
        return results

    def extract_citations(self, article: str) -> List[str]:
        """
        Extract citations/references from generated article.

        Args:
            article: The generated article text.

        Returns:
            List of extracted citations.
        """
        # Look for References section
        refs_pattern = r"(?:References|المراجع)\s*\n(.*?)(?:\n\n|\Z)"
        match = re.search(refs_pattern, article, re.DOTALL | re.IGNORECASE)
        
        if not match:
            return []
        
        refs_text = match.group(1)
        
        # Extract individual citations (numbered or bulleted)
        citations = re.findall(r"(?:^|\n)\s*(?:\d+\.|\-|\*)\s*(.+?)(?=\n\s*(?:\d+\.|\-|\*)|$)", refs_text, re.DOTALL)
        
        return [c.strip() for c in citations if c.strip()]

    def validate_citations(self, citations: List[str]) -> Dict[str, bool]:
        """
        Perform basic validation on citations.

        Args:
            citations: List of citation strings.

        Returns:
            Dictionary mapping each citation to validity status.
        """
        validation_results = {}
        
        for citation in citations:
            # Basic validation: check if citation has minimum structure
            has_quotes = '"' in citation or "'" in citation
            has_year = bool(re.search(r'\b\d{4}\b', citation))
            has_punctuation = citation.endswith('.') or citation.endswith('.')
            is_substantial = len(citation) > 20
            
            is_valid = has_year and is_substantial and has_punctuation
            validation_results[citation] = is_valid
        
        return validation_results

    def generate_with_image(
        self, 
        event_name: str, 
        context: Optional[str] = None,
        language: str = "en"
    ) -> Dict[str, str]:
        """
        Generate article with DALL-E image.

        Args:
            event_name: Name of the event.
            context: Additional context.
            language: Output language.

        Returns:
            Dictionary with 'article' and 'image_prompt' keys.
        """
        # Generate article
        article = self.generate_wiki_article(event_name, context, language=language)
        
        # Generate image prompt
        if language == "ar":
            prompt = f"قم بإنشاء وصف مفصل لصورة تمثل '{event_name}' في عمان. يجب أن يكون الوصف مناسباً لتوليد الصور باستخدام DALL-E."
        else:
            prompt = f"Create a detailed image prompt for '{event_name}' in Oman that would be suitable for DALL-E image generation. Focus on visual elements, setting, atmosphere, and cultural details."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating detailed image prompts for AI image generation.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=200,
            )
            
            image_prompt = response.choices[0].message.content.strip()
            
            return {
                "article": article,
                "image_prompt": image_prompt
            }
            
        except Exception as e:
            return {
                "article": article,
                "image_prompt": f"Error generating image prompt: {str(e)}"
            }

