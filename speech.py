import platform
if platform.system()=='Windows':
 from accessible_output import speech
 from accessible_output.speech import outputs
 import accessible_output
 try:
  ooutput=getattr(outputs,"NVDA")()
 except accessible_output.output.OutputError:
  ooutput=None
 if ooutput and not ooutput.canSpeak(): ooutput=None
 Speaker=speech.Speaker(ooutput)
elif platform.system()=='Linux':
 import speechd
 class SpeechdSpeaker(object):
  def __init__(self):
   self.Client=speechd.SSIPClient('fscroller-speechd-client')
  def output(self,text,interrupt=False):
   if interrupt: self.Client.stop()
   self.Client.speak(text)
 Speaker=SpeechdSpeaker()