"""
Command-line interface for Oman Events Wikipedia Generator.
"""
import click
import sys
import json
from pathlib import Path
from .wiki_generator import WikiGenerator
from .exporters import ExportFormatter, BatchExporter


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Oman Events Wikipedia Generator - Generate Wikipedia-style articles about Oman events.
    
    Supports multiple languages, export formats, and batch processing.
    """
    pass


@cli.command()
@click.argument("event_name")
@click.option(
    "--context",
    "-c",
    help="Additional context or details about the event",
    default=None,
)
@click.option(
    "--style",
    "-s",
    type=click.Choice(["formal", "casual", "detailed"], case_sensitive=False),
    default="formal",
    help="Writing style for the article",
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["en", "ar"], case_sensitive=False),
    default="en",
    help="Output language: en (English) or ar (Arabic)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (prints to stdout if not specified)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["text", "markdown", "html", "pdf"], case_sensitive=False),
    default="text",
    help="Output format",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def article(event_name, context, style, language, output, format, model):
    """
    Generate a full Wikipedia-style article for an Oman event.

    Example:
        python -m src.cli article "Muscat Festival" --style formal --language en
        python -m src.cli article "مهرجان مسقط" --language ar --format html
    """
    try:
        click.echo(f"Generating article for: {event_name}")
        click.echo(f"Language: {language}, Model: {model}, Format: {format}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)
        content = generator.generate_wiki_article(event_name, context, style, language)

        # Handle output format
        if format == "markdown":
            content = ExportFormatter.to_markdown(content, event_name)
        elif format == "html":
            content = ExportFormatter.to_html(content, event_name)
        elif format == "pdf":
            if not output:
                click.echo("Error: PDF format requires --output option", err=True)
                sys.exit(1)
            ExportFormatter.to_pdf(content, event_name, output)
            click.echo(f"\n✓ PDF saved to: {output}")
            return

        if output:
            output_path = Path(output)
            output_path.write_text(content, encoding="utf-8")
            click.echo(f"\n✓ Article saved to: {output}")
        else:
            click.echo("\n" + "=" * 80)
            click.echo(content)
            click.echo("=" * 80)

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo(
            "\nPlease ensure you have set OPENAI_API_KEY in your .env file.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating article: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("event_name")
@click.option(
    "--max-length",
    "-l",
    type=int,
    default=200,
    help="Maximum length of summary in words (default: 200)",
)
@click.option(
    "--language",
    "-g",
    type=click.Choice(["en", "ar"], case_sensitive=False),
    default="en",
    help="Output language",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def summary(event_name, max_length, language, model):
    """
    Generate a brief summary of an Oman event.

    Example:
        python -m src.cli summary "Muscat Festival" --max-length 150 --language en
    """
    try:
        click.echo(f"Generating summary for: {event_name}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)
        content = generator.generate_summary(event_name, max_length, language)

        click.echo("\n" + "=" * 80)
        click.echo(content)
        click.echo("=" * 80)

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo(
            "\nPlease ensure you have set OPENAI_API_KEY in your .env file.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating summary: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("event_name")
@click.option(
    "--language",
    "-l",
    type=click.Choice(["en", "ar"], case_sensitive=False),
    default="en",
    help="Output language",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def infobox(event_name, language, model):
    """
    Generate a Wikipedia-style infobox for an Oman event.

    Example:
        python -m src.cli infobox "Muscat Festival" --language en
    """
    try:
        click.echo(f"Generating infobox for: {event_name}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)
        content = generator.generate_infobox(event_name, language)

        click.echo("\n" + "=" * 80)
        click.echo(content)
        click.echo("=" * 80)

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo(
            "\nPlease ensure you have set OPENAI_API_KEY in your .env file.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating infobox: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("event_name")
@click.option(
    "--context",
    "-c",
    help="Additional context or details about the event",
    default=None,
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["en", "ar"], case_sensitive=False),
    default="en",
    help="Output language",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    required=True,
    help="Output file path",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["text", "markdown", "html", "pdf"], case_sensitive=False),
    default="text",
    help="Output format",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def full(event_name, context, language, output, format, model):
    """
    Generate a complete Wikipedia article with infobox and summary.

    Example:
        python -m src.cli full "Muscat Festival" -o muscat_festival.html --format html
    """
    try:
        click.echo(f"Generating complete article for: {event_name}")
        click.echo(f"Using model: {model}, Language: {language}, Format: {format}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)

        click.echo("1/3 Generating infobox...")
        infobox_content = generator.generate_infobox(event_name, language)

        click.echo("2/3 Generating summary...")
        summary_content = generator.generate_summary(event_name, 200, language)

        click.echo("3/3 Generating full article...")
        article_content = generator.generate_wiki_article(event_name, context, "formal", language)

        # Format output
        if format == "markdown":
            full_content = ExportFormatter.to_markdown(article_content, event_name, infobox_content, summary_content)
        elif format == "html":
            full_content = ExportFormatter.to_html(article_content, event_name, infobox_content, summary_content)
        elif format == "pdf":
            ExportFormatter.to_pdf(article_content, event_name, output, infobox_content, summary_content)
            click.echo(f"\n✓ Complete article saved to: {output}")
            return
        else:  # text
            full_content = f"""{'=' * 80}
