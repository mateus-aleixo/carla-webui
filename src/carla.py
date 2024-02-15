import carla
import dotenv
import logging
import os


def create_client(host, port):
    client = carla.Client(host, port)

    client.set_timeout(60.0)

    return client


def main():
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".."))

    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 2000))
    loglevel = os.getenv("LOGLEVEL", "INFO")

    if loglevel not in ["CRITICAL", "ERROR", "WARNING", "DEBUG"]:
        loglevel = logging.INFO
    else:
        loglevel = getattr(logging, loglevel)

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logging.info("listening to server %s:%s", host, port)

    client = create_client(host, port)

    if not client:
        logging.error("failed to connect to server")
        return
    else:
        logging.info("connected to server")
        return


if __name__ == "__main__":
    main()
