#create by Simon Shi


import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import os

import progressbar
import gtk

import menu_window
import GUI

import time

class Menu(object):
    STATE_CONTINUE = 1
    STATE_OVER = 2
    STATE_MENU_CHANGE = 3
    def __init__(self,menu=None):
        self.lastX = -1;
        self.lastY = -1;
        self.curX = None;
        self.curY = None;
        self.tdx = 100.0
        self.tdy = 100.0
        self.menu_window = None;
        if menu is not None:
            self.menu_window = menu.menu_window
        if self.menu_window == None:
            self.menu_window = GUI.menu_window 
            self.menu_window.set_items("Left screen","Right screen","WorkSpace","MiddleScreen & Cancel")
        self.menu_window.run()

    def stop(self):
        if self.menu_window is not None:
            self.menu_window.stop()
            self.menu_window = None    
    def __check_state(self,x,y):
        menu = self
        tdx = self.tdx 
        tdy = self.tdy
#        print "last: %f %f  hand: %f %f" % (menu.lastX,menu.lastY,x,y)
        west_percent = (menu.lastX - x)/tdx 
        east_percent = (x - menu.lastX)/tdx 
        north_percent = (y - menu.lastY)/tdy 
        south_percent = (menu.lastY - y)/tdy 
        target = None;
        for item_percent in (("west",west_percent),("east",east_percent),("north",north_percent),("south",south_percent)):
            #self.menu_window.selecting_item(item_percent[0],item_percent[1])
            if target == None:
                target = item_percent
            elif target[1] < item_percent[1]:
                target = item_percent
#        print "target %s %f" % target
        self.menu_window.selecting_item(target[0],target[1])
        if west_percent >=0.995:
            res = menu.west_call()         
        elif east_percent >=0.995:
            res = menu.east_call()         
        elif north_percent >=0.995:
            res = menu.north_call()         
        elif south_percent >=0.995:
            res = menu.south_call() 
        else:
            return (Menu.STATE_CONTINUE,1)       
        if res is None:
            return (Menu.STATE_OVER,1) 
        if isinstance(res,Menu):
            return (Menu.STATE_MENU_CHANGE,res)
        #should never goes here
        print "BUG!!! in Menu __check_state"
        return None
    def setCurrentPos(self,x,y):
        self.curX = x
        self.curY = y
	if(self.lastY == -1 or self.lastX == -1):
	    self.lastX = x
	    self.lastY = y
        return self.__check_state(x,y) 
    def west_call(self):
        print "move to left screen"
        #os.system("xdotool key alt+ctrl+Left")
        os.system("xdotool mousemove --sync 720 450")
        os.system("xdotool click 1")                          
        return None
        pass
    def east_call(self):
        print "move to left screen"
        #os.system("xdotool key alt+ctrl+Left")
        os.system("xdotool mousemove --sync 3760 450")
        os.system("xdotool click 1")                          
        return None
        pass
    def north_call(self):
        newMenu = WorkSpaceMenu(self);
        return newMenu
        pass
    def south_call(self):
        print "Quit menu"
        os.system("xdotool mousemove --sync 2240 450")
        os.system("xdotool click 1")                          
        return None
        pass

class WorkSpaceMenu(Menu):

    def __init__(self,parentMenu):
        super(WorkSpaceMenu,self).__init__(parentMenu);
        self.menu_window.set_items("Left Workspace","Right Workspace","TestSub","Cancel") 
        time.sleep(0.6)
    def west_call(self):
        print "move to left workspace"
        os.system("xdotool sleep 0.6 key alt+ctrl+Left")
        return None
        pass
    def east_call(self):
        print "move to left workspace"
        os.system("xdotool sleep 0.6 key alt+ctrl+Left")
        return None
        pass

