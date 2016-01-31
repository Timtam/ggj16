import platform

_system = platform.system()

if _system == 'Windows':
 from nvda import NVDA
 
 __all__ = ["NVDA"]
else:
 __all__ = []
