import carla
import weakref


"""GnssSensor class for GNSS sensor"""


class GnssSensor(object):
    """Class for GNSS sensors"""

    def __init__(self, parent_actor):
        """Constructor method"""
        self.sensor = None
        self._parent = parent_actor
        self.lat = 0.0
        self.lon = 0.0

        world = self._parent.get_world()
        blueprint = world.get_blueprint_library().find("sensor.other.gnss")

        self.sensor = world.spawn_actor(
            blueprint,
            carla.Transform(carla.Location(x=1.0, z=2.8)),
            attach_to=self._parent,
        )

        # We need to pass the lambda a weak reference to
        # self to avoid circular reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: GnssSensor._on_gnss_event(weak_self, event))

    def get_data(self):
        """Get data method"""
        return {"lat": self.lat, "lon": self.lon}

    @staticmethod
    def _on_gnss_event(weak_self, event):
        """GNSS method"""
        self = weak_self()

        if not self:
            return

        self.lat = event.latitude
        self.lon = event.longitude
