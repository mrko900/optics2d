from cgitb import reset

from .world import *


class Calculator:
    def __init__(self, world):
        self.current_snapshot = None
        self.reset()
        self.world = world

    def reset(self):
        self.current_snapshot = Snapshot([], [])

    def recalc(self):
        self.reset()
        self.calc_all_rays()
        for m in self.world.mirrors:
            self.current_snapshot.mirrors.append(m)

    def calc_all_rays(self):
        for ray in self.world.rays:
            path = [ray.origin]
            last_mirror = None
            for i in range(10):
                dist_to_closest = None
                closest = None
                for mirror in self.world.mirrors:
                    if mirror == last_mirror:
                        continue
                    p = ray.segment_intersect(mirror.get_segment())
                    if p:
                        dist = (p - ray.origin).length()
                        print("dist ", dist)
                        if dist_to_closest is None or dist_to_closest > dist:
                            dist_to_closest = dist
                            closest = mirror
                if closest:
                    last_mirror = closest
                    ray = closest.reflect(ray)
                    path.append(ray.origin)
                else:
                    break
            path.append(path[-1] + ray.direction)
            print("path", path)
            self.current_snapshot.ray_paths.append(path)
