# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\globalNuke\python\duckTools\dsCompTools\dsReader.ui'
#
# Created: Mon Aug 26 12:18:33 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_dsReader(object):
    def setupUi(self, dsReader):
        dsReader.setObjectName("dsReader")
        dsReader.resize(573, 490)
        self.gridLayout = QtGui.QGridLayout(dsReader)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.all_RB = QtGui.QRadioButton(dsReader)
        self.all_RB.setChecked(True)
        self.all_RB.setObjectName("all_RB")
        self.horizontalLayout.addWidget(self.all_RB)
        self.red_RB = QtGui.QRadioButton(dsReader)
        self.red_RB.setChecked(False)
        self.red_RB.setObjectName("red_RB")
        self.horizontalLayout.addWidget(self.red_RB)
        self.green_RB = QtGui.QRadioButton(dsReader)
        self.green_RB.setObjectName("green_RB")
        self.horizontalLayout.addWidget(self.green_RB)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.update_B = QtGui.QPushButton(dsReader)
        self.update_B.setObjectName("update_B")
        self.horizontalLayout_2.addWidget(self.update_B)
        self.explorer_B = QtGui.QPushButton(dsReader)
        self.explorer_B.setObjectName("explorer_B")
        self.horizontalLayout_2.addWidget(self.explorer_B)
        self.doIt3_B = QtGui.QPushButton(dsReader)
        self.doIt3_B.setObjectName("doIt3_B")
        self.horizontalLayout_2.addWidget(self.doIt3_B)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.tableWidget = QtGui.QTableWidget(dsReader)
        self.tableWidget.setMinimumSize(QtCore.QSize(457, 272))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setIconSize(QtCore.QSize(75, 75))
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(75)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(75)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)

        self.retranslateUi(dsReader)
        QtCore.QObject.connect(self.update_B, QtCore.SIGNAL("clicked()"), dsReader.close)
        QtCore.QMetaObject.connectSlotsByName(dsReader)

    def retranslateUi(self, dsReader):
        dsReader.setWindowTitle(QtGui.QApplication.translate("dsReader", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.all_RB.setText(QtGui.QApplication.translate("dsReader", "all", None, QtGui.QApplication.UnicodeUTF8))
        self.red_RB.setText(QtGui.QApplication.translate("dsReader", "update", None, QtGui.QApplication.UnicodeUTF8))
        self.green_RB.setText(QtGui.QApplication.translate("dsReader", "latest", None, QtGui.QApplication.UnicodeUTF8))
        self.update_B.setText(QtGui.QApplication.translate("dsReader", "update", None, QtGui.QApplication.UnicodeUTF8))
        self.explorer_B.setText(QtGui.QApplication.translate("dsReader", "explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.doIt3_B.setText(QtGui.QApplication.translate("dsReader", "doSomething", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("dsReader", "icon", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("dsReader", "ver", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("dsReader", "path", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("dsReader", "pathStart", None, QtGui.QApplication.UnicodeUTF8))
