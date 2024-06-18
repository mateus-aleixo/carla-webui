import carla
from classes.CameraManager import CameraManager
from classes.GnssSensor import GnssSensor
from functions.global_functions import find_weather_presets, get_actor_blueprints
import random
import sys


class World(object):
    """Class representing the surrounding environment"""

    def __init__(self, carla_world):
        """Constructor method"""
        self.world = carla_world

        try:
            self.map = self.world.get_map()
        except RuntimeError as error:
            print("RuntimeError: {}".format(error))
            print("The server could not send the OpenDRIVE (.xodr) file:")
            print(
                "Make sure it exists, has the same name of your town, and is correct."
            )
            sys.exit(1)

        self.player = None
        self.gnss_sensor = None
        self.camera_manager = None
        self._weather_presets = find_weather_presets()
        self._weather_index = 0
        self._actor_filter = "vehicle.*"
        self._actor_generation = "2"
        self.recording_enabled = False
        self.recording_start = 0

    def spawn_ego(self, ego=None):
        """Restart the world"""
        # Keep same camera config if the camera manager exists.
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_id = (
            self.camera_manager.transform_index
            if self.camera_manager is not None
            else 0
        )

        if ego is None:
            # Get a random blueprint.
            blueprint_list = get_actor_blueprints(
                self.world, self._actor_filter, self._actor_generation
            )

            if not blueprint_list:
                raise ValueError(
                    "Couldn't find any blueprints with the specified filters"
                )

            blueprint = random.choice(blueprint_list)
        else:
            blueprint = self.world.get_blueprint_library().find(ego)

        blueprint.set_attribute("role_name", "ego_vehicle")

        if blueprint.has_attribute("color"):
            color = random.choice(blueprint.get_attribute("color").recommended_values)
            blueprint.set_attribute("color", color)

        # Spawn the player.
        if self.player is not None:
            spawn_point = self.player.get_transform()
            spawn_point.location.z += 2.0
            spawn_point.rotation.roll = 0.0
            spawn_point.rotation.pitch = 0.0

            self.destroy()
            self.player = self.world.try_spawn_actor(blueprint, spawn_point)
            self.modify_vehicle_physics(self.player)

        while self.player is None:
            if not self.map.get_spawn_points():
                print("There are no spawn points available in your map/town.")
                print("Please add some Vehicle Spawn Point to your UE4 scene.")
                sys.exit(1)

            spawn_points = self.map.get_spawn_points()
            spawn_point = (
                random.choice(spawn_points) if spawn_points else carla.Transform()
            )

            self.player = self.world.try_spawn_actor(blueprint, spawn_point)
            self.modify_vehicle_physics(self.player)

        # Set up the sensors.
        self.gnss_sensor = GnssSensor(self.player)
        self.camera_manager = CameraManager(self.player)
        self.camera_manager.transform_index = cam_pos_id
        self.camera_manager.set_sensor(cam_index)

        # Set the player's autopilot.
        self.player.set_autopilot(True)

    def next_weather(self, reverse=False):
        """Get next weather setting"""
        self._weather_index += -1 if reverse else 1
        self._weather_index %= len(self._weather_presets)
        preset = self._weather_presets[self._weather_index]
        self.player.get_world().set_weather(preset[0])

    def modify_vehicle_physics(self, actor):
        # If actor is not a vehicle, we cannot use the physics control
        try:
            physics_control = actor.get_physics_control()
            physics_control.use_sweep_wheel_collision = True
            actor.apply_physics_control(physics_control)
        except Exception:
            pass

    def destroy_sensors(self):
        """Destroy sensors"""
        self.camera_manager.sensor.destroy()
        self.camera_manager.sensor = None
        self.camera_manager.index = None

    def destroy(self):
        """Destroys all actors"""
        actors = [
            self.camera_manager.sensor,
            self.gnss_sensor.sensor,
            self.player,
        ]

        for actor in actors:
            if actor is not None:
                actor.destroy()

        self.player = None
