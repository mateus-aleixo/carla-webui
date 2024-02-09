#!/usr/bin/env python

"""Entry point of the CARLA Web GUI application."""

from argparse import ArgumentParser
from subprocess import Popen
from website import create_app


__author__ = "Mateus Aleixo"
__copyright__ = "Copyright (c) 2024 Mateus Aleixo"
__credits__ = ["Mateus Aleixo"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Mateus Aleixo"
__email__ = "mateus.aleixo@ubi.pt"
__status__ = "Production"


def main():
    print(__doc__)

    argparser = ArgumentParser(description="CARLA Web GUI")

    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print debug information",
        dest="debug",
    )

    argparser.add_argument(
        "--host",
        default="localhost",
        help="IP of the host server (default: localhost)",
        metavar="H",
    )

    argparser.add_argument(
        "--port",
        default=2000,
        type=int,
        help="TCP port to listen to (default: 2000)",
        metavar="P",
    )

    argparser.add_argument(
        "--app-host",
        default="127.0.0.1",
        help="IP of the Flask app (default: 127.0.0.1)",
        metavar="AH",
    )

    argparser.add_argument(
        "--app-port",
        default=5000,
        type=int,
        help="TCP port of the Flask app (default: 5000)",
        metavar="AP",
    )

    args = argparser.parse_args()

    with open(".env", "w") as file:
        file.write(f"DEBUG={args.debug}\n")
        file.write(f"HOST={args.host}\n")
        file.write(f"PORT={args.port}\n")

    app = create_app()

    Popen(["python", "main.py"], cwd="src")
    app.run(host=args.app_host, port=args.app_port, debug=args.debug)


if __name__ == "__main__":
    main()
