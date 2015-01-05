"""
/***************************************************************************
Name                  : rss_menu 
Description          : Rss feed reader...
Date                 : Feb/11 
copyright            : (C) 2011 by AEAG
email                : xavier.culos@eau-adour-garonne.fr 
versions:
  todo : tri descendant
  todo : config
    - icone animée
    - freq
    - max elements
    - liste url + nom
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 
pyrcc4 -o resources.py resources.qrc
pyuic4 ui_rss_config_dlg.ui > ui_rss_config_dlg.ui.py
QMessageBox.information(None, "Cancel", "message")
 
"""
# Import the PyQt and QGIS libraries
import os
from PyQt4 import QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
import urllib
from xml.dom.minidom import *
from feedparser.feedparser import *
from rss_config_dlg import Rss_config_dlg
import webbrowser
import htmllib
from htmlentitydefs import name2codepoint as n2cp
import re
import operator
#import threading

# Initialize Qt resources from file resources.py
import resources

def substitute_entity(match):
    ent = match.group(3)
    
    if match.group(1) == "#":
        if match.group(2) == '':
            return unichr(int(ent))
        elif match.group(2) == 'x':
            return unichr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )
            
def decode_htmlentities(string):
    entity_re = re.compile(r'&(#?)(x?)(\w+);')
    return entity_re.subn(substitute_entity, unicode(string))[0]

#def _check(s):
#    s._check_for_updates()

