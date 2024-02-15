import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument(
    "--app-host",
    default="127.0.0.1",
    help="IP of the Flask app (default: 127.0.0.1)",
    metavar="AH",
)
parser.add_argument(
    "--app-port",
    default=5000,
    type=int,
    help="TCP port of the Flask app (default: 5000)",
    metavar="AP",
)
parser.add_argument(
    "--autolaunch",
    action="store_true",
    default=False,
    help="open the webui URL in the system's default browser upon launch",
)
parser.add_argument(
    "--data-dir",
    default=os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    type=str,
    help="base path where all user data is stored",
    metavar="D",
)
parser.add_argument(
    "--dump-sysinfo",
    action="store_true",
    help="launch.py argument: dump limited sysinfo file to disk and quit",
)
parser.add_argument(
    "--flask-debug",
    action="store_true",
    help="launch Flask with --debug option",
)
parser.add_argument(
    "--host",
    default="localhost",
    help="IP of the host server (default: localhost)",
    metavar="H",
)
parser.add_argument(
    "--loglevel",
    default=None,
    type=str,
    help="log level; one of: CRITICAL, ERROR, WARNING, INFO, DEBUG",
    metavar="L",
)
parser.add_argument(
    "--log-startup",
    action="store_true",
    help="launch.py argument: print a detailed log of what's happening at startup",
)
parser.add_argument(
    "--port",
    default=2000,
    type=int,
    help="TCP port to listen to (default: 2000)",
    metavar="P",
)
parser.add_argument(
    "--skip-install",
    action="store_true",
    help="launch.py argument: skip installation of packages",
)
parser.add_argument(
    "--skip-prepare-environment",
    action="store_true",
    help="launch.py argument: skip all environment preparation",
)
parser.add_argument(
    "--skip-python-version-check",
    action="store_true",
    help="launch.py argument: do not check python version",
)
parser.add_argument(
    "--theme",
    default=None,
    type=str,
    help="launches the UI with light or dark theme",
    metavar="T",
)
parser.add_argument(
    "--update-check",
    action="store_true",
    help="launch.py argument: check for updates at startup",
)
