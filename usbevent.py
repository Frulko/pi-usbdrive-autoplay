import threading
import time
import logging
import pyudev

class USBDetector():
    ''' Monitor udev for detection of usb '''
 
    def __init__(self, callbackMount, callbackUMount):
        logging.basicConfig(filename='example.log',level=logging.DEBUG)
        ''' Initiate the object '''
        thread = threading.Thread(target=self._work)
        thread.daemon = True
        thread.start()
        self.callback = callback

    def on_created(self):
      logging.info("on created")

    def on_deleted(self):
      logging.info("on delete")
      self.callback()
 
    def _work(self):
        ''' Runs the actual loop to detect the events '''
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='usb')
        # this is module level logger, can be ignored
        logging.info("Starting to monitor for usb")
        self.monitor.start()
        self.monitor.
        for device in iter(self.monitor.poll, None):
            logging.info("Got USB event: %s", device)
            if device.action == 'add':
                # some function to run on insertion of usb
                self.on_created()
            else:
                # some function to run on removal of usb
                self.on_deleted()