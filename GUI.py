#!/bin/python


import gtk
import gobject
import threading

import progressbar
import menu_window as menu_window_pack



progressbar_window = None;
menu_window = None;

def init():
    global menu_window
    global progressbar_window
    if progressbar_window == None:
        progressbar_window = progressbar.ProgressWindow()
        progressbar_window.set_title("Progress bar")
        progressbar_window.hide()
    if menu_window == None:
        menu_window = menu_window_pack.MenuWindow()
        menu_window.set_title("Menu window")
        menu_window.hide()
    threading.Thread(target= __start_gtk_main,name="GUI Thread").start()
def __start_gtk_main():
    gtk.main() 
