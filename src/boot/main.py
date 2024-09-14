import renderer
from optics import *
import copy
import time

m = Mirror(length=800, normal=Vec2(2, 1).normalize(), center=Vec2(400, 300))
m2 = Mirror(length=300, normal=Vec2(1, 0).normalize(), center=Vec2(110, 300))
world = World([Ray(Vec2(100, 100), Vec2(1, 0.7))], [m, m2])
calc = Calculator(world)
calc.recalc()
frames = 0
last = time.time()
while True:
    frames += 1
    renderer.render(copy.deepcopy(calc.current_snapshot))
    frames %= 1000
    if frames == 0:
        now = time.time()
        # print("1000 frames:", (now - last), "seconds", "(" + str(1000 / (now - last)) + " FPS)")
        last = now
