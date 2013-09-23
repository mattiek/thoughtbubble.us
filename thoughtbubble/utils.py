from thoughtbubble.models import *
import os
import hashlib

def path_and_rename(path, attr):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        chunks = getattr(instance, attr).chunks()
        md5 = hashlib.md5()
        for data in chunks:
            if not data:
                break
            md5.update(data)

        return os.path.join(path, "{}.{}".format(md5.hexdigest(),ext))
    return wrapper



def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
