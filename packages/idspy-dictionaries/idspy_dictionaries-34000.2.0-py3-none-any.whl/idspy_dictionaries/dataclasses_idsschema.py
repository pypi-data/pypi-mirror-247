from dataclasses import dataclass, field, fields
from pprint import pprint
from sys import version_info
from idspy_dictionaries._version import _IDSPY_VERSION, _IDSPY_IMAS_DD_GIT_COMMIT, \
                                        _IDSPY_IMAS_DD_VERSION, _IDSPY_INTERNAL_VERSION

default_version = (3, 10)
min_version = (3, 9)
cur_version = version_info

__IDSPY_USE_SLOTS = True


def idspy_dataclass(*args, **kwargs):
    # Check Python version
    has_slots = version_info >= default_version
    if not has_slots:
        # Add or modify the 'slots' argument based on Python version
        if 'slots' in kwargs:
            kwargs.pop('slots')

    # Use the original dataclass decorator
    return dataclass(*args, **kwargs)


@idspy_dataclass(slots=__IDSPY_USE_SLOTS, frozen=True)
class IdsVersion:
    idspy_version: str = field(default=_IDSPY_VERSION)
    imas_dd_git_commit: str = field(default=_IDSPY_IMAS_DD_GIT_COMMIT)
    imas_dd_version: str = field(default=_IDSPY_IMAS_DD_VERSION)
    idspy_internal_version: str = field(default=_IDSPY_INTERNAL_VERSION)


@idspy_dataclass(slots=__IDSPY_USE_SLOTS)
class IdsBaseClass:
    """
        Base class used for all the IDS
    """
    max_repr_length: int = 64
    version: IdsVersion = IdsVersion()

    @property
    def print_ids(self) -> object:
        """
            print IDS field values
        """
        pprint(f"current ids : {self}", indent=2)
        return None

    def __repr__(self):
        class_fields = fields(self)
        field_list = []
        for f in class_fields:
            value = getattr(self, f.name)
            if len(repr(value)) > self.max_repr_length:
                value = repr(value)[:self.max_repr_length] + "..."
            field_list.append(f"{f.name}={value}")
        return f"{self.__class__.__qualname__}(" + ", ".join(field_list) + ")"
