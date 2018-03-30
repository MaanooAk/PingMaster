
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def get_clipboard():
    return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()


def button(name, click, data=None):
    b = Gtk.Button(name)
    b.set_hexpand(True)
    if data is not None:
        b.connect("clicked", click, data)
    else:
        b.connect("clicked", click)
    return b


def image_button(stock_image, click, data=None):
    b = Gtk.Button()
    b.add(Gtk.Image(stock=stock_image))
    if data is not None:
        b.connect("clicked", click, data)
    else:
        b.connect("clicked", click)
    return b


def wrap_into_scrolled(o):
    sw = Gtk.ScrolledWindow()
    sw.set_hexpand(True)
    sw.set_vexpand(True)
    sw.add(o)
    return sw
