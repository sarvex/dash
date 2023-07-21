def _operation(name, location, **kwargs):
    return {"operation": name, "location": location, "params": dict(**kwargs)}


_noop = object()


def validate_slice(obj):
    if isinstance(obj, slice):
        raise TypeError("a slice is not a valid index for patch")


class Patch:
    """
    Patch a callback output value

    Act like a proxy of the output prop value on the frontend.

    Supported prop types: Dictionaries and lists.
    """

    def __init__(self, location=None, parent=None):
        if location is not None:
            self._location = location
        else:
            # pylint: disable=consider-using-ternary
            self._location = (parent and parent._location) or []
        self._operations = parent._operations if parent is not None else []

    def __getstate__(self):
        return vars(self)

    def __setstate__(self, state):
        vars(self).update(state)

    def __getitem__(self, item):
        validate_slice(item)
        return Patch(location=self._location + [item], parent=self)

    def __getattr__(self, item):
        if item == "tolist":
            # to_json fix
            raise AttributeError
        if item == "_location":
            return self._location
        return self._operations if item == "_operations" else self.__getitem__(item)

    def __setattr__(self, key, value):
        if key in ("_location", "_operations"):
            self.__dict__[key] = value
        else:
            self.__setitem__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)

    def __setitem__(self, key, value):
        validate_slice(key)
        if value is _noop:
            # The += set themselves.
            return
        self._operations.append(
            _operation(
                "Assign",
                self._location + [key],
                value=value,
            )
        )

    def __delitem__(self, key):
        validate_slice(key)
        self._operations.append(_operation("Delete", self._location + [key]))

    def __iadd__(self, other):
        if isinstance(other, (list, tuple)):
            self.extend(other)
        else:
            self._operations.append(_operation("Add", self._location, value=other))
        return _noop

    def __isub__(self, other):
        self._operations.append(_operation("Sub", self._location, value=other))
        return _noop

    def __imul__(self, other):
        self._operations.append(_operation("Mul", self._location, value=other))
        return _noop

    def __itruediv__(self, other):
        self._operations.append(_operation("Div", self._location, value=other))
        return _noop

    def __ior__(self, other):
        self.update(E=other)
        return _noop

    def __iter__(self):
        raise TypeError("Patch objects are write-only, you cannot iterate them.")

    def __repr__(self):
        return f"<write-only dash.Patch object at {self._location}>"

    def append(self, item):
        """Add the item to the end of a list"""
        self._operations.append(_operation("Append", self._location, value=item))

    def prepend(self, item):
        """Add the item to the start of a list"""
        self._operations.append(_operation("Prepend", self._location, value=item))

    def insert(self, index, item):
        """Add the item at the index of a list"""
        self._operations.append(
            _operation("Insert", self._location, value=item, index=index)
        )

    def clear(self):
        """Remove all items in a list"""
        self._operations.append(_operation("Clear", self._location))

    def reverse(self):
        """Reversal of the order of items in a list"""
        self._operations.append(_operation("Reverse", self._location))

    def extend(self, item):
        """Add all the items to the end of a list"""
        if not isinstance(item, (list, tuple)):
            raise TypeError(f"{item} should be a list or tuple")
        self._operations.append(_operation("Extend", self._location, value=item))

    def remove(self, item):
        """filter the item out of a list on the frontend"""
        self._operations.append(_operation("Remove", self._location, value=item))

    def update(self, E=None, **F):
        """Merge a dict or keyword arguments with another dictionary"""
        value = E or {}
        value.update(F)
        self._operations.append(_operation("Merge", self._location, value=value))

    # pylint: disable=no-self-use
    def sort(self):
        raise KeyError(
            "sort is reserved for future use, use brackets to access this key on your object"
        )

    def to_plotly_json(self):
        return {
            "__dash_patch_update": "__dash_patch_update",
            "operations": self._operations,
        }
