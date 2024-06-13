import carla
import collections
import math
import weakref


class CollisionSensor(object):
    """Class for collision sensors"""

    def __init__(self, parent_actor):
        """Constructor method"""
        self.sensor = None
        self.history = []
        self._parent = parent_actor

        world = self._parent.get_world()
        blueprint = world.get_blueprint_library().find("sensor.other.collision")

        self.sensor = world.spawn_actor(
            blueprint, carla.Transform(), attach_to=self._parent
        )

        # We need to pass the lambda a weak reference to
        # self to avoid circular reference.
        weak_self = weakref.ref(self)

        self.sensor.listen(
            lambda event: CollisionSensor._on_collision(weak_self, event)
        )

    def get_collision_history(self):
        """Gets the history of collisions"""
        history = collections.defaultdict(int)

        for frame, intensity in self.history:
            history[frame] += intensity

        return history

    @staticmethod
    def _on_collision(weak_self, event):
        """On collision method"""
        self = weak_self()

        if not self:
            return

        impulse = event.normal_impulse
        intensity = math.sqrt(impulse.x**2 + impulse.y**2 + impulse.z**2)

        self.history.append((event.frame, intensity))

        if len(self.history) > 4000:
            self.history.pop(0)
