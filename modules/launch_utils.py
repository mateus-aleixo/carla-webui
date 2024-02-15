import os
import platform
import re
import subprocess
import sys

from functools import lru_cache
from importlib import metadata, util
from modules import cmd_args, logging_config
from modules.paths_internal import script_path
from modules.timer import startup_timer

args, _ = cmd_args.parser.parse_known_args()
logging_config.setup_logging(args.loglevel)

python = sys.executable
git = os.environ.get("GIT", "git")
index_url = os.environ.get("INDEX_URL", "")
default_command_live = os.environ.get("WEBUI_LAUNCH_LIVE_OUTPUT") == "1"


def run(command, desc=None, errdesc=None, custom_env=None, live=default_command_live):
    if desc is not None:
        print(desc)

    run_kwargs = {
        "args": command,
        "shell": True,
        "env": os.environ if custom_env is None else custom_env,
        "encoding": "utf-8",
        "errors": "ignore",
    }

    if not live:
        run_kwargs["stdout"] = run_kwargs["stderr"] = subprocess.PIPE

    result = subprocess.run(**run_kwargs)

    if result.returncode != 0:
        error_bits = [
            f"{errdesc or 'Error running command'}.",
            f"Command: {command}",
            f"Error code: {result.returncode}",
        ]

        if result.stdout:
            error_bits.append(f"stdout: {result.stdout}")
        if result.stderr:
            error_bits.append(f"stderr: {result.stderr}")

        raise RuntimeError("\n".join(error_bits))

    return result.stdout or ""


def is_installed(package):
    try:
        dist = metadata.distribution(package)
    except metadata.PackageNotFoundError:
        try:
            spec = util.find_spec(package)
        except ModuleNotFoundError:
            return False

        return spec is not None

    return dist is not None


def run_pip(command, desc=None, live=default_command_live):
    if args.skip_install:
        return

    index_url_line = f" --index-url {index_url}" if index_url != "" else ""

    return run(
        f'"{python}" -m pip {command} --prefer-binary{index_url_line}',
        desc=f"Installing {desc}",
        errdesc=f"Couldn't install {desc}",
        live=live,
    )


def check_run_python(code):
    result = subprocess.run([python, "-c", code], shell=False, capture_output=True)

    return result.returncode == 0


def check_python_version():
    is_windows = platform.system() == "Windows"
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro

    if is_windows:
        supported_majors = [3]
        supported_minors = [0, 7, 8]
    else:
        supported_majors = [2, 3]
        supported_minors = [7, 8]

    if not (major in supported_majors and minor in supported_minors):
        import modules.errors

        modules.errors.print_error_explanation(
            f"""
            INCOMPATIBLE PYTHON VERSION
            
            This program is tested with 3.8.18 Python, but you have {major}.{minor}.{micro}.
            If you encounter an error regarding unsuccessful package (library) installation,
            please downgrade (or upgrade) to the latest version of 3.8 Python
            and delete current Python and "venv" folder in WebUI's directory.

            You can download 3.8 Python from here: https://www.python.org/downloads/release/python-3818/

            Use --skip-python-version-check to suppress this warning.                                     
        """
        )


@lru_cache()
def commit_hash():
    try:
        return subprocess.check_output(
            [git, "-C", script_path, "rev-parse", "HEAD"], shell=False, encoding="utf8"
        ).strip()
    except Exception:
        return "<none>"


re_requirement = re.compile(r"\s*([-_a-zA-Z0-9]+)\s*(?:==\s*([-+_.a-zA-Z0-9]+))?\s*")


def requirements_met(requirements_file):
    import packaging.version

    with open(requirements_file, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip() == "":
                continue

            m = re.match(re_requirement, line)

            if m is None:
                return False

            package = m.group(1).strip()
            version_required = (m.group(2) or "").strip()

            if version_required == "":
                continue

            try:
                version_installed = metadata.version(package)
            except Exception:
                return False

            if packaging.version.parse(version_required) != packaging.version.parse(
                version_installed
            ):
                return False

    return True


def version_check(commit):
    try:
        import requests

        commits = requests.get(
            "https://api.github.com/repos/mateus-aleixo/carla-webui/branches/test"
        ).json()

        if commit != "<none>" and commits["commit"]["sha"] != commit:
            print("--------------------------------------------------------")
            print("| You are not up to date with the most recent release. |")
            print("| Consider running `git pull` to update.               |")
            print("--------------------------------------------------------")
        elif commits["commit"]["sha"] == commit:
            print("You are up to date with the most recent release.")
        else:
            print("Not a git clone, can't perform version check.")
    except Exception as e:
        print("version check failed", e)


def prepare_environment():
    requirements_file = os.environ.get("REQS_FILE", "requirements_versions.txt")

    if not args.skip_python_version_check:
        check_python_version()

    startup_timer.record("checks")

    commit = commit_hash()

    startup_timer.record("git version info")

    print(f"Python {sys.version}")
    print(f"Commit hash: {commit}")

    if not os.path.isfile(requirements_file):
        requirements_file = os.path.join(script_path, requirements_file)

    if not requirements_met(requirements_file):
        run_pip(f'install -r "{requirements_file}"', "requirements")
        startup_timer.record("install requirements")

    if args.update_check:
        version_check(commit)
        startup_timer.record("check version")

    if "--exit" in sys.argv:
        print("Exiting because of --exit argument")
        exit(0)


def start():
    import webui

    print(f"Launching Web UI with arguments: {' '.join(sys.argv[1:])}")
    webui.main()
