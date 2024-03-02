import os
import socket
import subprocess
import time

from launch import args


def running(host, port):
    try:
        socket.create_connection((host, port))
        return True
    except ConnectionRefusedError:
        return False


def main():
    with open(".env", "w") as file:
        file.write(f"HOST={args.host}\n")
        file.write(f"PORT={args.port}\n")
        file.write(f"LOGLEVEL={args.loglevel}\n")
        file.write(f"SYNC={args.sync}\n")

    carla_dir = args.carla_dir

    if not carla_dir:
        print(
            "Please provide the path to CARLA directory using the --carla-dir argument"
        )
        exit(1)
    else:
        carla_executable = "CarlaUE4.sh" if os.name == "posix" else "CarlaUE4.exe"

        carla_path = os.path.abspath(carla_dir)

        if not os.path.exists(carla_path):
            print(f"Could not find {carla_path}")
            exit(1)

        if carla_executable not in os.listdir(carla_dir):
            print(f"Could not find {carla_executable} in {carla_dir}")
            exit(1)

    carla_dir = os.path.join(
        carla_dir,
        carla_executable,
    )

    print("Starting CARLA...")
    subprocess.Popen(
        f"{'bash' if os.name == 'posix' else ''} {carla_dir} {'--quality-level=Low' if args.low_quality else ''}",
        shell=True,
    )

    while not running(args.host, args.port):
        time.sleep(10)

    print("CARLA has started!")


if __name__ == "__main__":
    main()
