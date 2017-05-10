#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib.pyplot import gca


class plotD:
    def figureD(self,data):
        if type(data[0]) is not np.ndarray:
            return 0
        Z = data[0].astype(np.int16)
        Z[Z<0] =Z[Z>0].min()
        ls = LightSource(azdeg=315, altdeg=45)
        cmap =plt.cm.get_cmap('Dark2')
        ls.shade(Z, cmap)
        
        if len(Z.shape) == 3:
            ImBands, ImHeight, ImWidth = Z.shape
        else:
            ImBands, (ImHeight, ImWidth) = 1,Z.shape
        imTrans = data[1]  
        print "rans:",imTrans
        
        minX=imTrans[0]
        minY=imTrans[3]
        maxX=minX+imTrans[1]*ImWidth
        maxY=minY+imTrans[5]*ImHeight
        print minX,'\n',maxX,'\n',minY,'\n',maxY,'\n'
        
        #具体参见interPlot
        #eight, Width = 1,Z.shape
        tx=np.linspace(minX,maxX, ImWidth)
        ty=np.linspace(minY,maxY, ImHeight)
        XI,YI = np.meshgrid(tx,ty)
        
        #fig = plt.figure(figsize=(10,4))
        
        
        ax=gca()
        ax.pcolor(XI,YI,Z)#
        zone=int(np.max(Z)/3)
        level = [c for c in range(0,np.max(Z),zone)]
        print 'level',level
        CS = ax.contour(XI,YI,Z, level, hold='on', colors='k',origin='upper', aspect='equal')
        ax.clabel(CS,inline=1,fmt='%d',fontsize=10,colors = 'b' )
        print ax
        return ax


    
    
    

