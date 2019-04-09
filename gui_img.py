# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import urllib.request
import numpy as np
from prog import Movie
import imdb
import sys
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(620, 20, 91, 41))
        self.search_button.setObjectName("search_button")
        self.search_box = QtWidgets.QLineEdit(self.centralwidget)
        self.search_box.setGeometry(QtCore.QRect(280, 20, 321, 41))
        self.search_box.setToolTip("")
        self.search_box.setToolTipDuration(1)
        self.search_box.setObjectName("search_box")
        self.movie_label = QtWidgets.QLabel(self.centralwidget)
        self.movie_label.setGeometry(QtCore.QRect(160, 30, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.movie_label.setFont(font)
        self.movie_label.setObjectName("movie_label")
        self.Synopsis = QtWidgets.QTextEdit(self.centralwidget)
        self.Synopsis.setGeometry(QtCore.QRect(10, 150, 781, 401))
        self.Synopsis.setObjectName("Synopsis")
        self.Synopsis_label = QtWidgets.QLabel(self.centralwidget)
        self.Synopsis_label.setGeometry(QtCore.QRect(300, 130, 131, 20))
        self.Synopsis_label.setObjectName("Synopsis_label")
        self.imglabel = QtWidgets.QLabel(self.centralwidget)
        self.imglabel.setGeometry(QtCore.QRect(50, 0, 271, 181)) # 271,181 changed to 600, 600
        self.imglabel.setObjectName("imglabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IMDB_helper"))
        self.search_button.setText(_translate("MainWindow", "Search"))
        self.search_button.clicked.connect(self.on_search)
        self.movie_label.setText(_translate("MainWindow", "Enter movie name  "))
        self.Synopsis_label.setText(_translate("MainWindow", "Synopsis of the movie"))
        self.imglabel.setText(_translate("MainWindow", ""))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.triggered.connect(self.on_close)

    def on_search(self):
        ia = imdb.IMDb()
        result = ia.search_movie(self.search_box.text())
        movie = ia.get_movie(ia.get_imdbID(result[0]))
        print(movie['cover url'])
        req = urllib.request.urlopen(movie['cover url'])
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        # what percent of the original size is retained
        scale = 70
        # changing the output image to the desired size
        width = int(img.shape[1] * scale /100)
        height = int(img.shape[0] * scale /100)
        dim= (width, height)
        resized = cv2.resize(img,dim, interpolation = cv2.INTER_AREA)
        height, width, channel = resized.shape
        bytesperline = 3*width
        qImg = QtGui.QImage(resized.data, width, height, bytesperline, QtGui.QImage.Format_RGB888).rgbSwapped()
        pix = QtGui.QPixmap(qImg)
        self.imglabel.setPixmap(pix)
        self.Synopsis.clear()
        self.Synopsis.append(self.search_box.text())
        self.Synopsis.append(Movie(self.search_box.text()).get_synopsis())

    def on_close(self):
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())