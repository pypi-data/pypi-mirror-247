from __future__ import annotations

import atexit
import json
from os import environ, getenv
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import loguru
from dotenv import load_dotenv
from loguru import logger
from loguru._logger import Logger
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.pretty import Pretty
from rich.traceback import install as install_rich_traceback

load_dotenv()


class Log:
    """A custom project loguru.logger for MaxLog.
    
    Attributes:
        rich_level (int): The level at which to log to the console.
        proj_dir (Path, optional): The project directory. Defaults to None, in \
            which case the project directory is set from the environmental \
            variable VIRTUAL_ENV_PROMPT.
        console (rich.console.Console): The rich console.
        logger (loguru.Logger, optional): The loguru logger.
        handlers (List[Dict[str, Any]], optional): The loguru handlers. Defaults \
            to None, in which case the handlers are set to the default handlers.
        run (int, optional): The current run. Defaults to None, in which case \
            the run is read from the log directory.
    """

    FORMAT: str = """{time:hh:mm:ss:SSS A} | {file.name: ^13} |  \
Line {line: ^5} | {level: ^8} ﰲ  {message}"""

    def __init__(
        self,
        rich_level: Union[str, int] = "INFO",
        project_dir: Optional[str | Path] = None,
        console: Optional[Console] = None,
        loguru_logger: Optional[Logger] = None,
        handlers: List[Dict[str, Any]] = [],
        run: Optional[int] = None,
    ) -> None:
        # Set logger
        if loguru_logger is None:
            self.logger: Logger = logger  # type: ignore
        else:
            self.logger = loguru_logger

        # Set rich level
        self.rich_level = rich_level

        # Set console
        if console is None:
            console = Console()
        self.console = console
        install_rich_traceback(console=self.console, extra_lines=3)

        # Set project path
        self.proj_dir = project_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._create_log_files()

        if len(handlers) == 0:
            handlers = []
            for file in self.log_dir.iterdir():
                if file.suffix == ".log":
                    handlers.append(self._write_handler(file))

        handlers.append(
            dict(
                sink=self._loguru_sink,
                format="{message}",
                filter=self._rich_filter,
                backtrace=False,
                diagnose=False,
            )
        )

        self.handlers = handlers

        # run
        if run:
            self.run = run
            self._write_run()
        else:
            run = self._read_run()
            self.run = run

        self.logger.remove()
        self.logger.configure(
            handlers=handlers,
            extra={
                "project_path": self.proj_dir,
                "run": self.run,
                "verbose": False,
                "msg": None,
            },
            patcher=self._run_patcher,
        )

        self._write_run()
        self._write_env_vars()

    def __call__(self) -> Logger:
        return self.logger

    def __repr__(self) -> str:
        return f"Log<project={self.proj_dir.stem}, run={self.run}>"

    def __enter__(self, record: loguru.Record) -> loguru.Record:
        record["extra"]["verbose"] = True
        return record

    @property
    def proj_dir(self) -> Path:
        return self._project_path

    @proj_dir.setter
    def proj_dir(self, project_path: Optional[Union[str, Path]]) -> None:
        if project_path is None:
            load_dotenv()
            venv = getenv("VIRTUAL_ENV_PROMPT")
            if venv is None:
                raise ValueError(
                    "No project path provided and no environmental variable found."
                )
            else:
                self._project_path = Path("/Users/maxludden/dev/py/") / venv
        elif isinstance(project_path, str):
            self._project_path = Path(project_path)
        elif isinstance(project_path, Path):
            self._project_path = project_path
        else:
            raise TypeError("project_path must be a str or Path object.")

    @property
    def log_dir(self) -> Path:
        """Create log directory."""
        return self.proj_dir / "logs"

    @property
    def rich_level(self) -> int:
        return self._rich_level

    @rich_level.setter
    def rich_level(self, rich_level: Union[str, int]) -> None:
        """Set the level at which to log to the console."""
        if isinstance(rich_level, str):
            rich_level = rich_level.upper()
            match rich_level:
                case "TRACE":
                    self._rich_level = 5
                case "DEBUG":
                    self._rich_level = 10
                case "INFO":
                    self._rich_level = 20
                case "SUCCESS":
                    self._rich_level = 25
                case "WARNING":
                    self._rich_level = 30
                case "ERROR":
                    self._rich_level = 40
                case "CRITICAL":
                    self._rich_level = 50
                case _:
                    raise ValueError(
                        "rich_level must be one of: TRACE, DEBUG, INFO, SUCCESS, \
                            WARNING, ERROR, CRITICAL"
                    )
        elif isinstance(rich_level, int):
            if rich_level < 0 or rich_level > 50:
                raise ValueError("rich_level must be an integer between 0 and 50.")
            else:
                self._rich_level = rich_level
        else:
            raise TypeError("rich_level must be a str or int.")

    @property
    def handlers(self) -> List[Dict[str, Any]]:
        return self._handlers

    @handlers.setter
    def handlers(self, handlers: List[Dict[str, Any]]) -> None:
        """Set the loguru handlers."""
        self._handlers = handlers

    @property
    def run(self) -> int:
        """The current run.

        Returns:
            int: The current run.
        """
        return int(self._run)

    @run.setter
    def run(self, run: int) -> None:
        """Set the current run.

        Args:
            run (int): The current run.
        """
        self._run = run

    def _increment_run(self) -> None:
        """Increment the current run."""
        run_file = Path(self.log_dir) / "run.json"
        with open(run_file, "r") as infile:
            run = int(json.load(infile)["run"])
        run += 1
        with open(run_file, "w") as outfile:
            json.dump({"run": run}, outfile)
        self.console.line(2)

    def _read_run(self) -> int:
        """Read the current run from the log directory.

        Returns:
            int: The current run.
        """
        run_file: Path = self.log_dir / "run.json"
        if not run_file.exists():
            raise FileNotFoundError("No run file found.")
        with open(run_file, "r") as infile:
            return int(json.load(infile)["run"])

    def _write_run(self) -> None:
        run_file: Path = self.log_dir / "run.json"
        with open(run_file, "w") as outfile:
            json.dump({"run": self.run}, outfile)

    def _loguru_sink(self, msg: loguru.Message) -> None:
        """A loguru sink that prints to the console.

        Args:
            msg (loguru.Message): The loguru message to print.
        """

        record: loguru.Record = msg.record
        level_str: str = str(record["level"].name)
        style: Style = Style.null()
        verbose = bool(record["extra"].get("verbose"))

        match level_str:
            case "TRACE":
                style = Style(color="#aaaaaa")
            case "DEBUG":
                style = Style(color="#ffabf4", bold=True)
            case "INFO":
                style = Style(color="#5f00ff", bold=True)
            case "SUCCESS":
                style = Style(color="#00ff00", bold=True)
            case "WARNING":
                style = Style(color="#ffff00", bold=True)
            case "ERROR":
                style = Style(color="#ffaf00", bold=True)
            case "CRITICAL":
                style = Style(color="#ff0000", bold=True, encircle=True)

        reversed_style: Style = style + Style(reverse=True)

        width: int = self.console.width - 2

        time: Text = Text(self.console.get_datetime().strftime("%H:%M:%S"), style=style)
        run_str: str = f"Run {self.run}"
        run: Text = Text(str(f"{run_str}"), style=Style(color="#00cccc", bold=True))
        file: str = record["file"].name
        line_str = str(record["line"])
        line: str = f"Line {line_str}"
        loc_list = [
            Text(file, style=Style(color="#00ffff", bold=True, italic=True)),
            Text(": ", style=Style(color="#ffffff", bold=True)),
            Text(line, style=Style(color="#00ffff", bold=True, italic=True)),
        ]
        location = Text.assemble(*loc_list)
        level: Text = Text(str(f" {level_str} "), style=reversed_style)
        message: Text = Text(record["message"], style=style)

        table = Table(
            show_header=False,
            show_footer=False,
            show_edge=False,
            show_lines=False,
            expand=True,
            width=width,
            border_style=style
        )
        table.add_column("Time", justify="right", ratio=1)
        table.add_column("Run", justify="center", ratio=1)
        table.add_column("Location", justify="center")
        table.add_column("Level", justify="center")
        table.add_column("Message", justify="left", ratio=10)
        table.add_row(f"{time} ", run, location, level, message)
        self.console.print(table, justify="left")
        if verbose:
            self.console.print(
                Panel(
                    Pretty(record),
                    title=f"[{style}]{level_str.upper()} Record[/]",
                    style=style,
                    border_style=style
                ),
                justify="left"
            )

    # def _console_sink(self, msg: loguru.Message) -> None:
    #     """A loguru sink that prints to the console.

    #     Args:
    #         msg (loguru.Message): The loguru message to print.
    #     """

    #     record: loguru.Record = msg.record
    #     level_str: str = str(record["level"].name)
    #     style: Style = Style.null()
        

    #     match level_str:
    #         case "TRACE":
    #             style = Style(color="#5f00ff", italic=True)
    #         case "DEBUG":
    #             style = Style(color="#00afff", italic=True, bold=True)
    #         case "INFO":
    #             style = Style(color="#00ffff", bold=True)
    #         case "SUCCESS":
    #             style = Style(color="#00ff00", bold=True)
    #         case "WARNING":
    #             style = Style(color="#ffaf00", bold=True, italic=True)
    #         case "ERROR":
    #             style = Style(color="#ff0000", bold=True)
    #         case "CRITICAL":
    #             style = Style(color="#ffffff", bgcolor="#ff0000", bold=True)
    #     reversed_style: Style = style + Style(reverse=True)
    #     width: int = self.console.width - 2
    #     time: std_datetime = record["time"].replace(tzinfo=std_timezone.utc)
    #     year: int = time.year
    #     month: int = time.month
    #     day: int = time.day
    #     hour: int = time.hour
    #     minute: int = time.minute
    #     second: int = time.second
    #     microsecond: int = time.microsecond
    #     tzinfo = time.tzinfo
    #     assert tzinfo, "tzinfo is None"
    #     datetime = pdt(
    #         year, month, day, hour, minute, second, microsecond
    #     )  # type: ignore
    #     datetime_text: Text = Text(datetime.format("hh:mm:ss:SSS A"), style=style)

    #     # Run
    #     run_str: str = f"Run {self.run}"
    #     run: Text = Text(str(f"{run_str}"), style=Style(color="#00cccc", bold=True))
        
    #     # Location
    #     file: str = record["file"].name
    #     line_str = str(record["line"])
    #     line: str = f"Line {line_str}"
    #     loc_list = [
    #         Text(file, style=Style(color="#00ffff", bold=True, italic=True)),
    #         Text(": ", style=Style(color="#ffffff", bold=True)),
    #         Text(line, style=Style(color="#00ffff", bold=True, italic=True)),
    #     ]
    #     location = Text.assemble(*loc_list)
    #     level: Text = Text(str(f" {level_str} "), style=reversed_style)
    #     message: Text = Text(record["message"], style=style)

    #     table = Table(
    #         show_header=False,
    #         show_footer=False,
    #         show_edge=False,
    #         show_lines=False,
    #         expand=True,
    #         width=width,
    #     )
    #     table.add_column("Time", justify="right")
    #     table.add_column("Run", justify="center")
    #     table.add_column("Location", justify="center")
    #     table.add_column("Level", justify="center", ratio=1, min_width=16)
    #     table.add_column("Message", justify="left", ratio=5)
    #     table.add_row(f"{datetime_text} ", run, location, level, message)

    #     # verbose = bool(record["extra"].get("verbose", False))
    #     if record["extra"]["verbose"]:
    #         self.console.log(table, log_locals=True)
    #     else:
    #         self.console.print(table, justify="left")

    def _rich_filter(self, record: loguru.Record) -> bool:
        """A loguru filter that determines whether to log to the console.

        Args:
            record (loguru.Record): The loguru record to filter.

        Returns:
            bool: Whether to log the record to the console.
        """
        return record["level"].no >= self.rich_level

    def _run_patcher(self, record: loguru.Record) -> None:
        """Run the loguru patcher."""
        record["extra"].update({"run": self.run})
        if record["level"].no >= 40:
            record["extra"].update({"verbose": True})
        return

    def _create_log_files(self, log_files: Optional[List[str]] = None) -> None:
        """Create log files."""
        if log_files is None:
            log_files = [
                "debug.log",
                "info.log",
            ]
        self.log_dir.mkdir(parents=True, exist_ok=True)
        for file in log_files:
            (self.log_dir / file).touch(exist_ok=True)
        run_path: Path = self.log_dir / "run.json"
        if not run_path.exists():
            with open(run_path, "w") as outfile:
                json.dump({"run": 0}, outfile)

    def _write_env_vars(self) -> None:
        """Assign MaxLog environmental variables."""
        environ["MAXLOG_PROJECT_PATH"] = str(self.proj_dir)
        environ["MAXLOG_LOG_DIR"] = str(self.log_dir)

    def _write_handler(
        self, sink: str | Path, format: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a loguru handler."""
        # handler
        if isinstance(sink, str):
            sink = Path(sink)

        # level
        level: str = sink.stem.upper()
        if level not in [
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "RUN",
        ]:
            raise ValueError(f"Sink is not a valid log level: {level}")

        # format
        if format is None:
            format = self.FORMAT

        return {
            "sink": str(sink),
            "format": format,
            "level": level,
            "diagnose": True,
            "backtrace": True,
            "colorize": True,
        }

    def log(self, message: loguru.Message, *args, **kwargs) -> None:
        """Log a message to loguru sinks."""
        record: loguru.Record = message.record
        msg: str = record["message"]
        level: str = record["level"].name
        self.logger.log(level, msg, *args, **kwargs)

    def trace(self, *args, **kwargs) -> None:
        """Log a message with level TRACE to loguru sinks."""
        self.logger.opt(depth=1).trace(*args, **kwargs)

    def debug(self, *args, **kwargs) -> None:
        """Log a message with level DEBUG to loguru sinks."""
        self.logger.opt(depth=1).debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        """Log a message with level INFO to loguru sinks."""
        self.logger.opt(depth=1).info(*args, **kwargs)

    def success(self, *args, **kwargs) -> None:
        """Log a message with level SUCCESS to loguru sinks."""
        self.logger.opt(depth=1).success(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        """Log a message with level WARNING to loguru sinks."""
        self.logger.opt(depth=1).warning(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        """Log a message with level ERROR to loguru sinks."""
        self.logger.opt(depth=1).error(*args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        """Log a message with level CRITICAL to loguru sinks."""
        self.logger.opt(depth=1).critical(*args, **kwargs)

    # def console_log(self,msg: Any, *args, **kwargs) -> None:
    #     with self.logger.contextualize(verbose=True):
    #         self.logger.log(msg, *args, **kwargs)

    def catch(self, *args, **kwargs) -> None:
        """Log a message with level level to loguru sinks."""
        self.logger.catch(*args, **kwargs)

    @staticmethod
    def get_style(level: str) -> Style:
        """Get the style for a log level."""
        match level:
            case "TRACE":
                return Style(color="#aaaaaa", italic=True)
            case "DEBUG":
                return Style(color="#ffabf4", italic=True, bold=True)
            case "INFO":
                return Style(color="#5f00ff", bold=True)
            case "SUCCESS":
                return Style(color="#00ff00", bold=True)
            case "WARNING":
                return Style(color="#ffaf00", bold=True, italic=True)
            case "ERROR":
                return Style(color="#ff0000", bold=True)
            case "CRITICAL", _:
                return Style(color="#ffffff", bgcolor="#ff0000", bold=True)
    def _console_log_sink(self, msg: loguru.Message, *args, **kwargs) -> None:
        """Log a message to the console.
        
        Args:
            msg (loguru.Message): The loguru message to log.
            level (str, optional): The level at which to log the message. \
                Defaults to "SUCCESS".
            verbose (bool, optional): Whether to log the message verbosely. \
                Defaults to False.
        """
        record: loguru.Record = msg.record
        style: Style = Style.null()
        level: str = record["level"].name.upper()
        style = self.get_style(level)
        record["extra"]["msg"] = f"[{style}]{record['message']}[/]"
        if record["extra"].get("verbose", False):
            record_level: str = record["level"].name.upper()
            style = self.get_style(record_level)
            self.console.print(Pretty(record))
        # verbose: bool = False
        # if record["level"].no >= self.rich_level:
        #     self.console.log(record)
        # self.console.line()
        # verbose = bool(record["extra"]["verbose"])
        # if verbose:
        #     self.console.log(
        #         record["message"],
        #         record, style=style, log_locals=True, *args, **kwargs
        #     )
        # else:
        #     self.console.print(
        #         record["message"],
        #         record,
        #         style=style,
        #         log_locals=False,
        #         *args,
        #         **kwargs,
        #     )
        # self.console.line()

    def _console_log_filter(self, record: loguru.Record) -> bool:
        """A loguru filter that determines whether to log to the console.

        Args:
            record (loguru.Record): The loguru record to filter.

        Returns:
            bool: Whether to log the record to the console.
        """
        extra: Dict[str, Any] = record["extra"]
        extra_keys = extra.keys()
        if "verbose" not in extra_keys:
            return False
        return True

    def enable(self, *args, **kwargs) -> None:
        """Enable the logger."""
        self.logger.enable(*args, **kwargs)

    def disable(self, *args, **kwargs) -> None:
        """Disable the logger."""
        self.logger.disable(*args, **kwargs)


atexit.register(Log()._increment_run)

if __name__ == "__main__":  # pragma: no cover
    log = Log("TRACE")

    # Test log instance
    log.trace("This is a trace message.")
    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.success("This is a success message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    log.critical("This is a critical message.")
