"""
Proptotype example.
Converted from a pseudo-code:
https://refactoring.guru/design-patterns/prototype
"""

import copy
from abc import ABC, abstractmethod

    
class Shape(ABC):
    def __init__(self, X: int, Y: int, color: str, *args, **kwargs) -> None:
        """`Shape` is a self-referencing entity."""
        self.parent = None

        self.X = X
        self.Y = Y
        self.color = color

    def set_parent(self, parent):
        self.parent = parent

    @property
    def basic(self) -> tuple:
        return (self.X, self.Y, self.color)


class Rectangle(Shape):
    def __init__(self, X: int, Y: int, color: str, *args, **kwargs) -> None:
        super().__init__(X, Y, color)

        self.width = int(kwargs.get('width', 20))
        self.height = int(kwargs.get('height', 10))

    def __copy__(self):
        """
        Shallow copy - useful for creating "borg" rectangles that behave
        as one (changing one parameter in one will change it in others).
        """
        basic = copy.copy(self.basic)
        measurements = copy.copy(self.measurements)

        # Clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(*basic, **measurements)
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo: dict = {}):
        """
        Deep copy - for creating lone rectangles that behave independently
        of the rest.

        :arg `memo`: <dict> used by the `deepcopy` library to prevent infinite
        recursive copies in instances of circular references. Pass it to all
        the `deepcopy` calls you make in the `__deepcopy__` implementation to
        prevent infinite recursions.
        """
        basic = copy.deepcopy(self.basic, memo)
        measurements = copy.deepcopy(self.measurements, memo)

        # Clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(*basic, **measurements)
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new

    @property
    def measurements(self):
        return {"width": self.width, "height": self.height}

    @measurements.setter
    def measurements(self, measurements: dict) -> None:
        self.width = measurements["width"]
        self.height = measurements["height"]


class Circle(Shape):
    def __init__(self, X: int, Y: int, color: str, *args, **kwargs) -> None:
        super().__init__(X, Y, color)
        self.radius = int(kwargs.get('radius', 20))

    def __copy__(self):
        """Shallow copy."""
        basic = copy.copy(self.basic)
        radius = {"radius": self.radius}

        # Clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(*basic, **radius)
        new.__dict__.update(self.__dict__)

        return new
    
    def __deepcopy__(self, memo: dict = {}):
        """Deep copy."""
        basic = copy.deepcopy(self.basic, memo)
        radius = copy.deepcopy({"radius": self.radius}, memo)

        # Clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(*basic, **radius)
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new

class Application:
    #TODO:
    # 1. array of shapes
    # 2. methods: `clone` for shallow copy, `duplicate` for deep copy
    def __init__(self, *args, **kwargs) -> None:
        self._shapes = []
        