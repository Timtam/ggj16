import platform

_system = platform.system()

if _system == 'Windows':
 from nvda import NVDA
 from we import WindowEyes
 from virgo import Virgo
 
 __all__ = ["NVDA", "WindowEyes","Virgo"]
else:
 __all__ = []
