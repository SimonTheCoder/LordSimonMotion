#!/usr/bin/python
import gtk
import sys
import gobject
import threading
import time
import thread_window

class ProgressWindow(thread_window.LSWindow):
    def __init__(self):
        super(ProgressWindow,self).__init__()
        self.set_default_size(300,-1)
        vb = gtk.VBox()
        self.add(vb)
        self.progress_bar = gtk.ProgressBar()
        vb.pack_start(self.progress_bar)
        #b = gtk.Button(stock=gtk.STOCK_OK)
        #vb.pack_start(b)
        #b.connect('clicked',self.on_button_clicked)
        #self.show_all()
    def __set_progress_bar_fraction(self,fraction):
        self.progress_bar.set_fraction(fraction);

    def set_fraction(self,fraction):
        gobject.idle_add(self.__set_progress_bar_fraction,fraction)
    def set_dyn_title(self,new_title):
        gobject.idle_add(self.set_title,new_title)
    

def test():
    w = ProgressWindow()
    w.run()
    #gtk.main()     
    for i in range(10):
        w.set_fraction(i/10.0)
        time.sleep(1);
    w.stop(); 

print __name__  
if __name__ == "__main__":
    test()
