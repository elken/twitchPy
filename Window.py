import fnmatch
import tempfile
import time

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from Twitch import *
from ui import *


class TwitchMain(QMainWindow):

    def __init__(self):
        """
        Primary Twitch.py window
        :return: A Twitchy.py window object
        """
        super(TwitchMain, self).__init__()
        self.ui = Ui_TwitchWindow()
        self.ui.setupUi(self)
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "TwitchPy", "config")
        self.token = self.settings.value("token")
        self.acc_name = self.settings.value("name")
        print('Using ' + self.temp_dir + ' as temp dir.')
        start_time = time.time()
        self.twitch = Twitch(self.temp_dir, self.settings)
        end_time = time.time()
        print('Took %f' % (end_time - start_time))
        # self.main_layout = QGridLayout()
        # self.left_layout = QVBoxLayout()
        # self.center_layout = QGridLayout()
        # self.right_layout = QVBoxLayout()
        # self.top_bar = QHBoxLayout()
        # self.left_layout.addWidget(QLabel("Left"))
        # self.top_bar.addWidget(QLabel("Top"))
        # self.center_layout.addWidget(QLabel("Center"))
        # self.right_layout.addWidget(QLabel("Right"))
        #
        # self.main_layout.addItem(self.left_layout)
        # self.main_layout.addItem(self.top_bar)
        # self.main_layout.addItem(self.center_layout)
        # self.main_layout.addItem(self.right_layout)
        # self.setLayout(self.main_layout)

    @property
    def temp_dir(self):
        try:
            self._temp_dir
        except AttributeError:
            _dir = self.iter_temp_dirs()

            if _dir:
                return os.path.join(tempfile.gettempdir(), _dir)
            else:
                return tempfile.mkdtemp(prefix='twitchpy_')

    @staticmethod
    def iter_temp_dirs():
        for i in os.listdir(tempfile.gettempdir()):
            if fnmatch.fnmatch(i, 'twitchpy_*'):
                return i

    @property
    def acc_name(self):
        return self._acc_name

    @acc_name.setter
    def acc_name(self, value):
        self._acc_name = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @temp_dir.setter
    def temp_dir(self, value):
        self._temp_dir = value