INFOBOX
{'=' * 80}

{infobox_content}

{'=' * 80}
SUMMARY
{'=' * 80}

{summary_content}

{'=' * 80}
FULL ARTICLE
{'=' * 80}

{article_content}
"""

        output_path = Path(output)
        output_path.write_text(full_content, encoding="utf-8")
        click.echo(f"\n✓ Complete article saved to: {output}")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo(
            "\nPlease ensure you have set OPENAI_API_KEY in your .env file.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating content: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--events",
    "-e",
    multiple=True,
    help="Event names to generate (can be specified multiple times)",
)
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="File containing event names (one per line)",
)
@click.option(
    "--type",
    "-t",
    type=click.Choice(["article", "summary", "infobox"], case_sensitive=False),
    default="article",
    help="Type of content to generate",
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["en", "ar"], case_sensitive=False),
    default="en",
    help="Output language",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    required=True,
    help="Output directory for generated files",
)
@click.option(
    "--export-format",
    "-x",
    type=click.Choice(["text", "markdown", "html", "pdf"], case_sensitive=False),
    default="text",
    help="Export format",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def batch(events, file, type, language, output_dir, export_format, model):
    """
    Generate content for multiple events in batch.

    Example:
        python -m src.cli batch -e "Muscat Festival" -e "National Day" -o ./output
        python -m src.cli batch --file events.txt -o ./output --export-format html
    """
    try:
        # Collect event names
        event_names = list(events)
        
        if file:
            file_path = Path(file)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_events = [line.strip() for line in f if line.strip()]
                event_names.extend(file_events)
        
        if not event_names:
            click.echo("Error: No events specified. Use --events or --file", err=True)
            sys.exit(1)
        
        click.echo(f"Batch processing {len(event_names)} events...")
        click.echo(f"Type: {type}, Language: {language}, Format: {export_format}\n")
        
        generator = WikiGenerator(model=model)
        
        # Generate content
        results = generator.batch_generate(
            event_names=event_names,
            output_type=type,
            language=language
        )
        
        # Export results
        if export_format == "text":
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            for event_name, content in results.items():
                safe_name = "".join(c for c in event_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                file_path = output_path / f"{safe_name}.txt"
                file_path.write_text(content, encoding='utf-8')
                click.echo(f"✓ Saved: {file_path}")
        else:
            exported = BatchExporter.export_batch(
                articles=results,
                format=export_format,
                output_dir=output_dir
            )
            
            for title, path in exported.items():
                click.echo(f"✓ Exported: {path}")
        
        click.echo(f"\n✓ Batch processing complete! {len(results)} files generated.")

    except Exception as e:
        click.echo(f"Error in batch processing: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("event_name")
@click.option(
    "--context",
    "-c",
    help="Additional context for better image generation",
    default=None,
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["en", "ar"], case_sensitive=False),
    default="en",
    help="Output language",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def image_prompt(event_name, context, language, model):
    """
    Generate article with DALL-E image prompt.

    Example:
        python -m src.cli image-prompt "Muscat Festival"
    """
    try:
        click.echo(f"Generating article with image prompt for: {event_name}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)
        result = generator.generate_with_image(event_name, context, language)

        click.echo("\n" + "=" * 80)
        click.echo("IMAGE PROMPT FOR DALL-E:")
        click.echo("=" * 80)
        click.echo(result["image_prompt"])
        
        click.echo("\n" + "=" * 80)
        click.echo("ARTICLE:")
        click.echo("=" * 80)
        click.echo(result["article"])
        click.echo("=" * 80)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()

