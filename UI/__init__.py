#coding:utf-8

import sys
from PyQt4 import QtGui
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from UI.Shp import cShp
import ogr
from matplotlib.collections import PatchCollection

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        self.initCanvas()
    def initUI(self):
        #action
        openAction = QtGui.QAction(QtGui.QIcon('\\pic\\11.jpg'), 'Open Vector File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Arcinfo Shape')
        openAction.triggered.connect(self.on_Shp)
        saveAction = QtGui.QAction('&remove', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Plot')
        saveAction.triggered.connect(self.on_savedialog)
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        aboutAction = QtGui.QAction('&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.on_about)
        #menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)
        #toolbar
        toolbar = self.addToolBar('Standard')
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        #status
        self.statusBar().showMessage('Ready')
        #
        self.setGeometry(300, 100, 500, 400)
        self.setWindowTitle('pythonÁùÈË×é')
        self.show()
    def initCanvas(self):
        self.fig = plt.figure(figsize=(6,3), dpi=150)
        self.axes = self.fig.add_subplot(111)       
        qwidget = QtGui.QWidget()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(qwidget)
      
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.canvas)
        qwidget.setLayout(vbox)
        self.setCentralWidget(qwidget)
        #self.draw()  wait for a while  
    def on_Shp(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'd:\\',"*.shp")
        shp_driver = cShp()
        fieldlist,reclist,geomlist,spatialref,geomtype = shp_driver.Sread(filename)
        cm = matplotlib.cm.get_cmap('Dark2')
        cccol = cm(1.*np.arange(len(geomlist))/len(geomlist))
        minx,maxx,miny,maxy = 180,-180,90,-90
        for k in range(len(geomlist)):
            wkt = geomlist[k]
            geom =ogr.CreateGeometryFromWkt(wkt)
            minx_,maxx_,miny_,maxy_= geom.GetEnvelope()
            if minx_<minx:
                minx = minx_
            if miny_<miny:
                miny = miny_
            if maxx_>maxx:
                maxx = maxx_
            if maxy_>maxy:
                maxy = maxy_

            if geom.GetGeometryType() in [1,2,3]:
                ptchs = self.cal_patch(geom)
            elif geom.GetGeometryType() in [4,5,6]:
                ptchs = []
                for i in range(geom.GetGeometryCount()):
                    g = geom.GetGeometryRef(i)
                    p = self.cal_patch(g)
                    ptchs += p
            fc=cccol[k,:]
            self.axes.add_collection(PatchCollection(ptchs,edgecolor='k', facecolor=fc, linewidths=.1))
        
        self.axes.set_xlim(minx,maxx)
        self.axes.set_ylim(miny,maxy)
        self.axes.set_aspect(1.0)
        self.canvas.draw()
            
    def on_savedialog(self):
        
        path = unicode(QtGui.QFileDialog.getSaveFileName(self, 'Save file', 'C:\\', "PNG (*.png)|*.png"))
        if path:
            self.fig.savefig(path)
            self.statusBar().showMessage('Saved to %s' % path, 2000)
            
        
    def on_about(self):
        msg = """ A demo of using PyQt with matplotlib:
        * menubar
        * toolbar
        * statusbar
        * QFileDialog
        * QMessageBox
        * QWidget
        * FigureCanvas + Figure (matplotlib)
        """
        QtGui.QMessageBox.about(self, "About", msg)
    
    
#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        