import os
import shutil


def invalid(value, message=None):
    message = "" if message is None else f" ({message})"
    return ValueError(f"{value}{message}")


def check_executable(*names):
    missing = [name for name in names if not shutil.which(name)]
    if missing:
        raise RuntimeError("executables not found: " + " ".join(missing))


def check_path(value, exist=None):
    if exist == "file":
        if not os.path.isfile(value):
            raise invalid(value, "file not found")
    elif exist == "dir":
        if not os.path.isdir(value):
            raise invalid(value, "directory not found")
    elif exist == "parent":
        parent = os.path.dirname(value) or ".."
        if not os.path.isdir(parent):
            raise invalid(value, "parent directory not found")
    elif exist is not None:
        raise ValueError("exist as file, dir or parent")
    return value


def check_choice(value, choices, if_none=None):
    if value is None and if_none is not None:
        value = if_none
    if value not in choices:
        raise invalid(value, f"not in {choices}")
    return value


def check_number(value, min=None, max=None, divisible=None, type=None):
    if type is not None:
        if type == float and (isinstance(value, int) or value == "nan"):
            value = float(value)
        if type == int and isinstance(value, float) and value.is_integer():
            value = int(type)
        if not isinstance(value, type):
            raise invalid(value, f"not {type}")
    if min is not None and not value >= min:
        raise invalid(value, f"not >= {min}")
    if max is not None and not value <= max:
        raise invalid(value, f"not <= {max}")
    if divisible is not None:
        if value % divisible:
            raise invalid(value, f"not divisible by {divisible}")
    return value
