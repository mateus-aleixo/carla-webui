import hashlib
import json
import launch
import os
import pkg_resources
import platform
import psutil
import sys

from modules import paths_internal, errors, timer

checksum_token = "MateusAleixo_UBI_2024"
environment_whitelist = {
    "GIT",
    "INDEX_URL",
    "WEBUI_LAUNCH_LIVE_OUTPUT",
    "PYTHONPATH",
    "REQS_FILE",
    "COMMANDLINE_ARGS",
    "IGNORE_CMD_ARGS_ERRORS",
}


def get_argv():
    res = []

    for v in sys.argv:
        res.append(v)

    return res


def pretty_bytes(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]:
        if abs(num) < 1024 or unit == "Y":
            return f"{num:.0f}{unit}{suffix}"
        num /= 1024


def get_environment():
    return {k: os.environ[k] for k in sorted(os.environ) if k in environment_whitelist}


def get_dict():
    ram = psutil.virtual_memory()
    res = {
        "Platform": platform.platform(),
        "Python": platform.python_version(),
        "Commit": launch.commit_hash(),
        "Script path": paths_internal.script_path,
        "Data path": paths_internal.data_path,
        "Checksum": checksum_token,
        "Commandline": get_argv(),
        "Exceptions": errors.get_exceptions(),
        "CPU": {
            "model": platform.processor(),
            "count logical": psutil.cpu_count(logical=True),
            "count physical": psutil.cpu_count(logical=False),
        },
        "RAM": {
            x: pretty_bytes(getattr(ram, x, 0))
            for x in [
                "total",
                "used",
                "free",
                "active",
                "inactive",
                "buffers",
                "cached",
                "shared",
            ]
            if getattr(ram, x, 0) != 0
        },
        "Environment": get_environment(),
        "Startup": timer.startup_record,
        "Packages": sorted(
            [f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set]
        ),
    }

    return res


def get():
    res = get_dict()
    text = json.dumps(res, ensure_ascii=False, indent=4)
    h = hashlib.sha256(text.encode("utf8"))
    text = text.replace(checksum_token, h.hexdigest())

    return text
