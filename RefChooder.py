# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RefChooser.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets,uic



class RefChooser(QtWidgets.QMainWindow):

    def __init__(self, col_num = 5):
        super(RefChooser, self).__init__()
        uic.loadUi('RefChooser.ui', self)
        self.col_num = col_num

        for i in range(self.col_num):
            self.checkBox_i = QtWidgets.QCheckBox(self.centralwidget)
            self.checkBox_i.setObjectName(f"checkBox_{i}")
            self.checkBox_i.setText(f"reference_{i+1}")
            self.gridLayout.addWidget(self.checkBox_i, i, 0, 1, 1)

            self.checkBox_i.toggled.connect(self.clickedWhich)

    def clickedWhich(self):
        button_name  = self.sender()
        print(button_name.text())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = RefChooser()
    ui.show()
    sys.exit(app.exec_())
