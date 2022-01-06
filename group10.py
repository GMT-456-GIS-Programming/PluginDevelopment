# -*- coding: utf-8 -*-
"""
/***************************************************************************
 group10
                                 A QGIS plugin
 group10
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-12-24
        git sha              : $Format:%H$
        copyright            : (C) 2021 by group10
        email                : emreabaogluu@gmail.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.core import *
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .group10_dialog import group10Dialog
import os.path
from osgeo import ogr


class group10:
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
            'group10_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&group10')

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
        return QCoreApplication.translate('group10', message)

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
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/group10/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&group10'),
                action)
            self.iface.removeToolBarIcon(action)
    
    def error_msj(self,uyari):
        QMessageBox.warning(self.dlg.show(), self.tr("HKMO Warning"), self.tr(str(uyari)),QMessageBox.Ok)
    
    def shapefile_sec(self):
        try: 
            self.shapefilePath,x = QFileDialog.getOpenFileName(self.dlg, "Shapefile dosyasını seçin", "" , "ESRI Shapefiles(*.shp *.SHP);; GeoJSON (*.GEOJSON *.geojson);; Geography Markup Language(*.GML)")
            # x dosyanın uzantısını veriyor ( ESRI Shapefiles(*.shp *.SHP))
            
            
            self.shp = ogr.Open(self.shapefilePath)
            self.layer = self.shp.GetLayer(0)
            self.name = self.layer.GetName()
            self.layerDef = self.layer.GetLayerDefn()
            self.kontrol = False
        
    

            if self.layerDef.GetGeomType() == ogr.wkbLineString:
                self.vlayer = QgsVectorLayer(self.shapefilePath, self.name, "ogr")
                self.kontrol = True
                self.dlg.lineEdit.setText(self.shapefilePath)
            else:
                self.error_msj("Seçtiğiniz katman geometrisi sadece çizgi geometrisi olabilir !")
                self.dlg.lineEdit.setText("")
                return False
        except:
            return False
    
    
    
    def run(self):
        """Run method that performs all the real work"""
        if self.first_start == True:
            self.first_start = False
            self.dlg = group10Dialog()
            self.dlg.toolButton.clicked.connect(self.shapefile_sec)
            self.dlg.runButton.clicked.connect(self.run)
            

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            if self.kontrol == True:
                totalMin=9999999999
                processed=0

                if not self.vlayer.isValid():
                    print("[ERR1] Layer is not a valid.")                    
                else:
                    QgsProject.instance().addMapLayer(self.vlayer)
                    oznitelikler = self.vlayer.fields().names()
                    print(oznitelikler)                    
                    eklenecekOznitelikler = ["minMesafe","gercekMes"]
                    self.vlayer.startEditing()
                    dp = self.vlayer.dataProvider()

                    for isim in eklenecekOznitelikler:
                        if not isim in oznitelikler:
                            dp.addAttributes([QgsField(isim,QVariant.Double)])

                    self.vlayer.updateFields()

                    lines = [feat for feat in self.vlayer.getFeatures()]

                    if len(lines) > 0:
                        sCrs = self.vlayer.sourceCrs()
                        print("crs: ",sCrs)
                        d = QgsDistanceArea()
                        d.setEllipsoid(sCrs.ellipsoidAcronym())

                        for cizgi in lines:
                            geom = cizgi.geometry()
                            gercekMesafe = d.measureLine(geom.asMultiPolyline()[0])
                            processed=processed+1


                            print(gercekMesafe)

                            baslangicNoktasi = geom.constGet()[0][0]
                            bitisNoktasi = geom.constGet()[0][-1]

                            print("baslangic noktasi: ",baslangicNoktasi)
                            print("bitis noktasi: ",bitisNoktasi)

                            minCizgi = QgsFeature()
                            minCizgi.setGeometry(QgsGeometry.fromPolyline([baslangicNoktasi,bitisNoktasi]))

                            minMesafe = d.measureLine(minCizgi.geometry().asPolyline())

                            print("Minimum Distance : ", minMesafe)
                            totalMin=min(totalMin,minMesafe)

                            cizgi["minMesafe"] = minMesafe
                            cizgi["gercekMes"] = gercekMesafe
                            self.vlayer.updateFeature(cizgi)


                        

                        self.vlayer.updateFields()
                        self.vlayer.commitChanges()
                        self.dlg.minLabel.setText("Min. Length: "+str(totalMin))
                        self.dlg.procLineSegment.setText("Processed Line Series:"+str(processed))
                    else:
                        print("[ERR2] No line segments exist in current layer.");
    
