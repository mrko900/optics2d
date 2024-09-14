from typing import List
from dataclasses import dataclass
from .math import *
from .elements import *


@dataclass
class World:
    rays: List['Ray']
    mirrors: List['Mirror']


@dataclass
class Snapshot:
    ray_paths: List[List['Vec2']]  # ray path
    mirrors: List['Mirror']

