from launch import args
from subprocess import Popen
from webbrowser import open_new
from website import create_app


def main():
    with open(".env", "w") as file:
        file.write(f"HOST={args.host}\n")
        file.write(f"PORT={args.port}\n")
        file.write(f"LOGLEVEL={args.loglevel}\n")

    app = create_app()

    Popen(["python", "api.py"], cwd="src")

    if args.autolaunch and not args.flask_debug:
        open_new(f"http://{args.app_host}:{args.app_port}")

    app.run(host=args.app_host, port=args.app_port, debug=args.flask_debug)


if __name__ == "__main__":
    main()
