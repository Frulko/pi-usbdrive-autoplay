import signal,sys,time  
import os
import glob
import subprocess
from usbevent import USBDetector
import threading
from functools import wraps



def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap

class Timer():
    toClearTimer = False
    def setTimeout(self, fn, time):
        isInvokationCancelled = False
        @delay(time)
        def some_fn():
                if (self.toClearTimer is False):
                        fn()
                else:
                    print('Invokation is cleared!')        
        some_fn()
        return isInvokationCancelled
    def setClearTimer(self):
        self.toClearTimer = True


def callbackUnmount():           
    global terminate        
    print("here>")                
    #terminate = True
    
    #sys.exit()

def callbackMount():           
    print("mount")        
    
#usbdetect = USBDetector(callbackMount, callbackUnmount)
process = None
allowed_extensions = [".mp4", ".mov", ".mpg", ".mpeg"]

terminate = False



#if len(sys.argv) < 2:
  #print("You need to specify folder path")
  #sys.exit()


#dir = sys.argv[1]

#if os.path.isdir(dir) == False:
#  print(("{} is not a valid directory").format(dir))
  # sys.exit()



def signal_handling(signum,frame):           
    global terminate, process                    
    terminate = True 
    print "bye bye"
    os.system("ps -ef | grep omxplayer | grep -v grep | awk '{print $2}' | xargs kill -9")           

signal.signal(signal.SIGINT,signal_handling) 




def launchPlaylistFromDirectory(dir):
  global terminate
    
  files = os.listdir(dir)
  print(("List files for: {}").format(dir))

  playlist = []

  for file in files:
    if file[0] == ".":
      continue
    
    filename, file_extension = os.path.splitext(file)
    if file_extension in allowed_extensions:
      #print(("--- {} // {}").format(filename, file_extension))
      playlist.append(("{}/{}").format(dir, file))
      #os.system(("omxplayer -b {}/{}").format(dir, file))

  nbPlaylistItem = len(playlist)
  print(playlist)
  if nbPlaylistItem == 1:
    print("One file looping")
    opa = os.system(("omxplayer -b --loop {}").format(playlist[0]))
    # process = subprocess.Popen(['omxplayer', '-b', '--loop', playlist[0]])
    if opa > 0:
      sys.exit()
  elif nbPlaylistItem == 0:
    print("No video file to play")
    sys.exit()
  else:
    print("else")
    while True:
      # print("{} files looping".format(len(playlist)))
      for playlistItem in playlist:
        # process = subprocess.Popen(['omxplayer', '-b', playlistItem])
        opa = os.system(("omxplayer -b {}").format(playlistItem))
        if opa > 0:
          terminate = True
          break
      if terminate:                            
          print "I'll be back"                 
          break

  

  print "bye"   


loopProcess = None


timer = Timer()
def detectUSB():
  global loopProcess
  medias = ["/media/usb0", "/media/usb1", "/media/usb2", "/media/usb3"]
  hasNoMedias = True
  mediaPointIndex = ''

  if loopProcess == None:
    loopProcess = subprocess.Popen(['omxplayer', '-b', '--loop', '/home/pi/loop.mp4'],stdout=subprocess.PIPE)
  for media in medias:
    if len(os.listdir(media) ) != 0:    
      hasNoMedias &= False
      mediaPointIndex = media
  
  
  if hasNoMedias == False:

    os.system("ps -ef | grep omxplayer | grep -v grep | awk '{print $2}' | xargs kill -9")
    loopProcess = None
    print("Launch - {}".format(mediaPointIndex))
    launchPlaylistFromDirectory(mediaPointIndex)
    timer.setTimeout(detectUSB, 1.0)
  else :
    print("No USB keys founds")
    timer.setTimeout(detectUSB, 1.0)

timer.setTimeout(detectUSB, 0.1) 