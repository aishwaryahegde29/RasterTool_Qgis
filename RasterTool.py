# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterTool
                                 A QGIS plugin
 Extract Pixel value from raster files and analyse
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-06-13
        git sha              : $Format:%H$
        copyright            : (C) 2019 by NITK
        email                : aishwaryahegde29@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .RasterTool_dialog import RasterToolDialog
import os.path
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtWidgets import *
# Initialize Qt resources from file resources.py
from nltk import infile

from .resources import *
# Import the code for the dialog
from osgeo import gdal
import os.path
import processing, os, subprocess, time
from qgis.utils import *
from qgis.core import *
from qgis.gui import QgsMessageBar
# from qgis.PyQt.QtGui import QProgressBar
from qgis.PyQt.QtCore import *
from pandas import read_csv
from osgeo import gdal
import os
from pyrsgis.convert import rastertocsv
from qgis.core import *
from qgis.core import QgsVectorFileWriter, QgsWkbTypes
from qgis.core import QgsProject

import osgeo.ogr, osgeo.osr
from osgeo import ogr
from mpl_toolkits.mplot3d.axes3d import *
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import csv
import numpy as np
from matplotlib.mlab import griddata
import scipy as sp
import scipy.interpolate
import plotly.plotly as py
import plotly.graph_objs as go
from mpl_toolkits.mplot3d import Axes3D
import pylab
import visvis

