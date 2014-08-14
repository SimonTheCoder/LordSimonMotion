#!/usr/bin/python
import gtk
import sys
import gobject
import threading
import time
import thread_window

class MenuWindow(thread_window.LSWindow):
    def __init__(self):
        super(MenuWindow,self).__init__()
        self.grayColorValue = 50000
        self.selectedColor = gtk.gdk.Color(6400, 6400, 6440)
        self.normalColor = gtk.gdk.Color(self.grayColorValue,self.grayColorValue, self.grayColorValue)
        
        self.set_keep_above(True)
        self.set_accept_focus(False)
        self.set_default_size(300,300)
        
        self.set_title("Menu")
        self.set_position(gtk.WIN_POS_CENTER)
        table = gtk.Table(3, 3, True)
        
        self.center = gtk.Button("      ")
        self.west = gtk.Button("west")
        self.east = gtk.Button("east")
        self.north = gtk.Button("north")
        self.south = gtk.Button("south")
        
        self.__rest_color()

        table.attach(self.center,1,2,1,2)
        table.attach(self.west,0,1,1,2)
        table.attach(self.east,2,3,1,2)
        table.attach(self.north,1,2,0,1)
        table.attach(self.south,1,2,2,3)

        self.add(table);
        self.show_all()
    def __rest_color(self):
        self.center.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color(0,65535,0))
        self.west.modify_bg(gtk.STATE_NORMAL,self.normalColor)
        self.east.modify_bg(gtk.STATE_NORMAL,self.normalColor)
        self.north.modify_bg(gtk.STATE_NORMAL,self.normalColor)
        self.south.modify_bg(gtk.STATE_NORMAL,self.normalColor)


    def __selecting(self,which,percent):
        if percent <= 0.0:
            return
        if percent >= 1:
            percent = 1.0
        target = None
        if (which == "center"):
            gobject.idle_add(self.__rest_color)
            return
        if (which == "west"):
            target = self.west
        if (which == "east"):
            target = self.east
        if which == "north":
            target = self.north
        if which == "south":
            target = self.south
        for item in (self.west,self.east,self.north,self.south):
            if item == target:
                next
            item.modify_bg(gtk.STATE_NORMAL,self.normalColor)
        r = self.grayColorValue * percent
        r = round(r)

        g = 65535-(65535-self.grayColorValue)*percent
        g = round(g)

        b = r

        #self.center.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color(r,g,b))
        self.center.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color(int(r),int(g),int(b)))

        r = self.grayColorValue * (1 - percent)
        r = round(r)

        g = self.grayColorValue + (65535 - self.grayColorValue) * percent
        g = round(g)

        b = r
        target.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color(int(r),int(g),int(b)))
    def selecting_item(self,which,percent):
        gobject.idle_add(self.__selecting,which,percent)



    def __set_items(self,west="",east="",north="",south=""):
        self.west.set_label(west)
        self.east.set_label(east)
        self.north.set_label(north)
        self.south.set_label(south)

    def set_items(self,west="",east="",north="",south=""):
        gobject.idle_add(self.__set_items,west,east,north,south)
        gobject.idle_add(self.__rest_color)


def test():
    w = MenuWindow()
    w.run()
    #gtk.main()     
    for i in range(20):
        percent = i/100.0
        print percent
        w.selecting_item("west",percent)        
        time.sleep(0.1);
    w.set_items("a","b","c","d")
    for i in range(100):
        percent = i/100.0
        print percent
        w.selecting_item("east",percent)        
        time.sleep(0.1);

    w.stop(); 

print __name__  
if __name__ == "__main__":
    test()   
