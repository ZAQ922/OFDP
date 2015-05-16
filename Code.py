"""
Window must be in top left corner
x_pad=7 adjust for window sides and top
y_pad=29
mouse press coords:
steam play button (330,200)
window egde(500,90) take to (0,0)
steam menu1(400,300)
delay 30s between menu 1 and 2
door menu1&2(400,330)
level v survive(250,250)
difficulty student(400,230)
scroll wheel all back
play area(7,29,792,471)
player picks round, start script, script presses mouse at (0,0)

pixel locations:
Ltrig(241,205)
Rtrig(543,205)
"""
import PIL
import pyscreenshot as ImageGrab#pyscreenshot: wrapper replaces ImageGrab
from pyscreenshot.about import __version__
from pyscreenshot.loader import Loader, FailedBackendError
from PIL import Image
from PIL.Image import core as _imaging

#os checking
import sys
from sys import platform as _platform
import os
import time

f_win32 = False
f_linux = False
f_darwn = False

#decides what OS and which libraries to import
if(_platform=="win32"):#WINDOWS imports
    f_win32 = True
    #print "WINDOWS OS"
    import win32api
    import win32gui
    import win32con
    #import pywinauto#wrapper that allows PIL/PILLOW images to run on non-window OS's 
    import ImageOps
    import numpy
    from numpy import *
elif((_platform=="linux")or(_platform=="linux2")):#LINUX imports
    f_linux = True
    #print "LINUX OS"
    import autopy
    import numpy
    from numpy import *
    import subprocess
    subprocess.call(["xdotool", "mousemove", "945", "132"])
elif(_platform=="darwin"):#OsX imports
    f_darwn = True
    print "OSX OS"

################################################################################
#WINDOWS API SECTION
################################################################################

#Global Variables
x_pad = 7
y_pad = 29

#Left mouse click
def LC():
    #Left Down
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    #Delay down signals, so it won't get ahead of itself
    time.sleep(.1)
    #Left Up
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #print "LC"


'''
#click-drag function, doesn't exactly work
def LP():
    pywinauto.controls.HwndWrapper.DragMouse(button="left",pressed='',press_coords=(500,90),release_coords=(0,0))
    print "LP"
'''

#right mouse click
def RC():
    #Right Down
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    #Delay down signals so it won't get ahead of itself
    time.sleep(.1)
    #Right Up
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    #print "RC"

#scroll function
def wheel():
    #Scroll down, alter 4th argument
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,x_pad,y_pad,-1000,0)


#coordinates of things, doesn't really work but it's a cool concept
class coord():
    press_play = (330, 200)
    drag_window = (500, 90)
    menu_top = (400, 300)
    menu_door1 = (400, 330)
    menu_door2 = (400, 330)
    menu_level = (250, 250)
    menu_diffi = (400, 230)

