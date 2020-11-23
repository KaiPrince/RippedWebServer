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
