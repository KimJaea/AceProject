import cv2
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

global camera, image

class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

class ShowVideo(QtCore.QObject):
    camera = cv2.VideoCapture(0)

    ret, image = camera.read()
    height, width = image.shape[:2]
    # height, width = 360, 480

    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):

        run_video = True
        while run_video:
            ret, image = self.camera.read()
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            qt_image = QtGui.QImage(color_swapped_image.data, self.width, self.height,
                                    color_swapped_image.strides[0], QtGui.QImage.Format_RGB888)
            self.VideoSignal.emit(qt_image)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    def userAuth(self):
        print("사용자 인증")
        
    def barcode(self):
        print("바코드 인식")

    def stuff(self):
        print("물체 인식")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    image_viewer = ImageViewer()
    vid.VideoSignal.connect(image_viewer.setImage)

    font = QtGui.QFont()
    font.setPointSize(20)
    font.setBold(True)

    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('사용자 인증')
    push_button3 = QtWidgets.QPushButton('바코드 인식')
    push_button4 = QtWidgets.QPushButton('물체 인식')
    push_button5 = QtWidgets.QPushButton('종료')

    push_button1.setFont(font)
    push_button2.setFont(font)
    push_button3.setFont(font)
    push_button4.setFont(font)
    push_button5.setFont(font)

    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.userAuth)
    push_button3.clicked.connect(vid.barcode)
    push_button4.clicked.connect(vid.stuff)
    push_button5.clicked.connect(sys.exit)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout1 = QtWidgets.QHBoxLayout()
    horizontal_layout2 = QtWidgets.QHBoxLayout()    
    horizontal_layout3 = QtWidgets.QHBoxLayout()

    horizontal_layout1.addWidget(image_viewer)
    horizontal_layout2.addWidget(push_button2)
    horizontal_layout2.addWidget(push_button3)
    horizontal_layout3.addWidget(push_button4)
    horizontal_layout3.addWidget(push_button5)
    
    vertical_layout.addWidget(push_button1)
    vertical_layout.addLayout(horizontal_layout1)
    vertical_layout.addLayout(horizontal_layout2)
    vertical_layout.addLayout(horizontal_layout3)
    
    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.setWindowTitle('쓰레기통')
    main_window.setWindowIcon(QIcon('.\\image.png'))
    main_window.resize(640 , 480)
    main_window.show()
    
    sys.exit(app.exec_())
