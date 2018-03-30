
# import gi
# gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def show_dialog(dialog):
    """
    Show and handle a dialog
    """

    result = dialog.run()
    dialog.destroy()

    return result


class AboutDialog(Gtk.Dialog):

    def __init__(self, parent):
        super().__init__("About", parent, 0, (Gtk.STOCK_OK,
                                              Gtk.ResponseType.OK))

        self.set_border_width(10)

        label = Gtk.Label()
        label.set_markup(
            "<big><b>Ping Master</b> <small>v.0.3</small></big>\n\n" +
            "Created by <b>MaanooAk</b>, more at " +
            "<a href=\"https://maanoo.com\">maanoo.com</a>\n\n")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
