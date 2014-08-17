#!/usr/bin/env python

import webkit, gtk, os

win = gtk.Window()
win.resize(300,400)
win.connect('destroy', lambda w: gtk.main_quit())

scroller = gtk.ScrolledWindow()
win.add(scroller)

web = webkit.WebView()

settings = webkit.WebSettings()

settings.set_property('enable-default-context-menu',1)
settings.set_property('enable-file-access-from-file-uris',1)
settings.set_property('enable-universal-access-from-file-uris',1)

aDir = os.path.dirname(__file__)
web.set_settings(settings)

index = os.path.abspath(os.path.join(aDir,"gui","index.html"))
print "openning:",index
web.open(index)

scroller.add(web)

win.show_all()

gtk.main()


