#coding:utf-8

import sys
from PyQt4 import QtGui,QtCore
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from UI.Shp import cShp
import ogr
from matplotlib.collections import PatchCollection
#from lib2to3.fixer_util import String
from matplotlib.patches import Polygon
from UI.Img import cRaster

import time############
from UI.plotDem import plotD
from PyQt4.Qt import QStringList

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        self.initCanvas()
        self.ax_index=0
        self.message=""
     
    def initUI(self):
        #action
        openActionV = QtGui.QAction(QtGui.QIcon('pic\\V.jpg'), 'Open Vector File', self)
        openActionV.setShortcut('Ctrl+V')
        openActionV.setStatusTip('Open Arcinfo Shape')
        openActionV.triggered.connect(self.on_Shp)
        
        openActionI = QtGui.QAction(QtGui.QIcon('pic\\R.jpg'), 'Open Raster File', self)
        openActionI.setShortcut('Ctrl+r')
        openActionI.setStatusTip('Open Arcinfo Shape')
        openActionI.triggered.connect(self.on_Img)
        
        saveAction = QtGui.QAction(QtGui.QIcon('pic\\s.jpg'),'&save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Plot')
        saveAction.triggered.connect(self.on_savedialog)
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        contourAction = QtGui.QAction(QtGui.QIcon('pic\\c.jpg'),'&contour', self)
        contourAction.setShortcut('Ctrl+c')
        contourAction.setStatusTip('contour')
        contourAction.triggered.connect(self.on_contourdialog)
        
        aboutAction = QtGui.QAction('&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.on_about)
        infotAction = QtGui.QAction(QtGui.QIcon('pic\\I.jpg'),'&Info', self)
        infotAction.setStatusTip('Information')
        infotAction.triggered.connect(self.on_info)
        #menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openActionV)
        fileMenu.addAction(openActionI)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        tackleMenu = menubar.addMenu('&Fun')
        tackleMenu.addAction(contourAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)
        
        #toolbar
        toolbar = self.addToolBar('Standard')
        toolbar.addAction(openActionV)
        toolbar.addAction(openActionI)
        toolbar.addAction(saveAction)
        toolbar.addAction(contourAction)
        toolbar.addAction(infotAction)
        #status
        self.statusBar().showMessage('Ready')
        #
        self.setGeometry(300, 100, 500, 400)
        self.setWindowTitle("python string六人")
        self.show()

    
    
    
    def initCanvas(self):
        self.fig = plt.figure(figsize=(6,3), dpi=150)  
        self.qwidget = QtGui.QWidget()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.qwidget)
        
        #hbox wight
        self.combobox=QtGui.QComboBox()
        a=["aaa"]+["bbbb"]+["ccc"]
        for i in range(3):
            self.combobox.addItem(QtCore.QString(a[i]))
        self.combobox.currentIndexChanged.connect(self.on_combo)
        #hbox 
        hbox =QtGui.QHBoxLayout()
        hbox.addWidget(self.combobox)
        '''
        self.grid_cb = QtGui.QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.grid_cb.stateChanged.connect(self.on_Shp)
        # Layout with box sizers
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.grid_cb)
        # hbox.setAlignment(self.grid_cb, QtCore.Qt.AlignVCenter)
        '''
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)
        self.qwidget.setLayout(vbox)
        self.setCentralWidget(self.qwidget)
        #self.draw()  wait for a while  
    def on_Shp(self):#shp图标的对应操作
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'd:\\python',"*.shp")
        b=filename.__str__()
        fname=b.encode("utf-8")
        shp_driver = cShp()
        #fieldlist,reclist,geomlist,spatialref,geomtype = shp_driver.Sread(fname)
        self.Info = shp_driver.read(fname)
        self.dataType=0#用数字表示文件格式，0为矢量，栅格为1；存储的时候有用
        spatialref=self.Info[3]
        geomlist=self.Info[2]
        self.message=spatialref.ExportToWkt()
        self.new_axes()
        cm = matplotlib.cm.get_cmap('Dark2')
        cccol = cm(1.*np.arange(len(geomlist))/len(geomlist))
        minx,maxx,miny,maxy = 0,0,0,0
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
        
        
        x=time.time()-1460860000
        print 'time',x
        self.qwidget.setStatusTip("hehe"+str(time.time()-1460860000))
        
        
    def on_Img(self):#img图标的对应操作
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'd:\\python',"*.tif")
        b=filename.__str__()
        fname=b.encode("utf-8")
        test = cRaster()
        self.Info = test.read(fname)
        self.dataType=1#用数字表示文件格式，0为矢量，栅格为1,如果画图操作存为3；存储的时候有用
        self.message=self.Info[2]
        data=self.Info[0]
        
        self.new_axes()
        self.axes.imshow(data)
        self.canvas.draw() 
    
    def on_contourdialog(self):
        if( self.dataType!=1):
            QtGui.QMessageBox.about(self, "Attention","This method set for raster!")
            return
        self.new_axes()
        plota=plotD()
        self.axes = plota.figureD(self.Info)
        print "self",self.axes
        
        self.canvas.draw()  
    def on_savedialog(self):
        if(self.dataType==0):
            path = unicode(QtGui.QFileDialog.getSaveFileName(self, 'Save file', 'D:\\test', "shp (*.shp)|*.shp"))
            if path:
                driver = cShp()
        if(self.dataType==1):
            path = unicode(QtGui.QFileDialog.getSaveFileName(self, 'Save file', 'D:\\test', "tif (*.tif)|*.tif"))
            if path:
                driver = cRaster()
        path=path.encode("utf-8")
        arg=list(self.Info)+[path]
        driver.write(*arg)    
        
        #if path:
            #self.fig.savefig(path)
            #self.statusBar().showMessage('Saved to %s' % path, 2000)
    def on_combo(self):
        mes=self.combobox.currentText()
        print mes
    
    def new_axes(self):#清空图，以画新的图
        if(self.ax_index):
            self.axes.remove()
            self.ax_index=0
        self.axes = self.fig.add_axes([0, 0, 1, 1])#.add_subplot(111) 
        self.ax_index=1        
        self.axes.set_axis_off()
    def on_info(self):#显示图片信息
        QtGui.QMessageBox.about(self, "Info", self.message)
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
    def cal_patch(self,geom):
        ptchs = []
        for i in range(geom.GetGeometryCount()):
            ring = geom.GetGeometryRef(i)
            pnts = [[ring.GetX(j),ring.GetY(j)] for j in range(ring.GetPointCount())]
            if len(pnts) == 0:
                continue
            ptchs.append(Polygon(pnts))
        return ptchs
    
#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        