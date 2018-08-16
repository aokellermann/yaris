#!/usr/bin/python2

import gi, serial, signal, sys, os, subprocess
from subprocess import Popen, PIPE
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Pango, Gdk, GdkX11
try:
    ser = serial.Serial("/dev/ttyUSB0", 115200)
except serial.SerialException:
    sys.exit("Couldn't open /dev/ttyUSB0")

class Yaris(Gtk.Window):
    def __init__(self):
        super(Yaris, self).__init__()
        self.connect("destroy", Gtk.main_quit)
        
        label = Gtk.Label()
        font = Pango.FontDescription("DejaVu Sans 32") # Increase font size
        label.modify_font(font)
        
        area = Gtk.DrawingArea() 
        fifo_path = "/tmp/yaris_cam_fifo"
        try:
            os.remove(fifo_path) # delete already existing fifo if needed
        except OSError:
            pass
        os.mkfifo(fifo_path)
        
        box = Gtk.VBox() 
        box.pack_start(label, expand = False,  fill = False, padding = 0)
        box.pack_end(area, expand = True, fill = True, padding = 0)
       
        eb = Gtk.EventBox() #to change background color
        eb.add(box)

        self.add(eb)
        self.update_label(eb, label)
        self.show_all()
        
        try:
            command = "mplayer -slave -input file=%s -wid %i tv://video=/dev/video0" % (fifo_path, area.get_property("window").get_xid())
        except Exception as e:
            sys.exit("Couldn't open /dev/video0")
        subprocess.Popen(command.split(), stdout = PIPE, stderr = PIPE)

        
    def update_label(self, ebox, label):
        distance = getLidarDistance()
        label.set_text(str(distance))
        timeout = 350
        color = "green"
        if distance < 80:
            color = "yellow"
            if distance < 60:
                timeout = 250
                color = "orange"

            if distance < 40:
                timeout = 150
                color = "red"
            
            command = "aplay /usr/share/yaris/beep.wav"
            subprocess.Popen(command.split(), stdout = PIPE, stderr = PIPE)
            
        ebox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(color)) # Change color of background of distance label
        GLib.timeout_add(timeout, self.update_label, ebox, label)
        
# Returns distance in centimeters, with a hardware minimum of 30
def getLidarDistance():
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 'Y' and recv[1] == 'Y':
                low = int(recv[2].encode('hex'), 16)
                high = int(recv[3].encode('hex'), 16)
                return low + high * 256
                
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Keyboard interrupt handler
    Yaris()
    Gtk.main()
