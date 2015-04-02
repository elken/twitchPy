from twitch import *
import posixpath
from gi.repository import Gtk, GdkPixbuf, Gdk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Twitch.py")
        self.set_border_width(10)
        self.set_default_size(800, 600)
        self.t = Twitch()

        header = Gtk.HeaderBar(title="Twitch.py")
        header.set_subtitle("Watching: Nothing")
        header.props.show_close_button = True 

        self.set_titlebar(header)
        
        w,h = self.get_size()
        box = Gtk.VBox(spacing=w/5)
        box = self.drawChannelBox()
        label = Gtk.Label("Test")

        player = Gtk.VBox()
        player.pack_start(label, True, True, 0)

        mainBox = Gtk.HBox()
        mainBox.pack_start(box, False, False, 0)
        mainBox.pack_start(player, True, True, 0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(mainBox)

        self.add(scrolled)
        self.show_all()


    def resizeImage(self, filename=None, width=None, height=None):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
            return pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

    def drawChannelBox(self):
        imBox = Gtk.VBox()
        nameBox = Gtk.VBox()
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.t.parseFollows()
        self.t.parseImageURL()
        self.t.getLogos()

        images = self.t.returnImageURL()
        temp = self.t.returnTempDir()

        viewIcon = Gtk.Image()
        viewIcon.set_from_file("res/svg-glyph_live.png")

        folIcon = Gtk.Image()
        folIcon.set_from_file("res/svg-glyph_followers.png")
        for k, v in images.items():
            userLabel = Gtk.Label('<span font_family="HelveticaNeue" font="12">' + k.strip('"') + '</span>')
            playingLabel = Gtk.Label('<span font_family="HelveticaNeue" font="8">Playing</span>')
            viewLabel = Gtk.Label('<span font_family="HelveticaNeue" font="7">100</span>')
            folLabel = Gtk.Label('<span font_family="HelveticaNeue" font="7">100</span>')

            image = Gtk.Image()
            image.set_from_pixbuf(self.resizeImage(filename=os.path.join(temp,posixpath.basename(v)), width=40, height=40))

            mainBox = Gtk.HBox()
            viewFolBox = Gtk.VBox()

            userLabel.set_use_markup(True)
            playingLabel.set_use_markup(True)
            viewLabel.set_use_markup(True)
            folLabel.set_use_markup(True)

            imBox.pack_start(image, True, True, 0)
            nameBox.pack_start(userLabel, True, True, 0)
            nameBox.pack_start(playingLabel, True, True, 0)
            viewFolBox.pack_start(viewIcon, True, True, 0)
            viewFolBox.pack_start(viewLabel, True, True, 0)
            viewFolBox.pack_start(folIcon, True, True, 0)
            viewFolBox.pack_start(folLabel, True, True, 0)
            mainBox.pack_start(imBox, True, True, 0)
            mainBox.pack_start(nameBox, True, True, 0)
            mainBox.pack_start(viewFolBox, True, True, 0)
            scrolled.add(mainBox)

        return scrolled

    def run(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()
