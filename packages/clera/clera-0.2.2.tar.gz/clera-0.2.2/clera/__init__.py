from .core import *
from .stubs import *
from .scripts.editor import editor
from .scripts.deploy import deploy

core.__all__.append('editor')
__all__ = core.__all__

version = __version__ = '0.2.2 Released 19-DECEMBER-2023'

__version__ = ver = version.split()[0]