import argparse
import os

modules_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.dirname(modules_path)

parser_pre = argparse.ArgumentParser(add_help=False)
parser_pre.add_argument(
    "--data-dir",
    default=os.path.dirname(modules_path),
    type=str,
    help="base path where all user data is stored",
    metavar="D",
)
cmd_opts_pre = parser_pre.parse_known_args()[0]

data_path = cmd_opts_pre.data_dir
