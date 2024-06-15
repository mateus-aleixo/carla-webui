import carla
import re


def get_map_name(world):
    """Method to get map name"""
    return world.get_map().name.split("/")[-1]


def find_weather_presets():
    """Method to find weather presets"""
    rgx = re.compile(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)")

    def name(x):
        return " ".join(m.group(0) for m in rgx.finditer(x))

    presets = [x for x in dir(carla.WeatherParameters) if re.match("[A-Z].+", x)]
    return [(getattr(carla.WeatherParameters, x), name(x)) for x in presets]


def get_actor_blueprints(world, filter, generation):
    """Method to get actor blueprints"""
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2, 3]:
            bps = [
                x for x in bps if int(x.get_attribute("generation")) == int_generation
            ]
            return bps
        else:
            print("Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except:
        print("Warning! Actor Generation is not valid. No actor will be spawned.")
        return []


def has_ego_vehicle(world):
    """Method to check if ego vehicle exists"""
    for actor in world.get_actors().filter("vehicle.*"):
        if actor.attributes.get("role_name") == "ego_vehicle":
            return True

    return False
