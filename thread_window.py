#!/usr/bin/python
import gtk
import sys
import gobject
import threading
import time
import thread_window
class LSWindow(gtk.Window):

    def __init__(self):
        super(LSWindow,self).__init__()
        gtk.gdk.threads_init()
    def __start_main(self):
        gtk.main()
    def __destroy_me(self):
        if not self.emit("delete-event",gtk.gdk.Event(gtk.gdk.DELETE)):
            self.destroy();
        gtk.main_quit()
    def __show(self):
        print "Window show"
        self.show_all()
    def __hide(self):
        print "Window hidden"
        self.hide()
    def run(self):
        gobject.idle_add(self.__show)
        #threading.Thread(target=self.__start_main).start()
    def stop(self):
        gobject.idle_add(self.hide)
        time.sleep(1.5)
        #gobject.idle_add(self.__destroy_me)


