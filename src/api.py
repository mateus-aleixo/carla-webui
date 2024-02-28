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


def load_map(map_number):
    print(client.get_available_maps())
    map_name = f"Town0{map_number}"

    if map_name != sim_world.get_map().name.split("/")[-1]:
        client.load_world(map_name)
        logging.info("loaded map Town0%s", map_number)
    else:
        logging.info("map Town0%s is already loaded", map_number)


def load_default_map():
    map_name = "Town10HD_Opt"

    if sim_world.get_map().name.split("/")[-1] != map_name:
        client.load_world(map_name)
        logging.info("loaded map %s", map_name)
    else:
        logging.info("map %s is already loaded", map_name)
