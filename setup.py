# This is the distutils script for creating a Python-based com (exe or dll)
# server using win32com.  This script should be run like this:
#
#  % python setup.py py2exe
#
# After you run this (from this directory) you will find two directories here:
# "build" and "dist".  The .dll or .exe in dist is what you are looking for.
##############################################################################
import shutil
import script
import sys
import os
import os.path
import py2exe
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll","sdl_ttf.dll"): # "sdl_ttf.dll" added by arit.
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
def ListAllFiles(path):
 entrylist=os.listdir(path)
 flist=[]
 for entry in entrylist:
  fentry=os.path.join(path,entry)
  if os.path.isdir(fentry):
   nflist=ListAllFiles(fentry)
   flist=flist+nflist
  else:
   flist.append(fentry)
 return flist
def listdlls(folder):
 fileslist=[]
 files=os.listdir(folder)
 for file in files:
  if os.path.isfile(os.path.join(folder,file)):
   ext=os.path.splitext(file)[1]
   if ext.lower()=='.dll':
    fileslist.append(file)
 return fileslist
origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one

Script=script.Script()
ScriptDir=Script.Path
os.chdir(ScriptDir)
from distutils.core import setup
import py2exe
import zipfile
if len(sys.argv)==1: sys.argv.append('py2exe')
BuildDir=ScriptDir+"\\build"
DistDir=ScriptDir+"\\dist"
py2exe_options=dict(
 ascii=False,
 excludes=['email',
           'pygit2',
           'distutils',
           'calendar',
           'numpy',
           'configparser',
           'doctest',
           'ftplib',
           'getpass',
           'optparse',
           'cookielib',
           'win32api',
           'win32con',
           'win32pipe',
           'tarfile',
           'difflib',
           'unittest'],
 dll_excludes=["w9xpopen.exe"],
 bundle_files=3,
 optimize=2,
 compressed=True)
setupparameters={
 'name':Script.Name,
 'options':{'py2exe':py2exe_options},
 'zipfile':None,
 'version':Script.Version,
 'description':Script.Description,
 'author':Script.Author,
 'author_email':Script.Email,
 'windows':[{'script':'game.py','other_resources':Script.Resources()}]}
setup(**setupparameters)
zip=zipfile.ZipFile(os.path.join(ScriptDir,"%s-%s.zip"%(Script.Name,Script.Version)),"w")
for file in ListAllFiles(DistDir):
 zip.write(file,'%s-%s\\%s'%(Script.Name,Script.Version,os.path.relpath(file,DistDir)),zipfile.ZIP_DEFLATED)
for file in listdlls(os.path.join(ScriptDir,"accessible_output","lib")):
 zip.write(os.path.join(ScriptDir,"accessible_output","lib",file),'%s-%s\\lib\\%s'%(Script.Name,Script.Version,file),zipfile.ZIP_DEFLATED)
for file in listdlls(ScriptDir):
 zip.write(os.path.join(ScriptDir,file),'%s-%s\\%s'%(Script.Name,Script.Version,file),zipfile.ZIP_DEFLATED)
for file in ListAllFiles(os.path.join(ScriptDir,"assets")):
 zip.write(file,'%s-%s\\assets\\%s'%(Script.Name,Script.Version,os.path.relpath(file,os.path.join(ScriptDir,"assets"))),zipfile.ZIP_DEFLATED)
zip.close()
shutil.rmtree(BuildDir)
shutil.rmtree(DistDir)