"""
Prototype conceptual example.
Based on https://refactoring.guru/design-patterns/prototype/python/example
"""

import copy


class SelfReferencingEntity:
    def __init__(self, *args, **kwargs) -> None:
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


class SomeComponent:
    """
    Python provides its own interface of Prototype via `copy.copy` and
    `copy.deepcopy` functions. Any class that wants to implement custom
    implementations have to override `__copy__` and `__deepcopy__` member
    functions.
    """

    def __init__(self, val: int, oblects: list, circular_ref) -> None:
        self.val = val
        self.objects = objects
        self.circular_ref = circular_ref

    def __copy__(self):
        """
        Creates a shallow copy. This method will be called whenever someone
        calls `copy.copy` with this object and the returned value is returned
        as the new shallow copy.
        """
        # First, let's create copies of the nested objects.
        objects = copy.copy(self.objects)
        circular_ref = copy.copy(self.circular_ref)

        # Then, let's clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(self.val, objects, circular_ref)
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo: dict = {}):
        """
        Create a deep copy. This method will be called whenever someone calls
        `copy.deepcopy` with this object and the returned value is returned as
        the new deep copy.

        :arg `memo`: <dict> used by the `deepcopy` library to prevent infinite
        recursive copies in instances of circular references. Pass it to all
        the `deepcopy` calls you make in the `__deepcopy__` implementation to
        prevent infinite recursions.
        """
        # First, create copies of the nested objects.
        objects = copy.deepcopy(self.objects, memo)
        circular_ref = copy.deepcopy(self.circular_ref, memo)

        # Then, clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(self.val, objects, circular_ref)
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new


if __name__ == "__main__":
    objects = [1, {1, 2, 3}, [1, 2, 3]]
    circular_ref = SelfReferencingEntity()
    component = SomeComponent(23, objects, circular_ref)
    circular_ref.set_parent(component)

    shallow_copied_component = copy.copy(component)
    # Change the list in `shallow_copied_component` and see if it changes in
    # component.
    shallow_copied_component.objects.append("another object")
    if component.objects[-1] == "another object":
        print(
            "Adding elements to `shallow_copied_component`'s "
            "list of `objects` adds it to `component`'s `objects`"
        )
    else:
        print(
            "Adding elements to `shallow_copied_component`'s "
            "list of `objects` doesn't add it to `component`'s `objects`"
        )

    # Change the set in the list of objects.
    component.objects[1].add(4)
    if 4 in shallow_copied_component.objects[1]:
        print(
            "Changing objects in the `component`'s objects "
            "changes that object in `shallow_copied_component`'s objects."
        )
    else:
        print(
            "Changing objects in the `component`'s objects doesn't "
            "that object in `shallow_copied_component`'s objects."
        )


    deep_copied_component = copy.deepcopy(component)
    # Change the list in deep_copied_component and see if it changes in
    # component.
    deep_copied_component.objects.append("one more object")
    if component.objects[-1] == "one more object":
        print(
            "Adding elements to `deep_copied_component`'s "
            "objects adds it to `component`'s objects."
        )
    else:
        print(
            "Adding elements to `deep_copied_component`'s "
            "objects doesn't add it to `component`'s objects."
        )

    # Change the set in the list of objects.
    component.objects[1].add(10)
    if 10 in deep_copied_component.objects[1]:
        print(
            "Changing objects in the `component`'s objects "
            "changes that object in `deep_copied_component`'s objects."
        )
    else:
        print(
            "Changing objects in the `component`'s objects "
            "doesn't change that object in `deep_copied_component`'s objects."
        )

    print(
        f"id(deep_copied_component.circular_ref.parent): "
        f"{id(deep_copied_component.circular_ref.parent)}"
    )
    print(
        f"id(deep_copied_component.circular_ref.parent.circular_ref.parent): "
        f"{id(deep_copied_component.circular_ref.parent.circular_ref.parent)}"
    )
    print(
        "^^ This shows that deepcopied objects contain same reference, they "
        "are not cloned repeatedly."
    )
