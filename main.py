from PySide6.QtWidgets import QApplication
import sys
from gui import Main

from config import Config

import logging
import argparse
import pathlib

# Custom logging formater to add color to terminal
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s.%(msecs)03d][%(filename)s][%(levelname)s] %(message)s"
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%I:%M:%S')
        return formatter.format(record)

def setupLogging(level):
    # Get number of loglevel from string
    numeric_level = getattr(logging, level.upper(), None)

    logging.basicConfig(level=logging.DEBUG, filename="log.txt", filemode="w")

    # Disable logs lower than WARNING from matplotlib
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("pyvisa").setLevel(logging.WARNING)

    # Add console log handler with custom formatting
    console = logging.StreamHandler()
    console.setLevel(numeric_level)
    console.setFormatter(CustomFormatter())
    logging.getLogger('').addHandler(console)

def loadConfig(filename):
    config = Config(filename)
    return config


def parseArguments():
    parser = argparse.ArgumentParser(description="Measurement Automation Software")
    parser.add_argument("-c", "--config", dest="config", metavar="PATH", type=pathlib.Path, default=pathlib.Path("./configs/default.json"), help="Path to config file")
    parser.add_argument("--log", metavar="LEVEL", dest="level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="WARNING", help="Set log level")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parseArguments()
    setupLogging(args.level)
    config = loadConfig(args.config)
    app = QApplication(sys.argv)
    m = Main(config)
    m.show()
    sys.exit(app.exec())
