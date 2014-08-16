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


web.set_settings(settings)

web.open("gui/index.html")

scroller.add(web)

win.show_all()

gtk.main()


