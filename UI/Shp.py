#coding:utf-8

from osgeo import ogr
import os

class cShp:
    def read(self,filename):
        #filename = "D:\\PYTHON\\cntry98.shp"
        #filename = "D:\\PYTHON\\shp\\stations.shp"
        #print filename
        ds = ogr.Open(filename, False) #代开Shape文件（False - read only, True - read/write）
        layer = ds.GetLayer(0) #获取图层
        # layer = ds.GetLayerByName(filename[-4:])
        spatialref = layer.GetSpatialRef() #投影信息
        lydefn = layer.GetLayerDefn() #图层属性的定义信息
        geomtype = lydefn.GetGeomType() #几何对象类型（wkbPoint, wkbLineString, wkbPolygon）
        fieldlist = [] #字段列表（字段类型，OFTInteger, OFTReal, OFTString, OFTDateTime）
        
        print 'FieldCount',lydefn.GetFieldCount()
        for i in range(lydefn.GetFieldCount()):
            fddefn = lydefn.GetFieldDefn(i)
            fddict = {'name':fddefn.GetName(),'type':fddefn.GetType(),
                      'width':fddefn.GetWidth(),'decimal':fddefn.GetPrecision()}
            fieldlist += [fddict]
        geomlist, reclist = [], [] #SF数据记录– 几何对象及其对应属性
        feature = layer.GetNextFeature() #获得第一个SF
        while feature is not None:
            geom = feature.GetGeometryRef()
            geomlist += [geom.ExportToWkt()]
            rec = {}
            for fd in fieldlist:
                rec[fd['name']] = feature.GetField(fd['name'])
            reclist += [rec]
            feature = layer.GetNextFeature()
        ds.Destroy() #关闭数据源
        #显示字段列表, 几何对象及属性值
        print 'spatialref\n',spatialref.ExportToWkt()
        print 'geomtype',geomtype
        return fieldlist,reclist,geomlist,spatialref,geomtype
        
    def write(self,*var):   
        #filename = "D:\\PYTHON\\shp\\cntry98_new.shp"
        #filename = "D:\\PYTHON\\shp\\station_1.shp"
        fieldlist,reclist,geomlist,spatialref,geomtype,filename=var
        print 'len_field',len(fieldlist)
        print 'len_geo',len(geomlist[0])
        print fieldlist[0]
        print geomlist[0],'\n', reclist[0][fieldlist[0][ 'name']]
        
        driver = ogr.GetDriverByName("ESRI Shapefile")
        if os.access(filename, os.F_OK ): #如文件已存在，则删除
            driver.DeleteDataSource(filename)
            
        ds = driver.CreateDataSource(filename) #创建Shape 文件
        
        #spatialref = osr.SpatialReference( 'LOCAL_CS["arbitrary"]' )
        #spatialref = osr.SpatialReference()
        #spatialref.ImportFromEPSG(4326)
        #geomtype = ogr. wkbPolygon
        layer = ds.CreateLayer(filename [:-4], srs=spatialref, geom_type=geomtype) #创建图层
        for fd in fieldlist: #将字段列表写入图层
            field = ogr.FieldDefn(fd['name'],fd['type'])
            if fd.has_key('width'):
                field.SetWidth(fd['width'])
            if fd.has_key('decimal'):
                field.SetPrecision(fd['decimal'])
            layer.CreateField(field)
        for i in range(len(reclist)): #将SF数据记录（几何对象及其属性写入图层）
            geom = ogr.CreateGeometryFromWkt(geomlist[i])
            feat = ogr.Feature(layer.GetLayerDefn()) #创建SF
            feat.SetGeometry(geom)
            for fd in fieldlist:
                feat.SetField(fd['name'], reclist[i][fd['name']])
            layer.CreateFeature(feat) #将SF写入图层
        ds.Destroy() #关闭文件
if __name__ == "__main__":
    filename = "D:\\PYTHON\\cntry98.shp"
    savename = "D:\\PYTHON\\shp\\station_1.shp"
    a=cShp()
    b=a.Sread(filename)
    print type(b)
    arg=list(b)+[savename]
    a.Swrite(*arg)
