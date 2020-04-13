import sys
from pathlib import Path
from typing import Union

from loguru import logger

MESSAGE_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | <cyan>file: {name}</cyan> | line: {line} |> {message}"


def get_logger(filename: str = None, output_path: Union[str, Path] = None) -> logger:
    """Gets a logger with relevant handlers for the output

    This method gets a logger to print to the sys.stderr output (i.e. the terminal/ console). If a filename and output path are provided, it'll also print the logs (at
    the DEBUG level) to a file in the provide output path directory.

    Args:
        filename (:obj:`str`, optional): name of the file. Default is None.
        output_path (:obj:`str or Path`, optional): path to the directory where the log
            file will be written. Default is None.

    Returns:
        A logger object
    """
    config = {
        "handlers": [{"sink": sys.stderr, "format": MESSAGE_FORMAT, "level": "INFO"}]
    }

    if filename and output_path:
        log_filepath = set_log_file(filename, output_path)
        file_handler = {
            "sink": log_filepath,
            "format": MESSAGE_FORMAT,
            "level": "DEBUG",
            "rotation": "1 MB",
        }
        config["handlers"].append(file_handler)

    logger.configure(**config)
    return logger


def set_log_file(filename: str, output_path: Union[str, Path]) -> Path:
    """Gets the filepath to which the log file will be written

    This method gets a filename and output path and return the full filepath to where the log file will be written. If the directory does not exist then it will be
    created. Also the log file will be created with a .log extension so if a different
    extension is given, it will be changed to .log.

    Args:
        filename (:obj:`str`, optional): name of the file. Default is None.
        output_path (:obj:`str or Path`, optional): path to the directory where the log
            file will be written. Default is None.

    Returns:
        A Path object to where the logs will be written.
    """
    if isinstance(output_path, str):
        output_path = Path(output_path)
    log_output_path = output_path / "logs"
    log_output_path.mkdir(parents=True, exist_ok=True)

    name, _ = filename.split(".")
    # If the name is a full filepath then only take the name of the file
    split_filepath = name.split("/")
    name = name if len(split_filepath) == 1 else split_filepath[-1]
    return log_output_path / f"{name}.log"
