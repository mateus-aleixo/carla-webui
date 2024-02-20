import carla
import dotenv
import logging
import os

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

dotenv.load_dotenv(dotenv_path=dotenv_path)

host = os.getenv("HOST", "localhost")
port = int(os.getenv("PORT", 2000))
loglevel = os.getenv("LOGLEVEL", "INFO")
sync = os.getenv("SYNC", False) == "True"

os.remove(dotenv_path)

if loglevel not in ["CRITICAL", "ERROR", "WARNING", "DEBUG"]:
    loglevel = logging.INFO
else:
    loglevel = getattr(logging, loglevel)

logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
logging.info("listening to server %s:%s", host, port)

client = None
traffic_manager = None
sim_world = None

try:
    client = carla.Client(host, port)
    client.set_timeout(60.0)

    traffic_manager = client.get_trafficmanager()
    sim_world = client.get_world()

    if sync:
        settings = sim_world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05

        sim_world.apply_settings(settings)
        traffic_manager.set_synchronous_mode(True)
except Exception as e:
    logging.error(e)


def invalid():
    return sim_world is None


def change_weather(number):
    if invalid():
        raise Exception("World is not initialized")

    weather = carla.WeatherParameters(number)
    sim_world.set_weather(weather)
