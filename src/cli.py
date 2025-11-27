"""
Command-line interface for Oman Events Wikipedia Generator.
"""
import click
import sys
from pathlib import Path
from .wiki_generator import WikiGenerator


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Oman Events Wikipedia Generator - Generate Wikipedia-style articles about Oman events.
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
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (prints to stdout if not specified)",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def article(event_name, context, style, output, model):
    """
    Generate a full Wikipedia-style article for an Oman event.

    Example:
        python -m src.cli article "Muscat Festival" --style formal
    """
    try:
        click.echo(f"Generating article for: {event_name}")
        click.echo(f"Using model: {model}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)
        content = generator.generate_wiki_article(event_name, context, style)

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
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def summary(event_name, max_length, model):
    """
    Generate a brief summary of an Oman event.

    Example:
        python -m src.cli summary "Muscat Festival" --max-length 150
    """
    try:
        click.echo(f"Generating summary for: {event_name}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)
        content = generator.generate_summary(event_name, max_length)

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
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def infobox(event_name, model):
    """
    Generate a Wikipedia-style infobox for an Oman event.

    Example:
        python -m src.cli infobox "Muscat Festival"
    """
    try:
        click.echo(f"Generating infobox for: {event_name}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)
        content = generator.generate_infobox(event_name)

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
    "--output",
    "-o",
    type=click.Path(),
    required=True,
    help="Output file path",
)
@click.option(
    "--model",
    "-m",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4)",
)
def full(event_name, context, output, model):
    """
    Generate a complete Wikipedia article with infobox and summary.

    Example:
        python -m src.cli full "Muscat Festival" -o muscat_festival.txt
    """
    try:
        click.echo(f"Generating complete article for: {event_name}")
        click.echo(f"Using model: {model}")
        click.echo("Please wait...\n")

        generator = WikiGenerator(model=model)

        click.echo("1/3 Generating infobox...")
        infobox_content = generator.generate_infobox(event_name)

        click.echo("2/3 Generating summary...")
        summary_content = generator.generate_summary(event_name)

        click.echo("3/3 Generating full article...")
        article_content = generator.generate_wiki_article(event_name, context, "formal")

        # Combine all parts
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


if __name__ == "__main__":
    cli()
