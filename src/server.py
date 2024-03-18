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

    if os.stat("root.txt").st_size != 0:
        with open("root.txt", "r") as file:
            carla_root = file.read().strip()
    else:
        carla_root = args.carla_root

        if not carla_root:
            print(
                "Please provide the path to CARLA directory in root.txt or using the --carla-dir argument"
            )
            exit(1)

    carla_executable = "CarlaUE4.sh" if os.name == "posix" else "CarlaUE4.exe"

    carla_path = os.path.abspath(carla_root)

    if not os.path.exists(carla_path):
        print(f"Could not find {carla_path}")
        exit(1)

    if carla_executable not in os.listdir(carla_root):
        print(f"Could not find {carla_executable} in {carla_root}")
        exit(1)

    carla_root = os.path.join(
        carla_root,
        carla_executable,
    )

    print("Starting CARLA...")
    subprocess.Popen(
        f"{'bash' if os.name == 'posix' else ''} {carla_root} {'--quality-level=Low' if args.low_quality else ''}",
        shell=True,
    )

    while not running(args.host, args.port):
        time.sleep(1)

    time.sleep(10)
    print("CARLA has started!")


if __name__ == "__main__":
    main()
