from carla import Client
from dotenv import load_dotenv
from logging import DEBUG, INFO, basicConfig, info
from os import path, getenv


def create_client(host: str, port: int) -> Client:
    client = Client(host, port)

    client.set_timeout(60.0)

    return client


def main():
    load_dotenv(path.join(path.dirname(__file__), ".."))

    debug = getenv("DEBUG", False) == "True"
    host = getenv("HOST", "localhost")
    port = int(getenv("PORT", 2000))

    basicConfig(format="%(levelname)s: %(message)s", level=DEBUG if debug else INFO)
    info("listening to server %s:%s", host, port)

    client = create_client(host, port)
    world = client.get_world()


if __name__ == "__main__":
    main()
