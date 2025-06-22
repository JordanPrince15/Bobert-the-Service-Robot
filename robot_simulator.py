
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.core import CardMaker, DirectionalLight, LineSegs, AmbientLight
from direct.task import Task

class RobotSimulator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Setup
        self.setBackgroundColor(0.1, 0.1, 0.2, 1)
        self.robot_scale = 2.0  # Scaling factor
        
        # Lighting
        self.setup_lighting()
        
        # Create robot
        self.create_robot()
        
        # Camera tracking
        self.camera_distance = 15
        self.setup_camera()
        
        # Controls
        self.setup_controls()
        
        # Ground grid
        self.create_grid()
        
        print("Use Arrow Keys to move, W/S to rotate sensor, Q/E to zoom")

    def setup_lighting(self):
        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 1, 1, 1))
        self.dlnp = self.render.attachNewNode(dlight)
        self.dlnp.setHpr(-45, -45, 0)
        self.render.setLight(self.dlnp)
        ambient = AmbientLight('ambient')
        ambient.setColor((0.4, 0.4, 0.4, 1))
        self.render.setLight(self.render.attachNewNode(ambient))

    def create_robot(self):
        # Main robot node
        self.robot = self.render.attachNewNode("robot")
        self.robot.setScale(self.robot_scale)
        
        # Chassis (larger)
        cm = CardMaker("chassis")
        cm.setFrame(-2, 2, -1.5, 1.5)  # Bigger base
        chassis = self.robot.attachNewNode(cm.generate())
        chassis.setZ(0.75)
        chassis.setColor(0.3, 0.3, 0.3, 1)
        
        # Wheels (larger)
        wheel_cm = CardMaker("wheel")
        wheel_cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        positions = [
            (-1.8, -1.5, -0.5), (-1.8, 1.5, -0.5),
            (1.8, -1.5, -0.5), (1.8, 1.5, -0.5)
        ]
        for pos in positions:
            wheel = self.robot.attachNewNode(wheel_cm.generate())
            wheel.setPos(pos)
            wheel.setColor(0.1, 0.1, 0.1, 1)
        
        # Sensor (more visible)
        self.sensor_pivot = self.robot.attachNewNode("sensor_pivot")
        self.sensor_pivot.setZ(1.5)
        sensor = self.sensor_pivot.attachNewNode(wheel_cm.generate())
        sensor.setScale(0.5, 1.5, 0.5)
        sensor.setColor(1, 0, 0, 1)

    def setup_camera(self):
        # Camera follows robot
        self.cam_pivot = self.robot.attachNewNode("cam_pivot")
        self.cam_pivot.setPos(0, 0, 2)
        self.camera.reparentTo(self.cam_pivot)
        self.camera.setPos(0, -self.camera_distance, self.camera_distance/3)
        self.camera.lookAt(self.cam_pivot)
        
        # Add camera task
        self.taskMgr.add(self.update_camera, "update_camera")

    def update_camera(self, task):
        # Smooth camera follow
        self.camera.setPos(
            self.camera.getX() * 0.9 + (0) * 0.1,
            self.camera.getY() * 0.9 + (-self.camera_distance) * 0.1,
            self.camera.getZ() * 0.9 + (self.camera_distance/3) * 0.1
        )
        self.camera.lookAt(self.cam_pivot)
        return Task.cont

    def setup_controls(self):
        # Movement
        self.accept("arrow_up", self.move_robot, ["forward"])
        self.accept("arrow_down", self.move_robot, ["backward"])
        self.accept("arrow_left", self.rotate_robot, ["left"])
        self.accept("arrow_right", self.rotate_robot, ["right"])
        
        # Sensor control
        self.accept("w", self.rotate_sensor, ["left"])
        self.accept("s", self.rotate_sensor, ["right"])
        
        # Camera zoom
        self.accept("q", self.zoom_camera, ["in"])
        self.accept("e", self.zoom_camera, ["out"])

    def move_robot(self, direction):
        speed = 0.5 if direction == "forward" else -0.5
        self.robot.setY(self.robot, speed)

    def rotate_robot(self, direction):
        angle = 3 if direction == "left" else -3
        self.robot.setH(self.robot, angle)

    def rotate_sensor(self, direction):
        angle = 5 if direction == "left" else -5
        self.sensor_pivot.setH(self.sensor_pivot.getH() + angle)

    def zoom_camera(self, direction):
        change = 1 if direction == "in" else -1
        self.camera_distance = max(5, min(20, self.camera_distance + change))

    def create_grid(self):
        grid_lines = LineSegs()
        grid_lines.setColor(1, 1, 1, 1)  # White color
        grid_lines.setThickness(1)
        
        size = 20
        step = 2
        for i in range(-size, size+1, step):
            grid_lines.moveTo(i, -size, 0)
            grid_lines.drawTo(i, size, 0)
            grid_lines.moveTo(-size, i, 0)
            grid_lines.drawTo(size, i, 0)
        
        self.grid = self.render.attachNewNode(grid_lines.create())
        self.grid.setZ(-0.1)  # Slightly below robot

sim = RobotSimulator()
sim.run()
