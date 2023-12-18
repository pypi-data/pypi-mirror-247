"""Custom Loguru.Logger with custom formatting and predesignated sinks."""
from json import dump, load
from os import getenv
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.prompt import Confirm, IntPrompt

from maxlog import Log

__version__ = "0.0.3"
__all__ = ["Log", "get_project_dir", "get_logs_dir", "get_run_file_path", "get_run"]
logger.disable("maxlog")


def get_project_dir():
    """Generate the project directory from the active virtual environment."""
    load_dotenv()
    project_name = getenv("VIRTUAL_ENV_PROMPT")
    if project_name:
        return Path.home() / "dev" / "py" / project_name
    else:
        pwd: Path = Path(__file__).parent
        while pwd.stem != "py":
            pwd = pwd.parent
        return pwd


def get_logs_dir():
    """Generate the logs directory from the active virtual environment."""
    return get_project_dir() / "logs"


def get_run_file_path():
    """Generate the run file path from the active virtual environment."""
    return get_logs_dir() / "run.json"


def get_run(run_file: Optional[Path] = None) -> int:
    """Get the run file from the active virtual environment."""
    if run_file is None:
        run_file = get_run_file_path()
    if run_file.exists():
        with run_file.open("r") as file:
            return load(file)
    else:
        # if run file does not exist, prompt to create it
        console = Console()
        if Confirm.ask(
            prompt="[#bold #ffaf00]No run file found. Set run to 0?[/]", console=console
        ):
            with open(run_file, "w") as outfile:
                dump({"run": 0}, outfile, indent=4)
            return 0
        elif Confirm.ask(prompt="[#bold #ffaf00]Set run manually?[/]", console=console):
            run = IntPrompt.ask(prompt="[#ffaf00]Enter run number:[/]", console=console)
            with open(run_file, "w") as outfile:
                dump({"run": run}, outfile, indent=4)
            return run
        else:
            raise FileNotFoundError("Unable to locate run file.")
