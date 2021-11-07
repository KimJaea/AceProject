import sys
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sub_class = uic.loadUiType("subGUI.ui")[0]

class SubWindow(QMainWindow, sub_class):
    def __init__(self):
        #super(SubWindow, self).__init__(parent)
        #sub_ui = "subGUI.ui"
        #uic.loadUi(sub_ui, self)
        super().__init__()
        self.setupUi(self)

        self.label_2.setText("")
        self.label_4.setText("")

        self.btn_re.clicked.connect(self.btn_re_clicked)
        self.btn_next.clicked.connect(self.btn_next_clicked)
        self.btn_exit.clicked.connect(self.btn_exit_clicked)
        self.btn_exit.clicked.connect(QCoreApplication.instance().quit)

        self.show()

    def btn_re_clicked(self):
        #재 촬영 코드
        QMessageBox.about(self, "재활용 안내", "다시 촬영합니다.")

    def btn_next_clicked(self):
        #다음 촬영 코드
        if self.radio_1.isChecked():
            QMessageBox.about(self, "재활용 안내", "바코드를 촬영합니다.")
        elif self.radio_2.isChecked():
            QMessageBox.about(self, "재활용 안내", "인공지능으로 촬영합니다.")

    def btn_exit_clicked(self):
        #입력 정보 모두 저장
        QMessageBox.about(self, "촬영 종료", "감사합니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SubWindow()
    ex.show()

    ##sys.exit(app.exec_())
    app.exec_()
