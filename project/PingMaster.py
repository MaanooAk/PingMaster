
# import gi
# gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from threading import Lock

import GtkUtils
import Dialogs
from PingThread import ping_thread
from Ips import get_hostname, generate_ips


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Ping MasterA")
        self.set_border_width(10)

        self.title = "Ping Master"

        self.hostname = "8.8.8.8"
        self.repeat = False
        self.delay = None
        self.alive = False
        self.code = 2
        self.close_on_alive = False
        self.close_on_fail = False

        self.last_thread = None
        self.start_count = 0
        self.lock = Lock()

        # Build

        self.hb = None
        self.properties_button = None
        self.build_header()

        # Box

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(
            Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

        # Tabs

        self.build_tab_auto()

        self.entry_hostname = None
        self.build_tab_simple()

        self.entry_ips = None
        self.button = None
        self.label_ips = None
        self.build_tab_costume()

        self.build_tab_advanced()

        # Stack switcher

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_halign(Gtk.Align.CENTER)
        stack_switcher.set_stack(self.stack)
        vbox.pack_start(stack_switcher, False, True, 0)
        vbox.pack_start(self.stack, True, True, 0)

        self.spinner = None
        self.status = None
        self.build_footer(vbox)

        # Menus

        self.menu = None
        self.build_menu()

        # Show

        self.connect("delete-event", self.delete_event)

        self.set_status("Pinging")
        self.perform_ping()
        self.show_all()

    def build_header(self):

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = self.title
        self.hb.set_subtitle("Idle")
        self.set_titlebar(self.hb)

        # Left header buttons
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        button = GtkUtils.image_button(Gtk.STOCK_PASTE, self.on_paste_clicked)
        box.add(button)

        button = GtkUtils.image_button(Gtk.STOCK_REFRESH,
                                       self.on_refresh_clicked)
        box.add(button)

        self.hb.pack_start(box)

        #  Right header buttons
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        button = Gtk.MenuButton()
        button.add(Gtk.Image.new_from_icon_name("open-menu-symbolic",
                                                Gtk.IconSize.BUTTON))
        box.add(button)
        self.properties_button = button

        self.hb.pack_end(box)

    def build_tab_auto(self):

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(4)
        grid.set_column_spacing(4)

        grid.attach(GtkUtils.button(
            "Ping DNS", self.on_ping_special_clicked, "dns"
        ), 0, 0, 2, 1)
        grid.attach(GtkUtils.button(
            "Ping Router", self.on_ping_special_clicked, "router"
        ), 0, 1, 1, 1)
        grid.attach(GtkUtils.button(
            "Ping Web", self.on_ping_special_clicked, "web"
        ), 1, 1, 1, 1)

        self.stack.add_titled(grid, "auto", "Auto")

    def build_tab_simple(self):

        self.entry_hostname = Gtk.Entry()
        self.entry_hostname.set_hexpand(True)
        self.entry_hostname.set_text("maanoo.com")

        button = GtkUtils.button("Ping", self.on_ping_clicked)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(4)
        grid.set_column_spacing(4)
        grid.attach(self.entry_hostname, 0, 0, 2, 1)
        grid.attach(button, 2, 0, 1, 1)

        self.stack.add_titled(grid, "simple", "Simple")

    def build_tab_costume(self):

        self.entry_ips = Gtk.Entry()
        self.entry_ips.set_hexpand(True)
        self.entry_ips.set_text("192.168.1.[0-255]")

        self.button = GtkUtils.button("Ping all", self.on_ping_all_clicked)

        box = Gtk.HBox(spacing=0)

        radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "Instant")
        radio1.connect("toggled", self.on_delay_toggle, 0)
        box.add(radio1)
        radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Short")
        radio2.connect("toggled", self.on_delay_toggle, 0.01)
        radio2.set_active(True)
        box.add(radio2)
        radio3 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Long")
        radio3.connect("toggled", self.on_delay_toggle, 0.1)
        box.add(radio3)

        self.label_ips = Gtk.Label()
        self.label_ips.set_hexpand(True)
        self.label_ips.set_selectable(True)

        label_ips_warp = GtkUtils.wrap_into_scrolled(self.label_ips)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(4)
        grid.set_column_spacing(4)
        grid.attach(self.entry_ips, 0, 0, 2, 1)
        grid.attach(self.button, 2, 0, 1, 1)
        grid.attach(box, 0, 1, 3, 1)
        grid.attach(label_ips_warp, 0, 2, 3, 1)

        self.stack.add_titled(grid, "costume", "Costume")

    def build_tab_advanced(self):

        label = Gtk.Label()
        label.set_markup(
            "<b>TODO</b> implement\n<b>TODO</b> implement\n"
            "<b>TODO</b> implement\n<b>TODO</b> implement\n")
        label.set_line_wrap(True)

        self.stack.add_titled(label, "advanced", "Advanced")

    def build_footer(self, vbox):

        self.spinner = Gtk.Spinner()

        self.status = Gtk.Label()
        self.status.set_hexpand(True)
        self.status.set_xalign(0)

        label = Gtk.Label()
        label.set_markup("<small>Repeat</small>")

        repeat = Gtk.CheckButton()
        repeat.set_active(self.repeat)
        repeat.connect("toggled", self.on_repeat_toggle)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(4)
        grid.set_column_spacing(4)
        grid.attach(self.spinner, 0, 0, 1, 1)
        grid.attach(self.status, 1, 0, 1, 1)
        grid.attach(label, 2, 0, 1, 1)
        grid.attach(repeat, 3, 0, 1, 1)

        vbox.pack_start(grid, False, True, 0)

    def build_menu(self):

        menu = Gtk.Menu()
        menu.set_halign(Gtk.Align.END)

        item = Gtk.MenuItem("Refresh")
        item.connect("activate", self.on_refresh_clicked)
        menu.append(item)
        menu.append(Gtk.SeparatorMenuItem())

        item = Gtk.MenuItem("Close")
        item.connect("activate", lambda _, w: w.close(), self)
        menu.append(item)

        def on_close_on_alive_activate(widget, window):
            window.close_on_alive = widget.get_active()

        item = Gtk.CheckMenuItem("Close on alive")
        item.set_active(self.close_on_alive)
        item.connect("activate", on_close_on_alive_activate, self)
        menu.append(item)

        def on_close_on_fail_activate(widget, window):
            window.close_on_fail = widget.get_active()

        item = Gtk.CheckMenuItem("Close on fail")
        item.set_active(self.close_on_fail)
        item.connect("activate", on_close_on_fail_activate, self)
        menu.append(item)
        menu.append(Gtk.SeparatorMenuItem())

        def on_about_activate(widget, window):
            Dialogs.show_dialog(Dialogs.AboutDialog(window))

        item = Gtk.MenuItem("About")
        item.connect("activate", on_about_activate, self)
        menu.append(item)

        menu.show_all()
        self.menu = menu

        self.properties_button.set_popup(menu)

    def delete_event(self, p1, p2):
        self.repeat = False

        if self.last_thread is not None:
            self.last_thread.active = False

        Gtk.main_quit(p1, p2)

    def set_status(self, text1, text2=None):
        if text2 is None:
            text2 = text1

        self.hb.set_subtitle(text1)
        self.status.set_markup("<small>" + text2 + "</small>")

    def on_repeat_toggle(self, widget):
        self.repeat = widget.get_active()

    def on_delay_toggle(self, widget, tag):
        self.delay = tag

    def on_ping_clicked(self, widget):
        self.hostname = self.entry_hostname.get_text()
        self.perform_ping()

    def on_ping_special_clicked(self, widget, tag):
        self.hostname = get_hostname(tag)
        self.perform_ping()

    def on_refresh_clicked(self, widget):
        self.perform_ping()

    def on_paste_clicked(self, widget):
        text = GtkUtils.get_clipboard()
        if text is not None:
            self.entry_hostname.set_text(text)
            self.hostname = text
            self.perform_ping()

    def on_ping_all_clicked(self, widget):
        text = self.entry_ips.get_text()

        self.label_ips.set_text("")

        delay = 0
        for i in generate_ips(text):
            self.hostname = i
            self.start_ping_thread(solo=False, delay=delay)
            delay += self.delay

    def show_pinging(self):
        self.start_count += 1
        self.spinner.start()
        # self.set_status("Pinging " + self.hostname)

    def show_result(self):
        self.start_count -= 1
        if self.start_count == 0:
            self.spinner.stop()

        if self.alive:
            self.set_status("Alive " + self.hostname)
        else:
            self.set_status("Failed " + self.hostname,
                            "Failed " + self.hostname + " with " +
                            ("no reply" if self.code == 1 else "error"))

        # Check for auto close
        if (self.alive and self.close_on_alive) or \
                (not self.alive and self.close_on_fail):
            self.close()
            return

        # Check for repeat
        if self.stack.get_visible_child_name() == "costume" and self.alive:
            self.label_ips.set_text(self.hostname + "\n" +
                                    self.label_ips.get_text())

    def perform_ping(self):

        self.start_ping_thread()

    def perform_ping_start(self, hostname):
        with self.lock:
            self.hostname = hostname
            self.show_pinging()

    def perform_ping_callback(self, hostname, result):
        with self.lock:
            self.last_thread = None

            self.hostname = hostname
            self.alive = result == 0
            self.code = result

            self.show_result()

            if self.repeat:
                delay = 5 if self.alive else 1
                self.start_ping_thread(delay=delay)

    def start_ping_thread(self, solo=True, delay=0):

        if solo and self.last_thread is not None:
            self.start_count -= 1
            self.last_thread.active = False

        self.last_thread = ping_thread(self.hostname, self.perform_ping_start,
                                       self.perform_ping_callback, delay)


def start_main_window():
    MainWindow()
    Gtk.main()
