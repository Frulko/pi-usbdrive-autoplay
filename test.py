import subprocess
import signal,sys,time  
import atexit
import os
import logging
from daemonize import Daemonize


def main():
  # logging.basicConfig(filename='test.log',level=logging.DEBUG)
  process = None
  terminate = False

  def clean_up(processPass):
    # do some clean up
    logger.debug("clean")
    print(processPass.pid)
    os.system("ps -ef | grep omxplayer | grep -v grep | awk '{print $2}' | xargs kill -9")
    terminate = True
    if processPass is None:
      print("not define")
    else:
      processPass.terminate()



  def signal_handling(signum,frame):           
      global process       
      terminate = True             
      print("kill")
      os.system("ps -ef | grep omxplayer | grep -v grep | awk '{print $2}' | xargs kill -9")
      print(process.pid)
      if process is None:
        print("not define")
      else:
        process.kill()   
      sys.exit(); 
                    






  try:
    logger.debug("Test")
    print("start player")
    logger.debug("Starting player")
    logger.debug(', '.join(sys.argv))
    time.sleep(1)
    logger.debug("trying")
    process = subprocess.call(['omxplayer', '-b', '--loop', '/media/usb1/aspirateur_musique_the_end.mp4'],stdout=subprocess.PIPE)
    # process = subprocess.call(["python", "timer.py"], stdout=subprocess.PIPE)
    atexit.register(clean_up, process)  
    logger.debug(process.pid)
    signal.signal(signal.SIGTERM, signal_handling)    
    # poll = process.poll()
    # time.sleep(10)
    # while terminate == False or poll is None:
    #   print("alive")
      
    #   time.sleep(1)
    
    #   if terminate:                            
    #     print "I'll be back"                 
    #     break

  except KeyboardInterrupt:
    # clean up
    print('stop')
    pass
  except Exception as inst:
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst) 
    raise
    


  print("You wont see this")




pid = "/tmp/test.pid"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("/home/pi/test.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

if __name__ == '__main__':
  # myname=os.path.basename(sys.argv[0])
  # pidfile='/tmp/%s' % myname       # any name
  # daemon = Daemonize(app="test_app", pid=pid, action=main, keep_fds=keep_fds)
  # daemon.start()
  main()