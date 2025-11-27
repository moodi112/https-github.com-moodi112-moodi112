# Quick Start Guide - Oman Events Wikipedia Generator

This guide will help you get started with the Oman Events Wikipedia Generator in under 5 minutes.

## Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation (2 minutes)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your API key:**
```bash
# Copy the example environment file
cp .env.example .env
```

3. **Edit `.env` file and add your API key:**
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4
```

That's it! You're ready to go.

## Basic Usage (Try these examples)

### Example 1: Generate a Wikipedia Article
```bash
python -m src.cli article "Muscat Festival"
```

This will generate a comprehensive Wikipedia-style article about the Muscat Festival and display it in your terminal.

### Example 2: Save Article to File
```bash
python -m src.cli article "National Day of Oman" -o national_day.txt
```

This saves the generated article to a file.

### Example 3: Generate a Summary
```bash
python -m src.cli summary "Salalah Tourism Festival" --max-length 150
```

This generates a brief 150-word summary.

### Example 4: Generate Complete Package
```bash
python -m src.cli full "Oman Rally" -o oman_rally_complete.txt
```

This generates an infobox, summary, and full article all in one file.

### Example 5: Add Context for Better Results
```bash
python -m src.cli article "Muscat Festival" \
  --context "Annual cultural festival held in January-February featuring traditional performances" \
  --style detailed \
  -o muscat_detailed.txt
```

## Common Oman Events to Try

Here are some events you can generate articles about:

**National Events:**
- National Day of Oman
- Renaissance Day
- Sultan Qaboos Grand Mosque Opening

**Festivals:**
- Muscat Festival
- Salalah Tourism Festival
- Khareef Festival
- Musandam Sea Festival

**Sports:**
- Oman Desert Marathon
- Al Mouj Golf Tournament
- Oman Sail
- Tour of Oman (cycling)

**Cultural:**
- Muscat International Book Fair
- Oman Traditional Crafts Festival
- Omani Women's Day

**Natural:**
- Khareef Season (Monsoon)
- Turtle Nesting Season

## Command Options

### For `article` command:
- `--style` or `-s`: Choose writing style (formal, casual, detailed)
- `--context` or `-c`: Provide additional context
- `--output` or `-o`: Save to file
- `--model` or `-m`: Choose AI model (gpt-4, gpt-3.5-turbo)

### For `summary` command:
- `--max-length` or `-l`: Set maximum words (default: 200)
- `--model` or `-m`: Choose AI model

### For `full` command:
- `--context` or `-c`: Provide additional context
- `--output` or `-o`: Output file (required)
- `--model` or `-m`: Choose AI model

## Troubleshooting

### "OpenAI API key not found"
- Make sure you created the `.env` file
- Check that you added your API key correctly
- Ensure there are no extra spaces or quotes around the key

### "Module not found"
- Run from the project root directory
- Make sure you installed dependencies: `pip install -r requirements.txt`

### Rate limit errors
- Wait a moment and try again
- Consider using `gpt-3.5-turbo` which has higher rate limits

## Cost Considerations

Approximate costs per request (as of 2024):
- Summary: ~$0.01 - $0.02 (with GPT-4)
- Full Article: ~$0.03 - $0.05 (with GPT-4)
- Complete Package: ~$0.05 - $0.08 (with GPT-4)

Using `gpt-3.5-turbo` is about 10x cheaper but may produce less detailed results.

## Next Steps

- Read the [full documentation](OMAN_WIKI_GENERATOR.md) for advanced features
- Check out the [main README](README.md) for project details
- Run tests: `pytest tests/test_wiki_generator.py`

## Getting Help

If you encounter issues:
1. Check this guide first
2. Read the troubleshooting section in [OMAN_WIKI_GENERATOR.md](OMAN_WIKI_GENERATOR.md)
3. Open a GitHub issue with details about the error

Happy generating! 🇴🇲
