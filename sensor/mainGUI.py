import sys, os
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

main_class = uic.loadUiType("mainGUI.ui")[0]

class SubWindow(QDialog):
    def __init__(self, parent):
        super(SubWindow, self).__init__(parent)
        sub_ui = "subGUI.ui"
        uic.loadUi(sub_ui, self)

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

class MainWindow(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.main_btn.clicked.connect(self.main_btn_clicked)
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(QCoreApplication.instance().quit)

    def main_btn_clicked(self):
        QMessageBox.about(self, "회원 인증", "QR 코드를 입력해 주세요.")
        ## 카메라로 QR 코드 촬영
        
        #QCoreApplication.exit(0)
        #QApplication.quit()
        
        #app = QApplication(sys.argv)
        #app.quit()
        self.close()

    def btn1_clicked(self):
        QMessageBox.about(self, "신고 안내", "현재 서비스 준비중입니다.")        
    
    def closeEvent(self, QCloseEvent):
        # self.deleteLater()        
        # QR 코드 인증 부분
        QCloseEvent.accept()
        QMessageBox.about(self, "인증 완료", "환영합니다.")
        os.startfile('.\\subGUI.py')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ##ex.show()
    ##app.exec_()
    
    sys.exit(app.exec_())
