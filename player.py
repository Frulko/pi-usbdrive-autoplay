import signal,sys,time  
import os
import glob
import subprocess
from usbevent import USBDetector

def callbackUnmount():           
    global terminate        
    print("here")                
    terminate = True
    
    sys.exit()
    
usbdetect = USBDetector(callbackUnmount)
process = None
allowed_extensions = [".mp4", ".mov", ".mpg", ".mpeg"]

if len(sys.argv) < 2:
  print("You need to specify folder path")
  sys.exit()


dir = sys.argv[1]

if os.path.isdir(dir) == False:
  print(("{} is not a valid directory").format(dir))
  sys.exit()

  
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



terminate = False   





def signal_handling(signum,frame):           
    global terminate, process                    
    terminate = True 
    print 'bye'
    if (process is None) != False:
      process.kill()                    

signal.signal(signal.SIGINT,signal_handling)                                   


if nbPlaylistItem == 1:
  print("One file looping")
  # opa = os.system(("omxplayer -b --loop {}").format(playlist[0]))
  # process = subprocess.Popen(['omxplayer', '-b', '--loop', playlist[0]])
  # if opa > 0:
  #   sys.exit()
elif nbPlaylistItem == 0:
  print("No video file to play")
  sys.exit()
else:
  while True:
    # print("{} files looping".format(len(playlist)))
    for playlistItem in playlist:
      process = subprocess.Popen(['omxplayer', '-b', playlistItem])
      # opa = os.system(("omxplayer -b {}").format(playlistItem))
      # if opa > 0:
      #   terminate = True
      #   break
    if terminate:                            
        print "I'll be back"                 
        break


#print(playlist)

print "bye"                                  
