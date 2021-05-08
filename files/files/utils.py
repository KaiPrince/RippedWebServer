from typing import Callable
from .const import ALLOWED_EXTENSIONS

from threading import Timer


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def copyfile(source, dest, buffer_size=1024 * 1024):
    """
    Copy a file from source to dest. source and dest
    must be file-like objects, i.e. any object with a read or
    write method, like for example StringIO.
    """
    while True:
        copy_buffer = source.read(buffer_size)
        if not copy_buffer:
            break
        dest.write_bytes(copy_buffer)


def periodically_do(func: Callable, interval_in_seconds: float):
    def _do():
        func()
        Timer(interval_in_seconds, _do).start()

    Timer(interval_in_seconds, _do).start()
