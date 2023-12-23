from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("brainmapper")
except PackageNotFoundError:
    # package is not installed
    pass
