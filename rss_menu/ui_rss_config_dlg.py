# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file
#   'W:\GitHub\rss_menu_plugin\rss_menu\ui_rss_config_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 280)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(396, 280))
        Dialog.setMaximumSize(QtCore.QSize(673, 406))
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.spinFrequence = QtWidgets.QSpinBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinFrequence.sizePolicy().hasHeightForWidth())
        self.spinFrequence.setSizePolicy(sizePolicy)
        self.spinFrequence.setMinimum(1)
        self.spinFrequence.setMaximum(120)
        self.spinFrequence.setProperty("value", 15)
        self.spinFrequence.setObjectName("spinFrequence")
        self.horizontalLayout_5.addWidget(self.spinFrequence)
        self.label_4 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.spinMax = QtWidgets.QSpinBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinMax.sizePolicy().hasHeightForWidth())
        self.spinMax.setSizePolicy(sizePolicy)
        self.spinMax.setMinimum(2)
        self.spinMax.setMaximum(20)
        self.spinMax.setProperty("value", 10)
        self.spinMax.setObjectName("spinMax")
        self.horizontalLayout_4.addWidget(self.spinMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableUrls = QtWidgets.QTableWidget(Dialog)
        self.tableUrls.setMinimumSize(QtCore.QSize(0, 0))
        self.tableUrls.setWordWrap(False)
        self.tableUrls.setRowCount(2)
        self.tableUrls.setColumnCount(2)
        self.tableUrls.setObjectName("tableUrls")
        item = QtWidgets.QTableWidgetItem()
        self.tableUrls.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableUrls.setHorizontalHeaderItem(1, item)
        self.tableUrls.horizontalHeader().setVisible(True)
        self.tableUrls.horizontalHeader().setCascadingSectionResizes(False)
        self.tableUrls.horizontalHeader().setDefaultSectionSize(100)
        self.tableUrls.horizontalHeader().setHighlightSections(True)
        self.tableUrls.horizontalHeader().setMinimumSectionSize(20)
        self.tableUrls.verticalHeader().setVisible(False)
        self.tableUrls.verticalHeader().setDefaultSectionSize(20)
        self.tableUrls.verticalHeader().setMinimumSectionSize(15)
        self.horizontalLayout.addWidget(self.tableUrls)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btnAdd = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAdd.sizePolicy().hasHeightForWidth())
        self.btnAdd.setSizePolicy(sizePolicy)
        self.btnAdd.setMinimumSize(QtCore.QSize(20, 20))
        self.btnAdd.setMaximumSize(QtCore.QSize(20, 20))
        self.btnAdd.setObjectName("btnAdd")
        self.verticalLayout_4.addWidget(self.btnAdd)
        self.btnRemove = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRemove.sizePolicy().hasHeightForWidth())
        self.btnRemove.setSizePolicy(sizePolicy)
        self.btnRemove.setMinimumSize(QtCore.QSize(20, 20))
        self.btnRemove.setMaximumSize(QtCore.QSize(20, 20))
        self.btnRemove.setBaseSize(QtCore.QSize(20, 20))
        self.btnRemove.setObjectName("btnRemove")
        self.verticalLayout_4.addWidget(self.btnRemove)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.btnOkCancel = QtWidgets.QDialogButtonBox(Dialog)
        self.btnOkCancel.setOrientation(QtCore.Qt.Horizontal)
        self.btnOkCancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnOkCancel.setObjectName("btnOkCancel")
        self.verticalLayout_3.addWidget(self.btnOkCancel)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        self.btnOkCancel.accepted.connect(Dialog.accept)
        self.btnOkCancel.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "RSS"))
        self.label_2.setText(_translate("Dialog", "Fréquence :"))
        self.label_4.setText(_translate("Dialog", "min"))
        self.label_3.setText(_translate("Dialog", "Nombre d\'éléments max : "))
        self.label.setText(_translate("Dialog", "Abonnements :"))
        item = self.tableUrls.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Nom"))
        item = self.tableUrls.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "URL"))
        self.btnAdd.setText(_translate("Dialog", "+"))
        self.btnRemove.setText(_translate("Dialog", "-"))