class RasterTool:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RasterTool_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.dlg = RasterToolDialog ()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&RasterTool')
        self.toolbar = self.iface.addToolBar ( u'RasterTool' )
        self.toolbar.setObjectName ( u'RasterTool' )

        self.dlg.pushButton_4.clicked.connect(self.rtocsv2)
        self.dlg.pushButton_5.clicked.connect(self.toshapefile)
        self.dlg.pushButton_4.clicked.connect(self.formatcsv)
        self.dlg.checkBox_scatter.clicked.connect(self.graph_1)
        self.dlg.checkBox_gsplot.clicked.connect(self.graph_2)
        self.dlg.button_box.clicked.connect(self.Pb_cancel)

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RasterTool', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/RasterTool/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


        self.dlg.lineEdit_2.clear ()
        self.o1folder ();
        self.dlg.pushButton_2.clicked.connect ( self.o1outputloc )

        self.newcsvfl ();
        self.dlg.pushButton_2.clicked.connect ( self.createcsv )
        self.newcsvfl2 ();
        self.dlg.pushButton_2.clicked.connect ( self.createcsv2 )

        self.dlg.lineEdit_3.clear ()
        self.initFolder ();
        self.dlg.pushButton_3.clicked.connect ( self.opentif )



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&RasterTool'),
                action)
            self.iface.removeToolBarIcon(action)
            del self.toolbar



    def o1folder(self):
        o1csv_path_project = QgsProject.instance ().fileName ()
        o1csv_path_project = o1csv_path_project[:o1csv_path_project.rfind ( "/" ):]

        self.o1csvfolderName = o1csv_path_project

    def o1outputloc(self):
        outcsvfolder = QFileDialog.getExistingDirectory ( self.dlg, caption="Select Folder for output CSV data" )
        self.outcsvfolderName = outcsvfolder + "/"

    def newcsvfl(self):
        newcsv_path_project = QgsProject.instance ().fileName ()
        newcsv_path_project = newcsv_path_project[:newcsv_path_project.rfind ( "/" ):]

        self.newcsvName = newcsv_path_project

    def createcsv(self):
        self.dlg.lineEdit_2.setText ( self.outcsvfolderName )
        folderx01 = self.outcsvfolderName + (
                    'output_%s' % (time.strftime ( "%Y%m%d_" )) + time.strftime ( "%H%M%S" ) + ".csv")
        with open ( os.path.join ( folderx01 ), 'w' ):
            self.newcsvName = folderx01
        self.dlg.lineEdit_2.setText ( self.newcsvName )


    def initFolder(self):
        path_project = QgsProject.instance ().fileName ()
        path_project = path_project[:path_project.rfind ( "/" ):]

        self.folderName = path_project

        self.dlg.lineEdit_3.setText ( self.folderName );

    def opentif(self):
        infile = str ( QFileDialog.getOpenFileName ( caption="Input Raster file",
                                                     filter="GeoTiff(*.tif)" )[0] )
        if infile != "":
            self.folderName = infile
        self.dlg.lineEdit_3.setText ( self.folderName );

    def rtocsv2(self):
        self.dlg.lineEdit_3.setText ( self.folderName )
        la = self.folderName
        self.dlg.lineEdit_2.setText ( self.newcsvName)
        boo = self.newcsvName
        layer = QgsRasterLayer ( la, 'raster' )
        provider = layer.dataProvider ()

        my_path = provider.dataSourceUri ()

        dataset = gdal.Open ( my_path )
        band = dataset.GetRasterBand ( 1 )

        data = band.ReadAsArray ( 0, 0, band.XSize, band.YSize )

        extent = layer.extent ()

        xmin = extent.xMinimum ()
        ymax = extent.yMaximum ()

        rows = layer.height ()
        columns = layer.width ()

        xsize = layer.rasterUnitsPerPixelX ()
        ysize = layer.rasterUnitsPerPixelY ()

        k = 1

        xinit = xmin + xsize / 2
        yinit = ymax - ysize / 2

        with open ( boo, 'a' ) as file:
            sq ="%s%s%s%s%s%s%s"%('id',',','Longitude(X)',',','Latitude(Y)',',','Raster value')
            file.write (sq)
            file.write ( '\n' )

        for i in range ( rows ):
            for j in range ( columns ):
                x = xinit + j * xsize
                y = yinit
                ky =( str ( k ) + "," + str ( x ) + "," + str ( y ) + "," + str ( data[i][j] ) + "\n" )
                with open ( boo, 'a' ) as file:
                    file.write ( ky )
                k += 1
            xinit = xmin + xsize / 2
            yinit -= ysize

    def newcsvfl2(self):
        newcsv2_path_project = QgsProject.instance ().fileName ()
        newcsv2_path_project = newcsv2_path_project[:newcsv2_path_project.rfind ( "/" ):]

        self.newcsv2Name = newcsv2_path_project

    def createcsv2(self):
        self.dlg.lineEdit_2.setText ( self.outcsvfolderName )
        folderx03 = self.outcsvfolderName + (
                    'RasterTool_%s' % (time.strftime ( "%Y%m%d_" )) + time.strftime ( "%H%M%S" ) + ".csv")
        with open ( os.path.join ( folderx03 ), 'w' ):
            self.newcsv2Name = folderx03

    def formatcsv(self):
        self.dlg.lineEdit_2.setText ( self.newcsvName )
        adk= self.newcsvName
        hu = self.newcsv2Name
        with open ( adk, 'r' ) as fin, open ( hu, 'w', newline='' ) as fout:

            # define reader and writer objects
            reader = csv.reader ( fin, skipinitialspace=True )
            writer = csv.writer ( fout, delimiter=',' )

            # write headers
            writer.writerow ( next ( reader ) )

            # iterate and write rows based on condition
            for i in reader:
                if float ( i[-1] )>-10000:
                    writer.writerow ( i )

        os.remove(adk)


    def toshapefile(self):
        hy = self.newcsv2Name
        kip = "%s%s%s" % ("file:///",hy,"?delimiter=,&crs=epsg:4326&xField=Longitude(X)&yField=Latitude(Y)")
        uri = kip
        vlayer = QgsVectorLayer(uri, "point", 'delimitedtext')
        QgsProject.instance().addMapLayer(vlayer)

    def graph_1(self):
        yo = self.newcsv2Name
        x = []
        y = []
        z = []

        with open ( yo, "r" ) as csv_file:
            csv_reader = csv.reader ( csv_file, delimiter=',' )
            next ( csv_reader )
            for row in csv_reader:
                x.append ( float ( row[2] ) )
                y.append ( float( row[1] ) )
                z.append (float (row[3] ) )
            fig = plt.figure ()
            ax = Axes3D ( fig )
            ax.scatter3D ( x, y, z, c=z, cmap=plt.cm.jet )
            ax.set_xlabel('Latitude(Y)')
            ax.set_ylabel ( 'Longitude(X)' )
            ax.set_zlabel('Pixel Value')
            ax.set_title('3D Scatter Plot')
            plt.show ()

    def graph_2(self):
        yw = self.newcsv2Name
        x = []
        y = []
        z = []

        with open(yw, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                x.append(float(row[2]))
                y.append(float(row[1]))
                z.append(float(row[3]))
        spline = sp.interpolate.Rbf(x, y, z, function='thin-plate')
        xi = np.linspace(min(x), max(x))
        yi = np.linspace(min(y), max(y))
        X, Y = np.meshgrid(xi, yi)
        # interpolation
        Z = spline(X, Y)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=1, antialiased=True)
        ax.set_xlabel ( 'Latitude(Y)' )
        ax.set_ylabel ( 'Longitude(X)' )
        ax.set_zlabel ( 'Pixel Value' )
        plt.show()


    def Pb_cancel(self):
        self.dlg.close ()

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass