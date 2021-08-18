"""
	Copyright © 2012 Bence Nagy
	Version updated and converted to python3 for compatibility with Gedit 3
	Tested on Debian 10, gedit 3.30
	https://github.com/gncgroup
	Source version by Bance Nagy is available here:
	https://code.google.com/archive/p/double-save-gedit/downloads
"""
from gi.repository import GObject, Gtk, Gedit
import urllib.request, urllib.parse, urllib.error


import os.path
import subprocess

from datetime import datetime


class DoubleSavePlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DoubleSavePlugin"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
    
    def do_activate(self):
        print("Activating plugin...")
        handlers = []
        handler_id = self.window.connect("tab-added", self.on_tab_added)
        handlers.append(handler_id) 
        print("Connected handler %s" % handler_id)
        

        
        self.window.set_data("DoubleSavePluginHandlers", handlers)

    def do_deactivate(self):
        print("Deactivating plugin...")
        handlers = self.window.get_data("DoubleSavePluginHandlers")
        for handler_id in handlers:
            self.window.disconnect(handler_id)
            print("Disconnected handler %s" % handler_id)

    def do_update_state(self):
        pass
    
    def on_tab_added(self, window, tab, data=None):
        document = tab.get_document()
        print("'%s' has been added." % document.get_short_name_for_display())
        doc = tab.get_document()
        doc.connect("save",self.saved)

    def saved(self, doc):
            source = urllib.request.url2pathname(doc.get_uri_for_display())
           
            homedir = os.path.expanduser("~")+"/gedit-backups/"
            subprocess.getoutput("mkdir "+homedir)
            
            name = doc.get_short_name_for_display()

            timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

            ext = ".bak"
            newFileName =  name+"-" + timestamp + ext
            newpath = "\""+homedir + newFileName+"\""
            command = "cp \""+source+"\" "+ newpath
            print(command)
            subprocess.getoutput(command)
            subprocess.getoutput("chmod -w "+newpath)
    
