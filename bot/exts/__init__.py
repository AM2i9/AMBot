import pkgutil

from bot import exts

def walk():

    def on_error(name):
        raise ImportError(name=name)

    for module in pkgutil.walk_packages(exts.__path__, f"{exts.__name__}.", onerror=on_error):
        
        if module.name.rsplit('.')[-1].startswith("_"):
            continue

        yield module.name