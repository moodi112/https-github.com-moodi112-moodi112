# Oman Events Wikipedia Generator

A Python CLI tool that generates Wikipedia-style articles about Oman events using OpenAI's GPT models.

## Features

- **Full Article Generation**: Create comprehensive Wikipedia-style articles with proper structure and sections
- **Summary Generation**: Generate concise summaries of events
- **Infobox Creation**: Create Wikipedia-style infoboxes with key event details
- **Complete Package**: Generate articles with infobox, summary, and full content in one command
- **Flexible Output**: Save to files or display in terminal
- **Customizable**: Choose writing style, article length, and AI model

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     OPENAI_MODEL=gpt-4
     ```

## Usage

### Basic Commands

The tool provides four main commands:

#### 1. Generate Article
Create a full Wikipedia-style article:

```bash
python -m src.cli article "Muscat Festival"
```

With options:
```bash
python -m src.cli article "Muscat Festival" \
  --style formal \
  --context "Annual cultural festival in January" \
  --output muscat_festival.txt \
  --model gpt-4
```

**Options:**
- `--context, -c`: Additional context about the event
- `--style, -s`: Writing style (formal, casual, detailed)
- `--output, -o`: Save to file instead of printing to terminal
- `--model, -m`: OpenAI model to use (default: gpt-4)

#### 2. Generate Summary
Create a brief summary:

```bash
python -m src.cli summary "National Day of Oman"
```

With options:
```bash
python -m src.cli summary "National Day of Oman" \
  --max-length 150 \
  --model gpt-4
```

**Options:**
- `--max-length, -l`: Maximum words in summary (default: 200)
- `--model, -m`: OpenAI model to use

#### 3. Generate Infobox
Create a Wikipedia-style infobox:

```bash
python -m src.cli infobox "Salalah Tourism Festival"
```

**Options:**
- `--model, -m`: OpenAI model to use

#### 4. Generate Complete Package
Generate infobox, summary, and full article in one command:

```bash
python -m src.cli full "Muscat Festival" --output complete_article.txt
```

With context:
```bash
python -m src.cli full "Muscat Festival" \
  --context "Major winter festival attracting international visitors" \
  --output complete_article.txt \
  --model gpt-4
```

**Options:**
- `--context, -c`: Additional context about the event
- `--output, -o`: Output file path (required)
- `--model, -m`: OpenAI model to use

### Example Oman Events

Here are some events you can generate articles about:

- **Muscat Festival** - Annual cultural and shopping festival
- **Salalah Tourism Festival** - Summer festival in Dhofar
- **National Day of Oman** - November 18th celebration
- **Renaissance Day** - July 23rd commemoration
- **Oman Desert Marathon** - Annual desert running event
- **Muscat International Book Fair** - Literary event
- **Al Mouj Golf Tournament** - Golf championship
- **Oman Rally** - International rally event
- **Khareef Season** - Monsoon season in Salalah
- **Oman Traditional Crafts Festival** - Handicrafts showcase

### Command Examples

Generate article and save to file:
```bash
python -m src.cli article "National Day of Oman" -o national_day.txt
```

Generate summary with shorter length:
```bash
python -m src.cli summary "Salalah Tourism Festival" --max-length 100
```

Generate complete package with context:
```bash
python -m src.cli full "Muscat Festival" \
  --context "Held annually in January-February, featuring cultural performances and shopping" \
  --output muscat_festival_complete.txt
```

Use different model:
```bash
python -m src.cli article "Oman Rally" --model gpt-3.5-turbo
```

## API Usage

You can also use the tool programmatically:

```python
from src.wiki_generator import WikiGenerator

# Initialize generator
generator = WikiGenerator(model="gpt-4")

# Generate article
article = generator.generate_wiki_article(
    event_name="Muscat Festival",
    context="Annual cultural event",
    style="formal"
)

# Generate summary
summary = generator.generate_summary("Muscat Festival", max_length=200)

# Generate infobox
infobox = generator.generate_infobox("Muscat Festival")

print(article)
```

## Configuration

### Environment Variables

Create a `.env` file with:

```env
# Required
OPENAI_API_KEY=your_api_key_here

# Optional
OPENAI_MODEL=gpt-4
```

### Supported Models

- `gpt-4` (default, recommended for best quality)
- `gpt-4-turbo`
- `gpt-3.5-turbo` (faster, more economical)

## Output Format

### Article Structure
Generated articles include:
- Introductory paragraph
- Historical background
- Key details and information
- Cultural/economic impact
- Notable participants
- Related events/traditions
- References section

### Infobox Structure
Infoboxes contain:
- Date/Time period
- Location
- Event type
- Significance
- Participants
- Other relevant details

## Error Handling

Common errors and solutions:

**API Key Not Found:**
```
Error: OpenAI API key not found. Please set OPENAI_API_KEY in .env file
```
Solution: Create `.env` file and add your API key

**Invalid Model:**
```
Error: Model not found
```
Solution: Use a valid OpenAI model name (gpt-4, gpt-3.5-turbo, etc.)

**Rate Limit:**
```
Error: Rate limit exceeded
```
Solution: Wait a moment and retry, or upgrade your OpenAI plan

## Tips for Best Results

1. **Provide Context**: Use the `--context` option to give the AI more information
2. **Choose Appropriate Style**: Use "formal" for encyclopedia-style, "detailed" for comprehensive coverage
3. **Use Specific Event Names**: The more specific, the better the results
4. **Save Important Articles**: Use `--output` to save generated content
5. **Review and Edit**: AI-generated content should be reviewed for accuracy

## Cost Considerations

API usage is billed by OpenAI. Approximate token usage:
- Summary: ~300-500 tokens
- Infobox: ~500-800 tokens
- Full Article: ~2000-3000 tokens
- Complete Package: ~3000-4000 tokens

Check OpenAI's pricing page for current rates.

## Troubleshooting

### Module Not Found Error
If you get `ModuleNotFoundError`, ensure you're running from the project root:
```bash
# Wrong
cd src
python -m cli article "Event"

# Correct
python -m src.cli article "Event"
```

### Dependencies Missing
Install all required packages:
```bash
pip install -r requirements.txt
```

### API Connection Issues
Check your internet connection and verify your API key is valid.

## Contributing

To add new features or improve the tool:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues or questions:
- Check the troubleshooting section
- Review OpenAI API documentation
- Report bugs via GitHub issues
