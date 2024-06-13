from carla import Actor, TrafficLight
from typing import NamedTuple, Union, Literal

ObstacleDetectionResult = NamedTuple(
    "ObstacleDetectionResult",
    [
        ("obstacle_was_found", bool),
        ("obstacle", Union[Actor, None]),
        ("distance", Union[float, Literal[-1]]),
    ],
)

TrafficLightDetectionResult = NamedTuple(
    "TrafficLightDetectionResult",
    [("traffic_light_was_found", bool), ("traffic_light", Union[TrafficLight, None])],
)
