from dataclasses import dataclass
from idlelib.searchengine import get_selection

from .math import *
import copy


@dataclass
class Ray:
    origin: Vec2
    direction: Vec2  # normalized

    def segment_intersect(self, segment: Segment) -> Vec2 or None:
        denom = segment.normal() * self.direction
        if abs(denom) < 1e-8:
            return None
        t = (segment.a - self.origin) * segment.normal() / denom
        if t < 0:
            return None
        intersection = self.origin + self.direction * t
        if 0 <= (intersection - segment.a) * segment.a_to_b().normalize() <= segment.length():
            return intersection
        else:
            return None


@dataclass
class Mirror:
    length: float
    normal: Vec2  # normalized
    center: Vec2

    def get_segment(self):
        a = self.center + self.normal.rotate_ccw() * self.length * 0.5
        b = self.center + self.normal.rotate_cw() * self.length * 0.5
        return Segment(a, b)

    def reflect(self, ray: Ray) -> Ray:
        intersection = ray.segment_intersect(self.get_segment())
        if intersection is None:
            return copy.deepcopy(ray)
        ray_dir = (ray.direction - 2 * (ray.direction * self.normal) * self.normal).normalize()
        return Ray(intersection, ray_dir)
