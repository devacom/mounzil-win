# -*- coding: utf-8 -*-
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# This project uses pyside6
try:
    from PySide6.QtCore import Qt, QSize, QPoint, QFile, QIODevice, QTextStream
    from PySide6.QtWidgets import QWidget
    from PySide6.QtGui import QIcon
except:
    from PyQt5.QtCore import Qt, QSize, QPoint, QFile, QIODevice, QTextStream
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtGui import QIcon

from mounzil.gui.about_ui import AboutWindow_Ui
from mounzil.gui import resources

class AboutWindow(AboutWindow_Ui):
    def __init__(self, mounzil_setting):
        super().__init__(mounzil_setting)

        self.mounzil_setting = mounzil_setting

        # setting window size and position
        size = self.mounzil_setting.value(
            'AboutWindow/size', QSize(545, 375))
        position = self.mounzil_setting.value(
            'AboutWindow/position', QPoint(300, 300))

        # read translators.txt files.
        # this file contains all translators.
        f = QFile(':/translators.txt')

        f.open(QIODevice.ReadOnly | QFile.Text)
        f_text = QTextStream(f).readAll()
        f.close()

        self.translators_textEdit.insertPlainText(f_text)



        self.resize(size)
        self.move(position)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def changeIcon(self, icons):
        icons = ':/' + str(icons) + '/'
        self.pushButton.setIcon(QIcon(icons + 'ok'))

    def closeEvent(self, event):
        # saving window size and position
        self.mounzil_setting.setValue('AboutWindow/size', self.size())
        self.mounzil_setting.setValue('AboutWindow/position', self.pos())
        self.mounzil_setting.sync()
        event.accept()
