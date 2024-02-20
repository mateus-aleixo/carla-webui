from launch import args
from webbrowser import open_new
from website import create_app


def main():
    app = create_app()

    if not args.flask_debug:
        with open(".env", "w") as file:
            file.write(f"HOST={args.host}\n")
            file.write(f"PORT={args.port}\n")
            file.write(f"LOGLEVEL={args.loglevel}\n")
            file.write(f"SYNC={args.sync}\n")

        if args.autolaunch:
            open_new(f"http://{args.app_host}:{args.app_port}")

    app.run(host=args.app_host, port=args.app_port, debug=args.flask_debug)


if __name__ == "__main__":
    main()
