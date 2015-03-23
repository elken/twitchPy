from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Twitch client")

        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")

    def run(self):
        window = self.builder.get_object("mainWindow")
        window.connect("delete-event", Gtk.main_quit)
        window.show_all()
        Gtk.main()
