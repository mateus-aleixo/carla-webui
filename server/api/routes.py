import base64
import carla
from classes.World import World
from flask import Blueprint, jsonify, request
from functions.global_functions import (
    get_map_name,
    has_ego_vehicle,
    get_actors,
    get_vehicles,
)
import io
import logging
import matplotlib.pyplot as plt
import random


"""API routes for the CARLA world."""


world = None


def create_api(cache):
    """Create the API routes for the CARLA world."""
    global world
    api = Blueprint("api", __name__)

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    client = carla.Client("localhost", 2000)
    client.set_timeout(60.0)
    world = World(client.get_world())

    @api.route("/world_info", methods=["GET"])
    @cache.cached(timeout=1)
    def world_info():
        """Get the world information from the CARLA world."""
        weather = world.world.get_weather()
        vehicles = get_vehicles(world)

        return jsonify(
            {
                "map": get_map_name(world.world),
                "precipitation": weather.precipitation,
                "wind_intensity": weather.wind_intensity,
                "num_vehicles": len(vehicles),
            }
        )

    @api.route("/vehicles", methods=["GET"])
    @cache.cached(timeout=1)
    def locations():
        """Get the actor locations from the CARLA world."""
        actors = get_actors(world)
        vehicles = get_vehicles(world)

        sign_locations = []
        spectator_location = []
        for actor in actors:
            if actor.type_id == "traffic.traffic_light":
                sign_locations.append([actor.get_location().x, actor.get_location().y])
            elif actor.type_id == "spectator":
                spectator_location = [actor.get_location().x, actor.get_location().y]
            else:
                pass

        vehicle_locations = []
        ego_location = []

        for vehicle in vehicles:
            if vehicle.attributes.get("role_name") == "random_vehicle":
                vehicle_locations.append(
                    [vehicle.get_location().x, vehicle.get_location().y]
                )
            elif vehicle.attributes.get("role_name") == "ego_vehicle":
                ego_location = [vehicle.get_location().x, vehicle.get_location().y]
            else:
                pass

        return jsonify(
            {
                "sign_locations": sign_locations,
                "vehicle_locations": vehicle_locations,
                "ego_location": ego_location,
                "spectator_location": spectator_location,
            }
        )

    @api.route("/map_info", methods=["GET"])
    @cache.cached(timeout=1)
    def map_info():
        """Get the map information from the CARLA world."""
        spawn_points = [
            [sp.location.x, sp.location.y]
            for sp in world.world.get_map().get_spawn_points()
        ]
        x_coords = [point[0] for point in spawn_points]
        y_coords = [point[1] for point in spawn_points]
        width = round(max(x_coords) - min(x_coords)) + 10
        height = round(max(y_coords) - min(y_coords)) + 10
        return jsonify(
            {
                "size": [width, height],
                "spawn_points": spawn_points,
            }
        )

    @api.route("/ego/vehicle", methods=["GET"])
    def has_ego():
        """Check if the ego vehicle exists in the CARLA world."""
        return jsonify({"has_ego": has_ego_vehicle(world.world)})

    @api.route("/ego/sensors", methods=["GET"])
    def ego_sensors():
        """Get the sensor data from the ego vehicle."""
        ego_vehicle = has_ego_vehicle(world.world)

        if not ego_vehicle:
            return jsonify({"error": "ego vehicle not found"}), 404

        gnss_sensor = world.gnss_sensor
        camera_manager = world.camera_manager

        if gnss_sensor is None or camera_manager is None:
            return jsonify({"error": "sensors not found"}), 404

        gnss_data = gnss_sensor.get_data()
        camera_image = camera_manager.get_camera_image()

        buf = io.BytesIO()
        plt.imsave(buf, camera_image, format="png")
        image_data = buf.getvalue()
        image = base64.b64encode(image_data).decode("utf-8")

        return jsonify(
            {
                "gnss_data": gnss_data,
                "image": image,
            }
        )

    @api.route("/weather", methods=["POST"])
    def set_weather():
        """Set the weather in the CARLA world."""
        weather = request.json.get("weather")
        if not hasattr(carla.WeatherParameters, weather):
            return jsonify({"error": f"weather {weather} not found"}), 400
        world.world.set_weather(getattr(carla.WeatherParameters, weather))
        cache.clear()  # Clear cache after setting new weather
        return jsonify({"success": f"weather set to {weather}"}), 200

    @api.route("/map", methods=["POST"])
    def set_map():
        """Load a new map in the CARLA world."""
        global world
        map_name = request.json.get("map")
        if map_name == get_map_name(world.world):
            return jsonify({"error": f"map {map_name} is already loaded"}), 400
        world = World(client.load_world(map_name))
        cache.clear()  # Clear cache after loading new map
        return jsonify({"success": f"map {map_name} loaded"}), 200

    @api.route("/layers", methods=["POST"])
    def set_layers():
        """Load or unload map layers in the CARLA world."""
        layers = [
            "Buildings",
            "Decals",
            "Foliage",
            "Ground",
            "ParkedVehicles",
            "Particles",
            "Props",
            "StreetLights",
            "Walls",
        ]

        layer_states = request.json.get("layers", {})

        if layer_states.get("All"):
            for layer in layers:
                world.world.load_map_layer(
                    carla.MapLayer(getattr(carla.MapLayer, layer))
                )
            return jsonify({"success": "all layers loaded"}), 200

        if layer_states.get("NONE"):
            for layer in layers:
                world.world.unload_map_layer(
                    carla.MapLayer(getattr(carla.MapLayer, layer))
                )
            return jsonify({"success": "all layers unloaded"}), 200

        for layer in layers:
            if layer_states.get(layer):
                world.world.load_map_layer(
                    carla.MapLayer(getattr(carla.MapLayer, layer))
                )
            else:
                world.world.unload_map_layer(
                    carla.MapLayer(getattr(carla.MapLayer, layer))
                )

        return jsonify({"success": "layers updated"}), 200

    @api.route("/ego/add", methods=["POST"])
    def add_ego():
        """Add an ego vehicle to the CARLA world."""
        ego_vehicle = request.json.get("ego")
        world.spawn_ego(ego_vehicle)
        return jsonify({"success": "ego vehicle added"}), 200

    @api.route("/ego/remove", methods=["DELETE"])
    def remove_ego():
        """Remove the ego vehicle from the CARLA world."""
        world.destroy()
        return jsonify({"success": "ego vehicle removed"}), 200

    @api.route("/random/vehicle/add", methods=["POST"])
    def add_random_vehicle():
        """Add a random vehicle to the CARLA world."""
        random_vehicle_bp = random.choice(
            world.world.get_blueprint_library().filter("vehicle.*")
        )
        random_vehicle_bp.set_attribute("role_name", "random_vehicle")
        spawn_points = world.world.get_map().get_spawn_points()
        if spawn_points:
            random.shuffle(spawn_points)
            random_transform = spawn_points[0]
            random_vehicle = world.world.try_spawn_actor(
                random_vehicle_bp, random_transform
            )

            if random_vehicle is None:
                logging.warning("Random vehicle could not be spawned")
                return jsonify({"error": "random vehicle could not be spawned"}), 400
            else:
                random_vehicle.set_autopilot(True)
                return jsonify({"success": "random vehicle added"}), 200
        else:
            logging.warning("No spawn points found")
            return jsonify({"error": "no spawn points found"}), 404

    @api.route("/random/vehicle/remove", methods=["DELETE"])
    def remove_random_vehicle():
        """Remove all random vehicles from the CARLA world."""
        random_vehicles = [
            actor
            for actor in get_actors(world)
            if actor.attributes.get("role_name") == "random_vehicle"
        ]
        for vehicle in random_vehicles:
            vehicle.destroy()
        return jsonify({"success": "random vehicles removed"}), 200

    @api.route("/random/vehicles", methods=["POST"])
    def n_random_vehicles():
        """Add or remove random vehicles from the CARLA world."""
        num_vehicles = request.json.get("num_vehicles")
        random_vehicles = [
            actor
            for actor in get_actors(world)
            if actor.attributes.get("role_name") == "random_vehicle"
        ]
        n = len(random_vehicles)
        dif = num_vehicles - n
        vehicles_spawned = 0

        if dif > 0:
            for _ in range(dif):
                _, status_code = add_random_vehicle()

                if status_code != 200:
                    return (
                        jsonify(
                            {
                                "error": f"random vehicle could not be spawned",
                                "vehicles_spawned": vehicles_spawned,
                            }
                        ),
                        status_code,
                    )
                else:
                    vehicles_spawned += 1

            return jsonify({"success": f"{dif} random vehicles added"}), 200
        elif dif < 0:
            for random_vehicle in random_vehicles[dif:]:
                random_vehicle.destroy()
            return jsonify({"success": f"{-dif} random vehicles removed"}), 200
        else:
            return jsonify({"success": "no changes"}), 200

    @api.route("/destroy/all", methods=["DELETE"])
    def destroy_all():
        """Destroy all actors in the CARLA world."""
        vehicles = get_vehicles(world)

        if len(vehicles) == 0:
            return jsonify({"error": "no actors to destroy"}), 400

        for vehicle in vehicles:
            if vehicle.attributes.get("role_name") == "ego_vehicle":
                world.destroy()
            else:
                vehicle.destroy()

        return jsonify({"success": "all vehicles destroyed"}), 200

    return api
