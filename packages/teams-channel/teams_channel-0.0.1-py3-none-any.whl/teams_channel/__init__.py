from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("teams_channel")
except PackageNotFoundError:
    # package is not installed
    pass