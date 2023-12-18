import argparse
import concurrent.futures
import contextlib
import subprocess
import os
import gzip
import shutil
import tempfile


class ArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        message = f"failed to parse command line: {message}"
        raise RuntimeError(message)


def z_open(path, mode="r", z="auto", level=6, **open_kargs):
    modes = dict(
        ((first + second + third), (first + second + (third or "t")))
        for first in ("r", "w", "x", "a")
        for second in ("", "+")
        for third in ("", "t", "b"))
    mode = modes[mode]
    z_mode = "extension" if z == "auto" and mode[0] in ("w", "x") else z
    if z if isinstance(z, bool) else infer_z(path, z_mode):
        return gzip.open(path, mode, level, **open_kargs)
    return open(path, mode, **open_kargs)
    

def infer_z(path, mode="auto"):
    if mode == "extension":
        return path.lower().endswith(".gz")
    if mode == "magic":
        with open(path, "rb") as file:
            return file.read(2) == b"\x1f\x8b"
    if mode == "auto":
        try:
            return infer_z(path, "magic")
        except Exception:
            return infer_z(path, "extension")
    raise ValueError(f"invalid infer mode: {mode} (auto, magic or extension)")


def z_format(path):
    base, extension = os.path.splitext(path.lower())
    if extension.lower() == ".gz":
        base, next_extension = os.path.splitext(base)
        extension = next_extension + extension
    return extension[1:]


def all_same(iterable, empty=None):
    iterable = iter(iterable)
    try:
        reference = next(iterable)
    except StopIteration:
        return empty
    return all(value == reference for value in iterable)


def check_executable(*names):
    missing = [name for name in names if not shutil.which(name)]
    if missing:
        raise RuntimeError("executables not found: " + " ".join(missing))


@contextlib.contextmanager
def pipe(command, stdin=None, binary=False):
    arguments = dict(
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary)
    with subprocess.Popen(command, **arguments) as process:
        try:
            yield process.stdout
        finally:
            if process.wait():
                error = process.stderr.read().strip()
                error = error.decode() if binary else error
                error = f"\n{error}" if error else ""
                raise RuntimeError(f"command failed:{error}")


def parallelize(tasks, parallel=1, function=None):
    parallel = int(min(parallel or os.cpu_count(), len(tasks)))
    if function is not None:
        tasks = ([function, *task] for task in task)
    if parallel < 2:
        for task in tasks:
            target, args = task[0], task[1:]
            yield target(*args)
    else:
        with concurrent.futures.ProcessPoolExecutor(parallel) as executor:
            futures = [executor.submit(*task) for task in tasks]
        yield from concurrent.futures.as_completed(futures)


def with_tmp_dir(function, add_var=True, var_name="tmp_dir"):
    def wrapper(*args, **kargs):
        with tempfile.TemporaryDirectory() as tmp_dir:
            if add_var:
                kargs[var_name] = tmp_dir
            return function(*args, **kargs)
    return wrapper
