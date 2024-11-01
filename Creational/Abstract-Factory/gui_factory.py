"""
Converted from a pseudo-code at https://refactoring.guru/design-patterns/abstract-factory
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class GUIFactory(ABC):
    """
    The abstract factory interface declares a set of methods that
    return different abstract products. These products are called
    a family and are related by a high-level theme or concept.
    Products of one family are usually able to collaborate among
    themselves. A family of products may have several variants,
    but the products of one variant are incompatible with the
    products of another variant.
    """
    @abstractmethod
    def create_button(self) -> Button:
        raise NotImplementedError("This is an abstract class!")

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        raise NotImplementedError("This is an abstract class!")


# Concrete factories produce a family of products that belong
# to a single variant. The factory guarantees that the
# resulting products are compatible. Signatures of the concrete
# factory's methods return an abstract product, while inside
# the method a concrete product is instantiated.
# Each concrete factory has a corresponding product variant.

class WinFactory(GUIFactory):
    def create_button(self) -> Button:
        print("This creates a Windows button")
        return WinButton()

    def create_checkbox(self) -> Checkbox:
        print("This creates a Windows checkbox")
        return WinCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        print("This creates a MacOS button")
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        print("This creates a MacOS checkbox")
        return MacCheckbox()


# Each distinct product of a product family should have a base
# interface. All variants of the product must implement this
# interface.

class Button(ABC):
    """
    The base interface of a Button.

    All products can interact with each other, but proper interaction
    ispossible only between products of the same concrete variant.
    """
    @abstractmethod
    def paint(self):
        raise NotImplementedError("This is an abstract class!")


# Concrete products are created by corresponding concrete factories.
class WinButton(Button):
    def paint(self):
        print("Renders a button in Windows style.")


class MacButton(Button):
    def paint(self):
        print("Renders a button in MacOS style.")


class Checkbox(ABC):
    """The base interface of a Checkbox."""
    @abstractmethod
    def paint(self):
        raise NotImplementedError("This is an abstract class!")

class WinCheckbox(Checkbox):
    def paint(self):
        print("Renders a checkbox in Windows style.")

class MacCheckbox(Checkbox):
    def paint(self):
        print("Renders a checkbox in macOS style.")


class Application(ABC):
    """
    The client code works with factories and products only
    through abstract types: GUIFactory, Button and Checkbox. This
    lets you pass any factory or product subclass to the client
    code without breaking it.
    """
    __factory = None
    __button = None
    __checkbox = None

    def __init__(self, factory: GUIFactory, *args, **kwargs):
        self.__factory = factory

    @property
    def factory(self) -> GUIFactory:
        return self.__factory

    @property
    def button(self) -> Button:
        return self.__button

    @property
    def checkbox(self) -> Checkbox:
        return self.__checkbox

    def createUI(self):
        self.__button = self.factory.create_button()
        self.__checkbox = self.factory.create_checkbox()

    def paint(self):
        self.__button.paint()
        self.__checkbox.paint()


def main(os_type):
    """
    The application picks the factory type depending on the
    current configuration or environment settings and creates it
    at runtime (usually at the initialization stage).
    """

    if os_type == "Windows":
        factory = WinFactory()
    elif os_type == "MacOS":
        factory = MacFactory()
    else:
        raise TypeError("Unknown OS!")

    app = Application(factory)
    app.createUI()
    app.paint()


if __name__ == "__main__":
    main("MacOS")