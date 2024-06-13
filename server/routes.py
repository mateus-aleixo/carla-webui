import carla
from classes.agents.BehaviorAgent import BehaviorAgent
from classes.World import World
from flask import Blueprint, jsonify, request
from functions.global_functions import get_map_name
import logging
import random

# DONT DELETE ROUTE BELOW
# import base64
# import cv2
# import imutils
# import numpy as np
# import pyautogui
# import pygetwindow

# @api.route("/image", methods=["GET"])
# def image():
#     carla_window = pygetwindow.getWindowsWithTitle("CarlaUE4")[0]
#     x, y, width, height = (
#         carla_window.left,
#         carla_window.top,
#         carla_window.width,
#         carla_window.height,
#     )
#     frame = np.array(pyautogui.screenshot(region=(x, y, width, height)))
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#     frame = imutils.resize(frame, width=800)
#     _, buffer = cv2.imencode(".png", frame)
#     image = base64.b64encode(buffer).decode("utf-8")

#     return jsonify({"image": image})


world = None
agent = None


def create_api(cache):
    global world, agent
    api = Blueprint("api", __name__)

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    client = carla.Client("localhost", 2000)
    client.set_timeout(60.0)
    world = World(client.get_world())
    agent = None

    @api.route("/world_info", methods=["GET"])
    @cache.cached(timeout=60)
    def world_info():
        weather = world.world.get_weather()
        actors = world.world.get_actors()
        return jsonify(
            {
                "map": get_map_name(world.world),
                "precipitation": weather.precipitation,
                "wind_intensity": weather.wind_intensity,
                "num_actors": len(actors),
            }
        )

    @api.route("/map_info", methods=["GET"])
    @cache.cached(timeout=60)
    def map_info():
        spawn_points = [
            [sp.location.x, sp.location.y] for sp in world.map.get_spawn_points()
        ]
        actor_locations = [
            [actor.get_location().x, actor.get_location().y]
            for actor in world.world.get_actors()
        ]
        x_coords = [point[0] for point in spawn_points]
        y_coords = [point[1] for point in spawn_points]
        width = round(max(x_coords) - min(x_coords)) + 10
        height = round(max(y_coords) - min(y_coords)) + 10
        return jsonify(
            {
                "size": [width, height],
                "spawn_points": spawn_points,
                "actor_locations": actor_locations,
            }
        )

    @api.route("/weather", methods=["POST"])
    def set_weather():
        weather = request.json.get("weather")
        if not hasattr(carla.WeatherParameters, weather):
            return jsonify({"error": f"weather {weather} not found"}), 400
        world.world.set_weather(getattr(carla.WeatherParameters, weather))
        cache.clear()  # Clear cache after setting new weather
        return jsonify({"success": f"weather set to {weather}"})

    @api.route("/map", methods=["POST"])
    def set_map():
        global world
        map_name = request.json.get("map")
        if map_name == get_map_name(world.world):
            return jsonify({"error": f"map {map_name} is already loaded"}), 400
        world = World(client.load_world(map_name))
        cache.clear()  # Clear cache after loading new map
        return jsonify({"success": f"map {map_name} loaded"})

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
            return jsonify({"success": "all layers loaded"})

        if layer_states.get("NONE"):
            for layer in layers:
                world.world.unload_map_layer(
                    carla.MapLayer(getattr(carla.MapLayer, layer))
                )
            return jsonify({"success": "all layers unloaded"})

        for layer in layers:
            if layer_states.get(layer):
                world.world.load_map_layer(
                    carla.MapLayer(getattr(carla.MapLayer, layer))
                )
            else:
                world.world.unload_map_layer(
                    carla.MapLayer(getattr(carla.MapLayer, layer))
                )

        return jsonify({"success": "layers updated"})

    @api.route("/ego/add", methods=["POST"])
    def add_ego():
        global agent
        ego_vehicle = request.json.get("ego")
        world.spawn_ego(ego_vehicle)
        agent = BehaviorAgent(world.player)
        destination = random.choice(world.map.get_spawn_points()).location
        agent.set_destination(destination)
        return jsonify({"success": "ego vehicle added"})

    @api.route("/ego/remove", methods=["DELETE"])
    def remove_ego():
        global agent
        world.destroy()
        agent = None
        return jsonify({"success": "ego vehicle removed"})

    @api.route("/ego/done", methods=["GET"])
    def check_done():
        global agent
        if agent is None:
            return jsonify({"error": "agent not found"}), 404
        if agent.done():
            destination = random.choice(world.map.get_spawn_points()).location
            agent.set_destination(destination)
            return jsonify({"done": True})
        else:
            agent.run_step()
            return jsonify({"done": False})

    @api.route("/random/vehicle/add", methods=["POST"])
    def add_random_vehicle():
        random_vehicle_bp = random.choice(
            world.world.get_blueprint_library().filter("vehicle.*")
        )
        random_vehicle_bp.set_attribute("role_name", "random_vehicle")
        spawn_points = world.map.get_spawn_points()
        if spawn_points:
            random.shuffle(spawn_points)
            random_transform = spawn_points[0]
            world.world.spawn_actor(random_vehicle_bp, random_transform)
            return jsonify({"success": "random vehicle added"})
        else:
            logging.warning("No spawn points found")
            return jsonify({"error": "no spawn points found"}), 404

    @api.route("/random/vehicle/remove", methods=["DELETE"])
    def remove_random_vehicle():
        random_vehicles = [
            actor
            for actor in world.world.get_actors()
            if actor.attributes.get("role_name") == "random_vehicle"
        ]
        for vehicle in random_vehicles:
            vehicle.destroy()
        return jsonify({"success": "random vehicles removed"})

    @api.route("/destroy/all", methods=["DELETE"])
    def destroy_all():
        for actor in world.world.get_actors():
            actor.destroy()
        return jsonify({"success": "all actors destroyed"})

    return api
