from PyQt5 import QtCore, QtGui, QtWidgets,uic
from RefChooser import *
dff,col_name = create_df_from_nor(athenafile='marked2.nor')

class RefRec(QtWidgets.QMainWindow):

    def __init__(self):
        super(RefRec, self).__init__()
        uic.loadUi('RefReciever.ui', self)
        self.pb_open_window.clicked.connect(self.open_window)

    def open_window(self):
        self.new_window = RefChooser()
        self.new_window.show()
        self.new_window.signal.connect(self.print_list)

    def print_list(self, list_):
        print(dff[list_].head())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = RefRec()
    ui.show()
    sys.exit(app.exec_())