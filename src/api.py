import carla
import cv2
import dotenv
import glob
import logging
import os
import time

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

transforms = {
    "Town01": [
        carla.Location(x=200.0, y=165.0, z=240.0),
        carla.Rotation(pitch=-90.0, roll=90.0),
    ],
    "Town02": [
        carla.Location(x=50.0, y=0.0, z=200.0),
        carla.Rotation(pitch=-90.0, roll=90.0),
    ],
    "Town03": [
        carla.Location(x=0.0, y=0.0, z=100.0),
        carla.Rotation(pitch=-90.0),
    ],
    "Town04": [
        carla.Location(x=-50.0, y=0.0, z=550.0),
        carla.Rotation(pitch=-90.0, roll=-90.0),
    ],
    "Town05": [
        carla.Location(x=0.0, y=0.0, z=100.0),
        carla.Rotation(pitch=-90.0),
    ],
    "Town10HD_Opt": [
        carla.Location(x=0.0, y=35.0, z=160.0),
        carla.Rotation(pitch=-90.0, roll=-90.0),
    ],
}

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


def get_map_name():
    return sim_world.get_map().name.split("/")[-1]


def capture_frame():
    camera_bp = sim_world.get_blueprint_library().find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", "640")
    camera_bp.set_attribute("image_size_y", "480")
    camera_bp.set_attribute("fov", "90")
    camera_bp.set_attribute("sensor_tick", "0.1")
    map_name = get_map_name()
    transform = transforms[map_name]
    camera_transform = carla.Transform(transform[0], transform[1])
    camera = sim_world.spawn_actor(camera_bp, camera_transform)

    try:
        camera.listen(lambda image: image.save_to_disk("out/%06d.png" % image.frame))
        while len(glob.glob("out/*.png")) < 2:
            pass
    except Exception as e:
        logging.error(e)
    finally:
        camera.destroy()
        time.sleep(0.5)
        os.remove(max(glob.glob("out/*.png")))

        image = cv2.imread(glob.glob("out/*.png")[0])
        frame = cv2.imencode(".png", image)[1].tobytes()

        for file in glob.glob("out/*.png"):
            os.remove(file)

        os.rmdir("out")

        return frame


def load_map(map_number):
    if map_number == 10:
        load_default_map()
        return

    map_name = f"Town0{map_number}"

    if map_name != get_map_name():
        client.load_world(map_name)
        logging.info("loaded map Town0%s", map_number)
    else:
        logging.info("map Town0%s is already loaded", map_number)


def load_default_map():
    map_name = "Town10HD_Opt"

    if get_map_name() != map_name:
        client.load_world(map_name)
        logging.info("loaded map %s", map_name)
    else:
        logging.info("map %s is already loaded", map_name)