class LordSimonListener(Leap.Listener):
    
    def on_init(self, controller):
        print "Initialized"
        self.circleCount = 0;
        self.window = None; 
        self.menu = None;
        self.menu_window = None;
        GUI.init()
    def on_connect(self, controller):
        print "Connected"
        self.conky_started = False;

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def clearGestureWindows(self,controller):
        if self.conky_started == True:
            os.system("cd ./conky/;./stopdraw.sh;cd -");
            self.conky_started = False;
        if self.window is not None:
            self.window.stop()
            self.window=None
    def get_fingers_avg_pos(self,hand):
        fingers = hand.fingers
        if not fingers.is_empty and len(fingers) != -1:
            avg_pos = Leap.Vector()
            for finger in fingers:
                avg_pos+= finger.stabilized_tip_position
            avg_pos /= len(fingers)
            return avg_pos
    def stop_menu(self):
        if self.menu is not None:
            self.menu.stop()
            self.menu = None
    def start_menu(self,controller):
        frame = controller.frame()
        hand = frame.hands[0]
        hand_pos = self.get_fingers_avg_pos(hand)
        if hand_pos is None:
            return
        self.clearGestureWindows(controller)
        if self.menu == None:
            self.menu = Menu()
      
        state,new_menu = self.menu.setCurrentPos(hand_pos.x,hand_pos.y)

        if state == Menu.STATE_OVER:
            print "Action selected."
            self.stop_menu()
        elif state == Menu.STATE_MENU_CHANGE:
            print "New menu"
            self.menu = new_menu
        else:
            #continue    
            pass
    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #~ print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              #~ frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        if frame.hands.is_empty :
            self.clearGestureWindows(controller)
            self.stop_menu()
        if not frame.hands.is_empty:
            if len(frame.hands) == 1:
                self.start_menu(controller)
                return
            else:
                if self.menu != None:
                    self.stop_menu()
                    pass
            if self.conky_started == False:
                os.system("cd ./conky/;./drawatmouse.sh;cd -");
                self.conky_started = True;
            # Get the first hand
            hand = frame.hands[0]
            
            # Check if the hand has any fingers
            fingers = hand.fingers
            if not fingers.is_empty:
                # Calculate the hand's average finger tip position
                avg_pos = Leap.Vector()
                for finger in fingers:
                    avg_pos += finger.tip_position
                avg_pos /= len(fingers)
                #~ print "Hand has %d fingers, average finger tip position: %s" % (
                      #~ len(fingers), avg_pos)

            # Get the hand's sphere radius and palm position
            #~ print "Hand sphere radius: %f mm, palm position: %s" % (
                  #~ hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            #~ print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                #~ direction.pitch * Leap.RAD_TO_DEG,
                #~ normal.roll * Leap.RAD_TO_DEG,
                #~ direction.yaw * Leap.RAD_TO_DEG)

            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        clockwiseness = "clockwise"
                        self.circleCount += 1
                        print "clockwise circleCount = %d" % self.circleCount
                        if self.window == None:
                            #self.window = progressbar.ProgressWindow()
                            self.window = GUI.progressbar_window
                            self.window.set_keep_above(True);
                            self.window.set_accept_focus(False)
                            win_width,win_height = self.window.get_size()
                            self.window.move(gtk.gdk.screen_width() - win_width,0)
                            #self.window.set_position((0,0));                           
                            self.window.run()                           
                        self.window.set_dyn_title("Lock Screen")                           
                        self.window.set_fraction(circle.progress /4) 
                        if self.circleCount >= 150 and circle.progress >4 and circle.progress <5:
                            self.circleCount = 0;
                            #os.system("zenity --notification --timeout 1 --text='Locking Screen...'")
                            os.system("xflock4")
                            if self.window != None:
                                self.window.stop()
                                self.window = None
                    else:
                        clockwiseness = "counterclockwise"
                        self.circleCount += 1
                        print "circleCount = %d" % self.circleCount
                        if self.window == None:
                            #self.window = progressbar.ProgressWindow()
                            self.window = GUI.progressbar_window
                            self.window.set_keep_above(True);
                            self.window.set_accept_focus(False)
                            win_width,win_height = self.window.get_size()
                            self.window.move(0,0)
                            #self.window.set_position((0,0));                           
                            self.window.run()                           
                        self.window.set_dyn_title("Give You LordSimon's Power")                           
                        self.window.set_fraction(circle.progress /4) 
                        if self.circleCount >= 150 and circle.progress >4 and circle.progress <5:
                            self.circleCount = 0;
                            if len(frame.hands)==2:
                                os.system("xdotool key Y O U R P A S S W O R D H E R E Return")    
                            else:
                                os.system("xdotool key Return")    
                            if self.window != None:
                                self.window.stop()
                                self.window = None
                    # Calculate the angle swept since the last frame
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                    print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                            gesture.id, self.state_string(gesture.state),
                            circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    #~ print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                            #~ gesture.id, self.state_string(gesture.state),
                            #~ swipe.position, swipe.direction, swipe.speed)
                    if gesture.state == Leap.Gesture.STATE_START:
                        dx,dy,dz = swipe.direction.x,swipe.direction.y,swipe.direction.z
                        print "Swip Start ======= dx,dy,dz[%f,%f,%f]" % (dx,dy,dz)
                        if dx>0.8 and abs(dy)<0.3 and abs(dz<0.4):
                            print "Swip form L to R"
                            print "mouse move to sceen right"
                            os.system("xdotool mousemove --sync 3680 512")
                            os.system("xdotool click 1")
                        elif dx < -0.8  and abs(dy)<0.3 and abs(dz)<0.4:
                            print "Swip from R to L"
                            print "mouse move to sceen left"
                            os.system("xdotool mousemove --sync 720 450")                            
                            os.system("xdotool click 1")
                        elif abs(dx) <0.3 and dy > 0.8 and abs(dz)<0.6:
                            print "Swip from D to U"
                            print "mouse move to sceen cent0er"
                            os.system("xdotool mousemove --sync 2240 450")
                            os.system("xdotool click 1")
                        elif abs(dx) <0.3 and dy < -0.8 and abs(dz)<0.6:
                            print "Swip from U to D" 
                            print "mouse move to sceen center"
                            os.system("xdotool mousemove --sync 2240 450")
                            os.system("xdotool click 1")                          

                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    keytap = KeyTapGesture(gesture)
                
                    print "Key Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_string(gesture.state),
                            keytap.position, keytap.direction )

                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    screentap = ScreenTapGesture(gesture)
                    print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_string(gesture.state),
                            screentap.position, screentap.direction )

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            #~ print ""
            pass

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = LordSimonListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