#set mouse to the coordinates
def MPOS(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
    
#function to get specific coordinates of where ever the mouse is upon execution
def get_cord():
    x,y=win32api.GetCursorPos()
    x=x-x_pad
    y=y-y_pad
    print x,y

#Class for particular values that will need logical comparisons
#4x4 matrix for me
class Blank:
    #LInit = 782#initial left
    #RInit = 667#initial right
    LHit = 543
    RHit = 662
    #BMiss = 16#if it misses on either side
    Stop = 868#stop check
    Pause = 171#UNPAUSE
    Replay = 162

    
#################################################SEEING SECTION#############################################################
#These next 2 def are the core of grabbing pixels and "seeing" them
#Grabs a specific area of the screen, returns the image to a directory with a unique name
def screenGrab():
    box = (x_pad,y_pad,x_pad+792,y_pad+471)
    im=ImageOps.grayscale(ImageGrab.grab(box))#explained past FG() in better detail
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
    a=array(im.getcolors())
    q=int(a.sum())
    #return im

'''
#should test the pixel colors much faster than screenGrab()
#doesn't work due to "color management" issues in GetPixel()
def FG(xcord, ycord):
    w = win32gui.FindWindow( None, "Bob Ross/window name" )#returns a handle
    dc = win32gui.GetWindowDC(w)#returns device context
    a=win32gui.GetPixel(w,xcord,ycord)#returns RGB from handle
    #dc.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    win32gui.DeleteDC()
    return a
'''

#the next get_X() use grayscale() and getcolors() to turn the pixels to grayscale, get the ASCII values and put them in an array
#that array is then summed for a precise number to decide actions
#.grab() will expand to the left, because this is the get_Rightbox, the left side shouldn't move
#keep that in mind by moving the (x/y_init-z) AND (x/y_end+z), Z being the amount you want to adjust the area by
#large pixel area = accurate sum, slower processing
#small pixel area = inaccurate sum, faster processing
#REMINDER: box=(x_init,y_init,x_end,y_end)
#              (   Top Left  ,Bottom right)
#.grab(box) expands left and down

#way to end punchy() while loop
def get_Kick():
    flag1=False
    box1=(x_pad+661,y_pad+279,x_pad+661+3,y_pad+279+3)#STOP
    im1=ImageOps.grayscale(ImageGrab.grab(box1))
    a1=array(im1.getcolors())
    q1=int(a1.sum())
    box2=(x_pad+355,y_pad+338,x_pad+355+1,y_pad+338+1)#REPLAY
    im2=ImageOps.grayscale(ImageGrab.grab(box2))
    a2=array(im2.getcolors())
    q2=int(a2.sum())
    box3=(x_pad+41,y_pad+3,x_pad+41+1,y_pad+3+1)#PAUSE
    im3=ImageOps.grayscale(ImageGrab.grab(box3))
    a3=array(im3.getcolors())
    q3=int(a3.sum())
    if((q1==Blank.Stop)or(q2==Blank.Replay)or(q3==Blank.Pause)):
        flag1=True
    return flag1


#Get pixel sum for Left Box(leftmost under guy)
def get_Lbox():
    box=(x_pad+359,y_pad+232,x_pad+359+3,y_pad+232+3)#must offset from window
    im=ImageOps.grayscale(ImageGrab.grab(box))
    ImageGrab.grab().save(os.getcwd() + '/LBox__' + str(int(time.time())) +'.png', 'PNG')
    a=array(im.getcolors())
    q=int(a.sum())
    print "Lbox\t" + str(q)
    return q

#Get pixel sum for Right Box(rightmost under guy)
def get_Rbox():
    box=(x_pad+424,y_pad+232,x_pad+424+3,y_pad+232+3)
    im=ImageOps.grayscale(ImageGrab.grab(box))
    #ImageGrab.grab(box).save(os.getcwd() + '/RBox__' + str(int(time.time())) +'.png', 'PNG')
    a=array(im.getcolors())
    q=int(a.sum())
    #print "Rbox\t" + str(q)
    return q
    
############################################################################################################################



#checks box values and punches accordingly
def punchy():
    print "PUNCHY"
    time.sleep(5)#delay for game to start
    while(True):
        flag = get_Kick()
        #if pause equals pause pixel sum, end loop
        if(flag==True):
            print "KICK"
            break
        else:
            bob = get_Lbox()#gets real time left box sum
            ross = get_Rbox()#gets real time right box sum                
            if(bob == Blank.LHit):
                #Left mouse click
                print "LC"
                LC()
            if(ross == Blank.RHit):
                #Right mouse click
                print "RC"
                RC()

#Starts the game
def StartGame():
    '''
    #press play
    MPOS((330,200))
    LC()
    time.sleep(5)#time to wait varied by computer
    MPOS((500,90))
    
    #move window to top left
    LP()
    '''
    
    #top Menu
    MPOS(coord.menu_top)
    LC()
    time.sleep(20)#allows game to fully load
    
    #click doors
    MPOS((400,330))
    LC()#click to screen
    time.sleep(1)
    
    #play option
    MPOS((400,330))
    LC()
    time.sleep(1)
    
    #Levels
    MPOS((250,250))
    LC()
    time.sleep(1)
    
    #difficulty
    MPOS((400,230))
    LC()
    time.sleep(5)
    
    #zoom out on map
    wheel()
    time.sleep(1)
    
################################################################################
#LINUX CODE
################################################################################
'''
This should just grab the screen using autopy, haven't worked past that to make it "see".

'''

def autoTrial():
    #screengrab function
    #autopy.bitmap.capture_screen().save(os.getcwd()+'/autopy__'+str(int(time.time()))+'.png','PNG')
    #this=autopy.bitmap.capture_screen()
    #print this
    #that=autopy.screen.get_color(1,1)#.screen is shorter version of bitmap.capture_screen()
    #print that
    t1=time.time()
    oneone=int(sum(array(autopy.color.hex_to_rgb(autopy.screen.get_color(1,1)))))#stores rgb of a pixel into an array then sums as int
    #print oneone
    onetwo=int(sum(array(autopy.color.hex_to_rgb(autopy.screen.get_color(1,2)))))
    #print onetwo
    twoone=int(sum(array(autopy.color.hex_to_rgb(autopy.screen.get_color(2,1)))))
    #print twoone
    twotwo=int(sum(array(autopy.color.hex_to_rgb(autopy.screen.get_color(2,2)))))
    #print twotwo
    three=int(oneone+onetwo+twoone+twotwo)
    #print three
    t2=time.time()
    tf=t2-t1
    IPS=int(1/tf)
    print IPS

def main():
    if(f_win32):
        #print "f_win32 = True"  
        #StartGame()
        #user picks level
        #run to play level
        #punchy()#function that punches/clicks
        get_Lbox()
        
    elif(f_linux):
        #print "f_linux = True"
        autoTrial()
    elif(f_darwn):
        print "f_darwn = True"  
    else:
        print "UNKNOWN OS"  

main()
