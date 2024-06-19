import carla
from carla import ColorConverter as cc
import numpy as np
import weakref


"""CameraManager class for camera management"""


class CameraManager(object):
    """Class for camera management"""

    def __init__(self, parent_actor):
        """Constructor method"""
        self.sensor = None
        self.image = None
        self._parent = parent_actor
        self.recording = False

        bound_x = 0.5 + self._parent.bounding_box.extent.x
        bound_y = 0.5 + self._parent.bounding_box.extent.y
        bound_z = 0.5 + self._parent.bounding_box.extent.z
        attachment = carla.AttachmentType

        self._camera_transforms = [
            (
                carla.Transform(
                    carla.Location(x=-2.0 * bound_x, y=+0.0 * bound_y, z=2.0 * bound_z),
                    carla.Rotation(pitch=8.0),
                ),
                attachment.SpringArmGhost,
            ),
            (
                carla.Transform(
                    carla.Location(x=+0.8 * bound_x, y=+0.0 * bound_y, z=1.3 * bound_z)
                ),
                attachment.Rigid,
            ),
            (
                carla.Transform(
                    carla.Location(x=+1.9 * bound_x, y=+1.0 * bound_y, z=1.2 * bound_z)
                ),
                attachment.SpringArmGhost,
            ),
            (
                carla.Transform(
                    carla.Location(x=-2.8 * bound_x, y=+0.0 * bound_y, z=4.6 * bound_z),
                    carla.Rotation(pitch=6.0),
                ),
                attachment.SpringArmGhost,
            ),
            (
                carla.Transform(
                    carla.Location(x=-1.0, y=-1.0 * bound_y, z=0.4 * bound_z)
                ),
                attachment.Rigid,
            ),
        ]

        self.transform_index = 1
        self.sensors = [
            ["sensor.camera.rgb", cc.Raw, "Camera RGB"],
            ["sensor.camera.depth", cc.Raw, "Camera Depth (Raw)"],
            ["sensor.camera.depth", cc.Depth, "Camera Depth (Gray Scale)"],
            [
                "sensor.camera.depth",
                cc.LogarithmicDepth,
                "Camera Depth (Logarithmic Gray Scale)",
            ],
            [
                "sensor.camera.semantic_segmentation",
                cc.Raw,
                "Camera Semantic Segmentation (Raw)",
            ],
            [
                "sensor.camera.semantic_segmentation",
                cc.CityScapesPalette,
                "Camera Semantic Segmentation (CityScapes Palette)",
            ],
            ["sensor.lidar.ray_cast", None, "Lidar (Ray-Cast)"],
        ]

        world = self._parent.get_world()
        bp_library = world.get_blueprint_library()

        for item in self.sensors:
            blp = bp_library.find(item[0])

            if item[0].startswith("sensor.camera"):
                blp.set_attribute("image_size_x", "1280")
                blp.set_attribute("image_size_y", "720")
            elif item[0].startswith("sensor.lidar"):
                blp.set_attribute("range", "50")

            item.append(blp)

        self.index = None

    def set_sensor(self, index, force_respawn=False):
        """Set a sensor"""
        index = index % len(self.sensors)
        needs_respawn = (
            True
            if self.index is None
            else (
                force_respawn or (self.sensors[index][0] != self.sensors[self.index][0])
            )
        )
        if needs_respawn:
            if self.sensor is not None:
                self.sensor.destroy()
                self.image = None
            self.sensor = self._parent.get_world().spawn_actor(
                self.sensors[index][-1],
                self._camera_transforms[self.transform_index][0],
                attach_to=self._parent,
                attachment_type=self._camera_transforms[self.transform_index][1],
            )

            # We need to pass the lambda a weak reference to
            # self to avoid circular reference.
            weak_self = weakref.ref(self)
            self.sensor.listen(
                lambda image: CameraManager._parse_image(weak_self, image)
            )

        self.index = index

    def get_camera_image(self):
        """Get camera image"""
        return self.image

    @staticmethod
    def _parse_image(weak_self, image):
        self = weak_self()
        if not self:
            return
        if self.sensors[self.index][0].startswith("sensor.lidar"):
            points = np.frombuffer(image.raw_data, dtype=np.dtype("f4"))
            points = np.reshape(points, (int(points.shape[0] / 4), 4))
            lidar_data = np.array(points[:, :2])
            lidar_data *= 720 / 100.0
            lidar_data += (0.5 * 1280, 0.5 * 720)
            lidar_data = np.fabs(lidar_data)
            lidar_data = lidar_data.astype(np.int32)
            lidar_data = np.reshape(lidar_data, (-1, 2))
            lidar_img_size = (1280, 720, 3)
            lidar_img = np.zeros(lidar_img_size)
            lidar_img[tuple(lidar_data.T)] = (255, 255, 255)
            self.image = lidar_img
        else:
            image.convert(self.sensors[self.index][1])
            array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (image.height, image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            self.image = array
        if self.recording:
            image.save_to_disk("_out/%08d" % image.frame)
