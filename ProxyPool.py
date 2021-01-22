import os
import Settings


def get_proxy():
    files = list(filter(lambda f: "|" not in f, os.listdir(Settings.POOL_DIR)))
    if not files:
        return None
    files.sort(key=lambda f: os.path.getmtime(os.path.join(Settings.POOL_DIR, f)))
    return files[0]
