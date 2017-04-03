# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name            : rss_menu plugin
Description          : Rss reader
Date                 : Feb 2012
copyright            : (C) 2011 by AEAG
email                : xavier.culos@eau-adour-garonne.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


def classFactory(iface):
    # load aeag_mask class from file aeag_mask
    from .rss_menu import rss_menu
    return rss_menu(iface)
