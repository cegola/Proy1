# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'venSalir.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_venSalir(object):
    def setupUi(self, venSalir):
        venSalir.setObjectName("venSalir")
        venSalir.resize(400, 142)
        venSalir.setModal(True)
        self.btnBoxSalir = QtWidgets.QDialogButtonBox(venSalir)
        self.btnBoxSalir.setGeometry(QtCore.QRect(210, 90, 161, 32))
        self.btnBoxSalir.setOrientation(QtCore.Qt.Horizontal)
        self.btnBoxSalir.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.btnBoxSalir.setCenterButtons(True)
        self.btnBoxSalir.setObjectName("btnBoxSalir")
        self.lblMenSalir = QtWidgets.QLabel(venSalir)
        self.lblMenSalir.setGeometry(QtCore.QRect(100, 50, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblMenSalir.setFont(font)
        self.lblMenSalir.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblMenSalir.setObjectName("lblMenSalir")
        self.lblImgSalir = QtWidgets.QLabel(venSalir)
        self.lblImgSalir.setGeometry(QtCore.QRect(40, 40, 41, 41))
        self.lblImgSalir.setText("")
        self.lblImgSalir.setPixmap(QtGui.QPixmap("img/iconoSalir.png"))
        self.lblImgSalir.setScaledContents(True)
        self.lblImgSalir.setObjectName("lblImgSalir")

        self.retranslateUi(venSalir)
        self.btnBoxSalir.accepted.connect(venSalir.accept)
        self.btnBoxSalir.rejected.connect(venSalir.reject)
        QtCore.QMetaObject.connectSlotsByName(venSalir)

    def retranslateUi(self, venSalir):
        _translate = QtCore.QCoreApplication.translate
        venSalir.setWindowTitle(_translate("venSalir", "¿Desea salir?"))
        self.lblMenSalir.setText(_translate("venSalir", "¿Está seguro que quiere salir de la aplicación?"))

