import sys

from types import *
from .ui_rss_config_dlg import Ui_rss_config_dlg

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *
from osgeo import ogr

class Rss_config_dlg(QDialog, Ui_rss_config_dlg):

    def __init__(self, parent, plugin):
        self.plugin = plugin
        QDialog.__init__(self, parent)
        self.setupUi(self)
     
        #self.defaultcursor = self.cursor

        #QObject.connect(self.tableResult, SIGNAL("cellDoubleClicked(int,int)"), self.onChoose)
        #QObject.connect(self.editSearch, SIGNAL("returnPressed()"), self.onReturnPressed)
        QObject.connect(self.btnAdd, SIGNAL("clicked()"), self.onAdd)
        QObject.connect(self.btnRemove, SIGNAL("clicked()"), self.onRemove)
        QObject.connect(self, SIGNAL("finished(int)"), self.onFinished)
        
        self.tableUrls.setRowCount(len(self.plugin.urls))

        self.spinFrequence.setValue(self.plugin.setting_frequence)
        self.spinMax.setValue(self.plugin.setting_max_elt)


        idx = 0
        for url in self.plugin.urls:
            item = QTableWidgetItem(url["name"])
            self.tableUrls.setItem(idx, 0, item)
            item = QTableWidgetItem(url["url"])
            self.tableUrls.setItem(idx, 1, item)
            idx = idx+1
            
        self.tableUrls.resizeColumnToContents(0)
        self.tableUrls.resizeColumnToContents(1)
            
    def onDoubleClicked(self):
        pass
        #self.plugin.iface.mainWindow().statusBar().showMessage("dbl clicked")

    def onFinished(self, result):
        if result:
            self.plugin.setting_frequence = self.spinFrequence.value()
            self.plugin.setting_max_elt = self.spinMax.value()
            
            self.plugin.urls = []
            for row in range(self.tableUrls.rowCount()):
                #QMessageBox.information(None, "Cancel", "Read " + str(row))
                name = self.tableUrls.item(row, 0).text().strip()
                url  = self.tableUrls.item(row, 1).text().strip()
                if (name != "") and (url != ""):
                    self.plugin.urls.append({"name":name, "url":url})

    def onClose(self):
        self.done(0)

    def onAdd(self):
        self.tableUrls.setRowCount(self.tableUrls.rowCount()+1)

    def onRemove(self):
        for item in self.tableUrls.selectedItems():
            self.tableUrls.removeRow(item.row())
