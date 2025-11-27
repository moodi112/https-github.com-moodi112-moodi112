"""
Entry point for running the Oman Events Wikipedia Generator as a module.
Usage: python -m src.cli [command] [options]
"""
from .cli import cli

if __name__ == "__main__":
    cli()
