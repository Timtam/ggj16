import os.path
import time
import sys
# loads of unused stuff in here
# usually I link in win32api and pygit2
# to retrieve some relevant data
# since we don't need those dependencies
# just remove them and set those two to False
GitLoaded=False
Win32ApiLoaded=False
class Script:
 def __init__(self):
  self.__Stable='Stable'
  self.__Development='Development'
  self.Version='1.0'
  self.Company='Global Game Jam 2016'
  self.Author='Hochschule Anhalt'
  self.Email='toni.barth@student.inf.hs-anhalt.de'
  self.Website='http://www.globalgamejam.org/'
  self.Name="No Buddy's Grey"
  self.Description='An interactive audio story to play for free, developed within 48 hours of hard work and less sleep.'
  self.Copyright='Copyright 2016 by Hochschule Anhalt'
 def __path(self):
  if hasattr(sys, "frozen") and sys.frozen in ["console_exe", "windows_exe"]:
   Path=unicode(os.path.dirname(sys.executable))
  else:
   Path = os.path.dirname(unicode(os.path.abspath(__file__)))
  bdir=os.path.isdir(Path)
  while not bdir:
   Path=os.path.abspath(Path+'/..')
   bdir=os.path.isdir(Path)
  return Path
 def __executable(self):
  if hasattr(sys, "frozen") and sys.frozen in ["console_exe", "windows_exe"]:
   return True
  else:
   return False
 def __revisionnumber(self):
  if self.Executable and Win32ApiLoaded:
   return LoadResource(0,u"REVISIONNUMBER",1)
  elif GitLoaded:
   try:
    repo=pygit2.Repository(os.path.join(self.Path, '.git'))
   except KeyError:
    return str(0)
   revcount=0
   for commit in repo.lookup_reference(repo.head.name).log():
    revcount+=1
   return str(revcount)
  else:
   return str(0)
 def __builddate(self):
  if self.Executable and Win32ApiLoaded:
   return LoadResource(0,u"BUILDDATE",1)
  elif GitLoaded:
   try:
    repo=pygit2.Repository(os.path.join(self.Path,".git"))
   except KeyError:
    return '00-00-00 00:00:00'
   headrev=repo.get(repo.head.target)
   ltime=time.localtime(headrev.commit_time)
   return str(ltime.tm_year)+'-'+str(ltime.tm_mon)+'-'+str(ltime.tm_mday)+' '+str(ltime.tm_hour)+':'+str(ltime.tm_min)+':'+str(ltime.tm_sec)
  else:
   return '00-00-00 00:00:00'
 def __releasenotes(self):
  if self.Executable and Win32ApiLoaded:
   return LoadResource(0,u"RELEASENOTES",1)
  elif GitLoaded:
   try:
    repo = pygit2.Repository(os.path.join(self.Path,'.git'))
   except KeyError:
    return '---'
   if self.VersionTag==self.__Stable:
    taglist=[]
    commit=repo.get(repo.head.target)
    for ref in repo.listall_references():
     oref=repo.revparse_single(ref)
     if oref.type==pygit2.GIT_OBJ_TAG and oref.hex==commit.hex: return oref.message
    return commit.message
   else:
    commit=repo.get(repo.head.target)
    return commit.message
  else:
   return '---'
 def __versiontag(self):
  if self.Executable and Win32ApiLoaded:
   return LoadResource(0,u"VERSIONTAG",1)
  elif GitLoaded:
   tag=self.__Development
   try:
    repo=pygit2.Repository(os.path.join(self.Path,'.git'))
   except KeyError:
    return 'Unknown'
   taglist=[]
   for ref in repo.listall_references():
    if ref.find('tags')>=0:
     oref=repo.revparse_single(ref)
     taglist.append(oref.hex)
   if len(taglist)>0:
    if repo.get(repo.head.target).hex in taglist:
     tag=self.__Stable
   return tag
  else:
   return 'Unknown'
 def __versionhash(self):
  if self.Executable and Win32ApiLoaded:
   return LoadResource(0,u'VERSIONHASH',1)
  elif GitLoaded:
   try:
    repo=pygit2.Repository(os.path.join(self.Path,'.git'))
   except KeyError:
    return '0000000000000000000000000000000000000000'
   return repo.get(repo.head.target).hex
  else:
   return '0000000000000000000000000000000000000000'
 def Resources(self):
  resources=[]
  resources.append((u'REVISIONNUMBER',1,self.RevisionNumber))
  resources.append((u'BUILDDATE',1,self.BuildDate))
  resources.append((u'VERSIONTAG',1,self.VersionTag))
  resources.append((u'RELEASENOTES',1,self.ReleaseNotes))
  resources.append((u'VERSIONHASH',1,self.VersionHash))
  return resources
 Path=property(__path)
 Executable=property(__executable)
 RevisionNumber=property(__revisionnumber)
 VersionTag=property(__versiontag)
 BuildDate=property(__builddate)
 ReleaseNotes=property(__releasenotes)
 VersionHash=property(__versionhash)