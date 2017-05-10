#coding:utf-8
from osgeo import gdal

class cRaster:
    def __init__(self):
        pass
    def __del__(self):
        pass

    def read(self,filename):
        #filename = "D:\\PYTHON\\fdem.tif"
        dataset=gdal.Open(filename) #打开文件
        
        im_width = dataset.RasterXSize #栅格矩阵的列数
        im_height = dataset.RasterYSize #栅格矩阵的行数
        self.im_bands = dataset.RasterCount #波段数
        
        im_geotrans = dataset.GetGeoTransform()
        #仿射矩阵，左上角像素的大地坐标和像素分辨率
        im_proj = dataset.GetProjection() #地图投影信息，字符串表示
        im_data = dataset.ReadAsArray(0,0,im_width,im_height)
        del dataset
        
        
        
        #显示栅格数据
        #print '1',"width,height,bands:",im_width,im_height,self.im_bands
        #print '2',im_data[10:15,20:25] #查看波段0,10~14 行和20~25列的数据
        #new_data = np.arange(total,dtype=im_data.dtype).reshape(tuple(size))
        #new_data[0] = im_data
        print '3',im_geotrans
        print 'pro:\n',im_proj,'\ntype pro',type(im_proj)
        #print "4",im_data.shape,im_data.dtype
        return im_data,im_geotrans,im_proj
        #["WGS 84 / UTM zone 50N",GEOGCS["WGS 84"
        #,DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,
        #AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],
        #PRIMEM["Greenwich",0],UNIT["degree",
        #(409294.88697, 27.37648, 0.0, 4423871.08338, 0.0, -27.37648)
        
        
    def write(self,*var):
        ImData,ImGeoTrans,ImProj,filename = var
        print '收到',__name__
        #判断栅格数据的数据类型
        if 'int8' in ImData.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in ImData.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32
            
        #判读数组维数
        if len(ImData.shape) == 3:
            ImBands, ImHeight, ImWidth = ImData.shape
        else:
            ImBands, (ImHeight, ImWidth) = 1,ImData.shape
        
        #创建文件
        driver = gdal.GetDriverByName("GTiff")
        dataset = driver.Create(filename, ImWidth, ImHeight, ImBands, datatype)
        dataset.SetGeoTransform(ImGeoTrans) #写入仿射变换参数
        dataset.SetProjection(ImProj) #写入投影
        if ImBands == 1:
            dataset.GetRasterBand(1).WriteArray(ImData) #写入数组数据
        else:
            for i in range(ImBands):
                dataset.GetRasterBand(i+1).WriteArray(ImData[i])
        del dataset
        
if __name__ == "__main__":
    filename = "D:\\PYTHON\\fdem.tif"
    savefile = "D:\\PYTHON\\shp\\station_shp.tif"
    a=cRaster()
    b=a.Iread(filename)
    print type(b[0]),type(b)
    print len(b)
    c=[b[0]]+list(b[1:])+[savefile]
    print type(c)
    print b[1:],'\n',c[1:]
    a.Iwrite(*c)

    
    