class rss_menu: 

  def __init__(self, iface):
    # Save reference to the QGIS interface
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf8"));
    
    self.iface = iface
    self.toolBar = None
    self.act_rss_menu = None
    self.act_aeag_toolbar_help = None
    self.canvas = self.iface.mapCanvas()
    self.timer_update = None
    self.icon = None
    self.menu = None
    self.urls = []
    self.feeds = {}
    self.menu_is_visible = False
    self.inProgress = False
    self.iconVisible = False
    self.menuVisible = True
    
    self.visited_feeds = {}
    self.setting_max_elt = 10
    self.setting_frequence = 15
    self.read()
    
  def store(self):
    s = QSettings()
    s.setValue("rss_menu/max_elt", self.setting_max_elt)
    s.setValue("rss_menu/frequence", self.setting_frequence)
     
    index = 0
    s.beginWriteArray("rss_menu/visited_feeds")
    for feeId, entries  in self.visited_feeds.iteritems():
        for entryId, value in entries.iteritems():
            if value:
                #QMessageBox.information(None, "Cancel", entryId)
                s.setArrayIndex(index)
                s.setValue("feedId", feeId)
                s.setValue("entryId", entryId)
                index = index + 1
    s.endArray()
    #QMessageBox.information(None, "Cancel", "Store " +  str(index))
    index = 0
    s.beginWriteArray("rss_menu/urls")
    for url  in self.urls:
        s.setArrayIndex(index)
        s.setValue("url", url["url"])
        s.setValue("name", url["name"])
        index = index + 1
    s.endArray()

  def read(self):
    try:
        s = QSettings()
        self.setting_max_elt = s.value("rss_menu/max_elt", 10, type=int)
        self.setting_frequence = s.value("rss_menu/frequence", 15, type=int)
        
        size = s.beginReadArray("rss_menu/visited_feeds")
        #QMessageBox.information(None, "Cancel", "Read " + str(size))
        for i in range(size):
            s.setArrayIndex(i)
            feeId = str(s.value("feedId"))
            entryId = str(s.value("entryId"))
            if not(feeId in self.visited_feeds):
                self.visited_feeds[feeId] = {}
            self.visited_feeds[feeId][entryId] = True
        s.endArray()
    
        size = s.beginReadArray("rss_menu/urls")
        for i in range(size):
            s.setArrayIndex(i)
            url = s.value("url")
            name = s.value("name")
            self.urls.append({"url":url, "name":name})
        s.endArray()

        if len(self.urls) == 0:
            raise Exception("")
    except:    
        self.urls = []
        self.urls.append({"url":"http://adour-garonne.eaufrance.fr/index2.php?option=ds-syndicate&version=1&feed_id=1", "name":"SIE AG"})

  def initGui(self):  
    self.toolBar = self.iface.pluginToolBar()
    
    # <specific_aeag>    
    toolbars = self.iface.mainWindow().findChildren(QToolBar)
    self.toolBar = self.iface.pluginToolBar()
    toolbars = self.iface.mainWindow().findChildren(QToolBar)
    toolbarFound = False
    for toolbar in toolbars:
       if toolbar.objectName() == "aeag_toolbar":
           self.toolBar = toolbar
           toolbarFound = True
    if not toolbarFound:
       self.toolBar = self.iface.addToolBar("A.E.A.G. Outils")
       self.toolBar.setObjectName("aeag_toolbar")
    # </specific_aeag>    
        
    self.icon = QIcon(":plugins/rss_menu/rss_menu.png")
    self.icon_news = QIcon(":plugins/rss_menu/rss_menu_2.png")
    self.act_rss_menu = QAction(self.icon, ("Flux RSS..."), self.iface.mainWindow())

    if self.iconVisible:
        self.toolBar.addAction(self.act_rss_menu)
    
    # Add actions to the toolbar
    QObject.connect(self.act_rss_menu, SIGNAL("triggered()"), self.do_rss_menu)
    
    self.menu = QtGui.QMenu("Actualités")
    self.action_config = self.menu.addAction("Configuration...")
    QObject.connect(self.action_config, SIGNAL("triggered()"), self.do_config)
    QObject.connect(self.menu, SIGNAL("aboutToHide()"), self.do_menu_hide)
    QObject.connect(self.menu, SIGNAL("aboutToShow()"), self.do_menu_show)
    
    self.yaUpdates = False

    self.timer_update = QTimer()
    QObject.connect(self.timer_update, SIGNAL("timeout()"), self.do_check_for_updates)
    self.m_gif = QMovie(":plugins/rss_menu/rss_menu.gif")
    QObject.connect(self.m_gif, SIGNAL("frameChanged(int)"), self.do_update_icon)
    
    self.do_check_for_updates()
    self.timer_update.start(self.setting_frequence*60*1000)

  def unload(self):
    self.toolBar.removeAction(self.act_rss_menu)
    self.m_gif.stop()
    self.timer_update.stop();

    del self.menu
    self.menu = None

    self.store()


  def do_rss_menu(self): 
    if not self.inProgress:
        self.menu.exec_(QtGui.QCursor.pos())

  def build_menu(self):
      self.menu.clear()
      
      for idFeed, feed in self.feeds.iteritems():
          if len(self.feeds) > 1:
              sousmenu = self.menu.addMenu(feed["title"])
              if feed["error"] :
                  yaNews = True
                  font = QFont()
                  font.setItalic(True)
                  sousmenu.menuAction().setFont(font)

      
          #sorted(self.feeds[idFeed]["entries"], key=lambda entry: entry[0], reverse=True)
          items = self.feeds[idFeed]["entries"].items()
          yaNews = False
              
          for idEntry, entry in sorted(items, key=lambda e: e[0], reverse=True):
              #entry = self.feeds[idFeed]["entries"][idEntry]
              #QMessageBox.information(None, "Cancel", entry[0])
              lib = decode_htmlentities((entry["title"]))
              action = QAction(entry["date"] + " - " + lib, self.iface.mainWindow())

              if not(entry["visited"]) and (entry["link"].strip() != ""):
                  yaNews = True
                  font = QFont()
                  font.setBold(True)
                  action.setFont(font)
                
              desc = entry["description"]
              desc = decode_htmlentities((wrap((desc), 100)))
              desc = re.sub(r'\n\n','\n', desc)
              desc = re.sub(r'\t',' ', desc)
              action.setToolTip(desc)

              if len(self.feeds) > 1:
                  QObject.disconnect(self.menu, SIGNAL("hovered(QAction *)"), self._actionHovered)
                  QObject.connect(sousmenu, SIGNAL("hovered(QAction *)"), self._actionHovered)
              else:
                  QObject.connect(self.menu, SIGNAL("hovered(QAction *)"), self._actionHovered)
              
              if len(self.feeds) > 1:
                  sousmenu.addAction(action)
              else:
                  self.menu.addAction(action)

              if entry["link"].strip() != "":
                  QObject.connect(action, SIGNAL("triggered()"), lambda feed=idFeed, entry=idEntry: self.do_entry_link(feed, entry))
              else:
                  if not idFeed in self.visited_feeds:
                      self.visited_feeds[idFeed] = {}
                  self.visited_feeds[idFeed][idEntry] = True
    
          if (len(self.feeds) > 1) and yaNews:
              font = QFont()
              font.setBold(True)
              sousmenu.menuAction().setFont(font)
          
          if len(self.feeds) > 1:
              sousmenu.addSeparator()
              action_read = sousmenu.addAction("Marquer comme lu")
          else:
              self.menu.addSeparator()
              action_read = self.menu.addAction("Marquer comme lu")
              
          QObject.connect(action_read, SIGNAL("triggered()"), lambda feed=idFeed: self.mark_as_read(feed))
          
      self.menu.addSeparator()
      self.action_config = self.menu.addAction("Configuration...")
      QObject.connect(self.action_config, SIGNAL("triggered()"), self.do_config)
      
      if self.menuVisible:
          menuBar = self.iface.editMenu().parentWidget() 
          menuBar.addMenu(self.menu)      
      
  def _check_for_updates(self):
      new_feed = False
      self.feeds = {}
      self.inProgress = True
      #QMessageBox.information(None, "Cancel", "in progress")
      
      for url in self.urls:
          myfeed = parse(url["url"])
          
          idFeed = url["url"]
          self.feeds[idFeed] = {}
          self.feeds[idFeed]["entries"] = {}
          self.feeds[idFeed]["error"] = False
          self.feeds[idFeed]["title"] = url["name"]

          if not "title" in myfeed["feed"]:
              self.feeds[idFeed]["error"] = True
              continue
          
          cnt = 0
          for item in myfeed["entries"]:
              if cnt > self.setting_max_elt:
                  pass
              
              date = QDate(item.date_parsed[0], item.date_parsed[1], item.date_parsed[2])
              time = QTime(item.date_parsed[3], item.date_parsed[4], item.date_parsed[5])
              dateTime = QDateTime(date, time)
              datelocale = QLocale().toString(date, QLocale.ShortFormat)
              
              idEntry = str(dateTime.toString("yyyyMMddHHmmss"))
              self.feeds[idFeed]["entries"][idEntry] = {}
              
              self.feeds[idFeed]["entries"][idEntry][0] = idEntry
              self.feeds[idFeed]["entries"][idEntry]["date"] = datelocale
              self.feeds[idFeed]["entries"][idEntry]["link"] = item.link
              self.feeds[idFeed]["entries"][idEntry]["title"] = item.title
              self.feeds[idFeed]["entries"][idEntry]["description"] = item.description
              visited = ((idFeed in self.visited_feeds) and (idEntry in self.visited_feeds[idFeed]))
              self.feeds[idFeed]["entries"][idEntry]["visited"] = visited
              new_feed = new_feed or (not visited)
      
          #self.feeds = sorted(self.feeds[idFeed]["entries"], key=lambda entry: entry[0], reverse=True)
          #sorted(self.feeds[idFeed]["entries"], lambda x, y: cmp(x["date"], y["date"]), reverse=True)
          
      self.yaUpdates = new_feed
      self.build_menu()

      # clean visited_feeds dictionary from olders entries   
      for feeId  in self.visited_feeds.keys():
          if not (feeId in self.feeds):
              del self.visited_feeds[feeId]
          else:
              for entryId in self.visited_feeds[feeId].keys():
                  if not entryId in self.feeds[feeId]["entries"]:
                      del self.visited_feeds[feeId][entryId]      

      if self.yaUpdates:
          self.m_gif.start()
          newIcon = QIcon(self.m_gif.currentPixmap())
          self.act_rss_menu.setIcon(newIcon)
      else:
          self.m_gif.stop()
          self.act_rss_menu.setIcon(self.icon)

      #QMessageBox.information(None, "Cancel", "end progress")
      self.inProgress = False

  def check_for_updates(self):
      if self.menu_is_visible or self.inProgress:
          pass
          #QMessageBox.information(None, "Cancel", "...")
      else:
          self._check_for_updates()
          #threading.Thread(target = _check, args=(self,)).start()
          
      return True
      
  def _actionHovered(self, action): 
      tip = action.toolTip() 
      QToolTip.showText(QCursor.pos(), tip) 
        
  def mark_as_read(self, feedId):
    for entryId, entries in self.feeds[feedId]["entries"].iteritems():
        if not feedId in self.visited_feeds:
            self.visited_feeds[feedId] = {}
            
        self.visited_feeds[feedId][entryId] = True
        self.feeds[feedId]["entries"][entryId]["visited"] = True
        
    self.build_menu()
    
  def do_entry_link(self, idFeed, idEntry):
      #QMessageBox.information(None, "Cancel", self.feeds[idFeed]["entries"][idEntry]["link"])
      if self.feeds[idFeed]["entries"][idEntry]["link"].strip() != "":
          webbrowser.open(self.feeds[idFeed]["entries"][idEntry]["link"], 1)
          
          if not(idFeed in self.visited_feeds):
              self.visited_feeds[idFeed] = {}
                  
          self.visited_feeds[idFeed][idEntry] = True
          self.feeds[idFeed]["entries"][idEntry]["visited"] = True
          
          self.build_menu()
  
  def do_check_for_updates(self):
    self.check_for_updates()

  def do_update_icon(self):
      try: # to prevent initial state pb
          newIcon = QIcon(self.m_gif.currentPixmap())
          self.act_rss_menu.setIcon(newIcon)
      except:
          pass
      
  def deactivate(self):
    pass

  def do_menu_hide(self):
    #QMessageBox.information(None, "Cancel", "hide")
    self.menu_is_visible = False

  def do_menu_show(self):
    self.menu_is_visible = True

  def do_config(self):
    self.timer_update.stop()
    
    dlg = Rss_config_dlg(self.iface.mainWindow(), self)
    if dlg.exec_() == 1:
        self.do_check_for_updates()
        if self.iconVisible:
            self.toolBar.addAction(self.act_rss_menu)
        else:
            self.toolBar.removeAction(self.act_rss_menu)
            
    self.timer_update.start(self.setting_frequence*60*1000)
