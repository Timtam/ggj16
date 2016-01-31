import platform

_system = platform.system()

if _system == 'Windows':
 from nvda import NVDA
 from sapi5 import Sapi5
 __all__ = ["NVDA", "Sapi5"]
elif _system == 'Darwin':
 from voiceover import VoiceOver
 __all__ = ["VoiceOver"]
elif _system == 'Linux':
 from speech_d import SpeechDispatcherOutput
 __all__ = ['SpeechDispatcherOutput']
