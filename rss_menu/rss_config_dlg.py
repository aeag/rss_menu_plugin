# -*- coding: utf-8 -*-
from .ui_rss_config_dlg import Ui_Dialog

from PyQt5.QtWidgets import QDialog, QTableWidgetItem


class Rss_config_dlg(QDialog, Ui_Dialog):

    def __init__(self, parent, plugin):
        self.plugin = plugin
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # self.defaultcursor = self.cursor

        self.btnAdd.clicked.connect(self.onAdd)
        self.btnRemove.clicked.connect(self.onRemove)
        self.finished.connect(self.onFinished)

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

    def onFinished(self, result):
        if result:
            self.plugin.setting_frequence = self.spinFrequence.value()
            self.plugin.setting_max_elt = self.spinMax.value()

            self.plugin.urls = []
            for row in range(self.tableUrls.rowCount()):
                name = self.tableUrls.item(row, 0).text().strip()
                url = self.tableUrls.item(row, 1).text().strip()
                if (name != "") and (url != ""):
                    self.plugin.urls.append({"name": name, "url": url})

    def onClose(self):
        self.done(0)

    def onAdd(self):
        self.tableUrls.setRowCount(self.tableUrls.rowCount()+1)

    def onRemove(self):
        for item in self.tableUrls.selectedItems():
            self.tableUrls.removeRow(item.row())
