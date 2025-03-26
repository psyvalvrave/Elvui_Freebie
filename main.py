# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import sys
from app import App, load_config

def main():
    config = load_config()
    app = QApplication(sys.argv)
    App.apply_styles(app)
    ex = App(config)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
