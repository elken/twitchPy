import sys
from Window import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = TwitchMain()
    t.show()
    sys.exit(app.exec_())
