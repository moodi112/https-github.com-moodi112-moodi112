"""
Tests for the Oman Events Wikipedia Generator.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.wiki_generator import WikiGenerator


class TestWikiGenerator:
    """Test cases for WikiGenerator class."""

    def test_init_with_api_key(self):
        """Test initialization with API key provided."""
        generator = WikiGenerator(api_key="test-key", model="gpt-4")
        assert generator.api_key == "test-key"
        assert generator.model == "gpt-4"

    def test_init_without_api_key_raises_error(self):
        """Test initialization without API key raises ValueError."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                WikiGenerator()
            assert "OpenAI API key not found" in str(exc_info.value)

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-env-key"})
    def test_init_with_env_variable(self):
        """Test initialization with API key from environment."""
        generator = WikiGenerator()
        assert generator.api_key == "test-env-key"

    @patch("src.wiki_generator.OpenAI")
    def test_generate_wiki_article(self, mock_openai):
        """Test generating a wiki article."""
        # Mock the OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test Wikipedia Article Content"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        generator = WikiGenerator(api_key="test-key")
        result = generator.generate_wiki_article("Muscat Festival")

        assert result == "Test Wikipedia Article Content"
        mock_client.chat.completions.create.assert_called_once()

    @patch("src.wiki_generator.OpenAI")
    def test_generate_wiki_article_with_context(self, mock_openai):
        """Test generating a wiki article with context."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Article with Context"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        generator = WikiGenerator(api_key="test-key")
        result = generator.generate_wiki_article(
            "Muscat Festival", context="Annual event", style="formal"
        )

        assert result == "Article with Context"
        assert mock_client.chat.completions.create.called

    @patch("src.wiki_generator.OpenAI")
    def test_generate_summary(self, mock_openai):
        """Test generating a summary."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test Summary"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        generator = WikiGenerator(api_key="test-key")
        result = generator.generate_summary("National Day", max_length=150)

        assert result == "Test Summary"
        mock_client.chat.completions.create.assert_called_once()

    @patch("src.wiki_generator.OpenAI")
    def test_generate_infobox(self, mock_openai):
        """Test generating an infobox."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test Infobox"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        generator = WikiGenerator(api_key="test-key")
        result = generator.generate_infobox("Salalah Festival")

        assert result == "Test Infobox"
        mock_client.chat.completions.create.assert_called_once()

    @patch("src.wiki_generator.OpenAI")
    def test_api_error_handling(self, mock_openai):
        """Test API error handling."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        generator = WikiGenerator(api_key="test-key")

        with pytest.raises(Exception) as exc_info:
            generator.generate_wiki_article("Test Event")
        assert "Error generating content" in str(exc_info.value)

    def test_build_prompt_basic(self):
        """Test basic prompt building."""
        generator = WikiGenerator(api_key="test-key")
        prompt = generator._build_prompt("Test Event", None, "formal")

        assert "Test Event" in prompt
        assert "formal" in prompt
        assert "wikipedia-style article" in prompt.lower()

    def test_build_prompt_with_context(self):
        """Test prompt building with context."""
        generator = WikiGenerator(api_key="test-key")
        prompt = generator._build_prompt(
            "Test Event", "Additional context here", "detailed"
        )

        assert "Test Event" in prompt
        assert "Additional context here" in prompt
        assert "detailed" in prompt

    @patch("src.wiki_generator.OpenAI")
    def test_different_models(self, mock_openai):
        """Test using different models."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Content"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # Test with gpt-3.5-turbo
        generator = WikiGenerator(api_key="test-key", model="gpt-3.5-turbo")
        assert generator.model == "gpt-3.5-turbo"

        # Test with gpt-4
        generator = WikiGenerator(api_key="test-key", model="gpt-4")
        assert generator.model == "gpt-4"

    @patch("src.wiki_generator.OpenAI")
    def test_summary_length_parameter(self, mock_openai):
        """Test that summary respects max_length parameter."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Short summary"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        generator = WikiGenerator(api_key="test-key")

        # Test with different max lengths
        generator.generate_summary("Event", max_length=100)
        call_args = mock_client.chat.completions.create.call_args

        # Check that max_length is in the prompt
        messages = call_args[1]["messages"]
        user_message = next(m for m in messages if m["role"] == "user")
        assert "100" in user_message["content"]


class TestWikiGeneratorIntegration:
    """Integration tests that require actual API calls (skipped by default)."""

    @pytest.mark.skip(reason="Requires actual OpenAI API key and makes real API calls")
    def test_real_api_call(self):
        """Test with real API (only run manually with valid API key)."""
        import os

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("No API key available")

        generator = WikiGenerator(api_key=api_key, model="gpt-3.5-turbo")
        result = generator.generate_summary("Muscat Festival", max_length=50)

        assert result
        assert len(result) > 0
        assert isinstance(result, str)
