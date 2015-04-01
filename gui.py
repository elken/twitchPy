from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

class MainWindow(Gtk.Window):
    def run(self):
        builder = Gtk.Builder()
        builder.add_from_file("main.glade")
        builder.connect_signals(Handler())

        label1 = Gtk.Label("Panel label")
        label2 = Gtk.Label("Panel label2")
        panel = builder.get_object("mainPanel")

        panel.pack1(label1)
        panel.pack2(label2)

        window = builder.get_object("mainWindow")
        window.show_all()
        Gtk.main()
