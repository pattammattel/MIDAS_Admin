# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RefChooser.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtCore import pyqtSignal

from StackCalcs import *
dff,col_name = create_df_from_nor(athenafile='marked2.nor')


class RefChooser(QtWidgets.QMainWindow):
    
    signal: pyqtSignal = QtCore.pyqtSignal(list)

    def __init__(self, ref_names = col_name):
        super(RefChooser, self).__init__()
        uic.loadUi('RefChooser.ui', self)
        self.ref_names = ref_names

        self.all_boxes = []

        for n,i in enumerate(self.ref_names):
            self.cb_i = QtWidgets.QCheckBox(self.centralwidget)
            if n == 0:
                self.cb_i.setChecked(True)
                self.cb_i.setEnabled(False)
            self.cb_i.setObjectName(i)
            self.cb_i.setText(i)
            self.gridLayout.addWidget(self.cb_i, n, 0, 1, 1)
            #self.cb_i.toggled.connect(self.clickedWhich)
            self.all_boxes.append(self.cb_i)

        self.pb_apply = QtWidgets.QPushButton(self.centralwidget)
        self.pb_apply.setText("Apply")
        self.gridLayout.addWidget(self.pb_apply, len(self.ref_names)+1, 0, 1, 1)

        self.pb_apply.clicked.connect(self.clickedWhichAre)

    def clickedWhich(self):
        button_name = self.sender()
        print(button_name.objectName())

    QtCore.pyqtSlot()
    def clickedWhichAre(self):

        self.onlyCheckedBoxes = []

        for names in self.all_boxes:
            if names.isChecked():
                self.onlyCheckedBoxes.append(names.objectName())
        self.signal.emit(self.onlyCheckedBoxes)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = RefChooser()
    ui.show()
    sys.exit(app.exec_())
