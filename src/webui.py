from launch import args
from webbrowser import open_new
from website import create_app


def main():
    app = create_app()

    if args.auto_launch:
        open_new(f"http://{args.app_host}:{args.app_port}")

    app.run(host=args.app_host, port=args.app_port, debug=args.flask_debug)


if __name__ == "__main__":
    main()
