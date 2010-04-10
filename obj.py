from geom import *
from app import *
from decimal import *
import math
from random import *
from string import *
      
"""
 Set of classes for building a car.
"""
  
class Rin(GLObject):
    def __init__(self, r):  #n is number of screws
        GLObject.__init__(self)
        self.r = r
        self.disk = Disk(0.1, r)
        self.axis = CartesianAxis(self)
        self.bBox = BBox(self)
        self.setBoundingBox(2. * self.r, 2. * self.r, 2. * self.r)
        self.child = [self.disk]
    def drawGL(self):
        GLObject.drawGL(self)
        glPushMatrix()
        self.transform.apply()
        self.disk.drawGL()
        glPopMatrix()

class Tire(GLObject):
    def __init__(self, r):
        GLObject.__init__(self)
        self.r = r
        self.torus = Torus(0.22 * r, r)
        self.axis = CartesianAxis(self)
        self.bBox = BBox(self)
        self.setBoundingBox(2. * self.r, 2. * self.r, 2. * self.r)
        self.child = [self.torus]
    def drawGL(self):
        GLObject.drawGL(self)
        glPushMatrix()
        self.transform.apply()
        self.torus.drawGL()
        glPopMatrix()
     
class Screw(GLObject):
    def __init__(self, r, sides):
        GLObject.__init__(self)
        self.r = r
        self.n = sides
        self.cyl = Cylinder(self.r / 2, 0.1)
        self.cyl.setSlices(self.n)
        self.cyl.setStacks(self.n)
        self.disk = Disk(0.0, self.r)
        self.disk.setSlices(self.n)
        self.disk.setStacks(self.n)
        self.axis = CartesianAxis(self)
        self.bBox = BBox(self)
        self.setBoundingBox(2. * self.r, 2. * self.r, 2. * self.r)
        self.child = [self.cyl, self.disk]
    def drawGL(self):
        GLObject.drawGL(self)
        glPushMatrix()
        self.transform.apply()
        self.cyl.drawGL()
        glPushMatrix()
        glTranslatef(0., 0., 0.05)
        self.disk.drawGL()
        glPopMatrix()
        glPopMatrix()

class Wheel(GLObject):
    def __init__(self, r, n):   # n is number of screws
        GLObject.__init__(self)
        self.r = r
        self.n = n
        self.tire = Tire(r)
        self.rin = Rin(0.75 * r)
        self.screw = Screw(0.04, 5) # 5 sides
        self.axis = CartesianAxis(self)
        self.bBox = BBox(self)
        self.setBoundingBox(2. * self.r, 2. * self.r, 2. * self.r)
        self.child = [self.tire, self.rin, self.screw]
    def drawGL(self):
        GLObject.drawGL(self)
        glPushMatrix()
        self.transform.apply()
        self.tire.drawGL()
        self.rin.drawGL()
        screwAng = 360. / self.n
        for i in range(self.n):
            glPushMatrix()
            glRotatef(-screwAng *i, 0.0, 0.0, 1.0)
            glTranslatef(0.2 * math.sin(self.transform.tethaZ), 0.2 * math.cos(self.transform.tethaZ), 0.)
            self.screw.drawGL()
            glPopMatrix()
        glPopMatrix()
                
class Car(GLObject):
    def __init__(self, a, b, c, d, e, f, dir, ini, end, m, n):
        GLObject.__init__(self)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.m = m
        self.n = n        
        self.ini = ini
        self.end = end
        self.dir = dir
        self.currentDir = dir
        self.corner = Corner(ini.getRow(), ini.getCol())
        self.back = Box(a, b, c)
        self.doors = Box(d, b, c)
        self.capo = Box(d, f, c)
        self.front = Box(e, b, c)
        self.wheel = Wheel(.4, 5)
        self.axis = CartesianAxis(self)
        self.bBox = BBox(self)
        self.setBoundingBox(a, b, c)
        self.child = [self.back, self.front, self.doors, self.capo, self.wheel]                
        self.walkedPathX = 0
        self.walkedPathZ = 0
        
        self.pathObj = Path(dir, self.ini, self.end, self.m, self.n)
        self.path = self.pathObj.getPath()  
        self.pathLength = len(self.path)              

    #METODO QUE DEFINE EL MOVIMIENTO DE LOS AUTOS QUE INICIAN EN 0.0 O 180.0 GRADOS
    def horizontalDrive(self):
        #LOS AUTOS QUE INICAN EN LOS BORDES, GIRAN PARA PODER MOVERSE ADECUADAMENTE
        if len(self.path) == self.pathLength:
            if self.dir == 0.0:
                if self.path[0].getRow() > self.ini.getRow():                    
                    if self.transform.tethaY > -90.0:
                        self.transform.deltaTethaY = -2.0
                    else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = 0.05                
                        self.pathLength = -1                        
                elif self.path[0].getRow() < self.ini.getRow():
                    if self.transform.tethaY < 90.0:
                        self.transform.deltaTethaY = 2.0
                    else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = -0.05                
                        self.pathLength = -1 
                else:
                    self.transform.deltaX = 0.05
                    self.pathLength = -1
            elif self.dir == 180.0:                
                if self.path[0].getRow() < self.ini.getRow():
                    if self.transform.tethaY > -90.0:
                        self.transform.deltaTethaY = -2.0
                    else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = 0.05                
                        self.pathLength = -1 
                elif self.path[0].getRow() > self.ini.getRow():
                    if self.transform.tethaY < 90.0:
                        self.transform.deltaTethaY = 2.0
                    else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = -0.05                
                        self.pathLength = -1 
                else:
                    self.transform.deltaX = 0.05
                    self.pathLength = -1            
        elif len(self.path) > 0:                                            
            nextRow = self.path[0].getRow()
            nextCol = self.path[0].getCol()            
            
            if len(self.path) > 1:
                curveMarkRow = self.path[1].getRow() - nextRow;
                curveMarkCol = self.path[1].getCol() - nextCol;
            elif len(self.path) == 1:
                self.path.pop(0)                                
                return                                                      
            
            #SE DEFINE EL DESPLAZAMIENTO EN EL EJE SOBRE EL CARRO
            if self.transform.xd > 10.0*(self.walkedPathX+1) or self.transform.zd > 10.0*(self.walkedPathZ+1):
                currentCorner = self.path[0]                   
                self.corner.setRow(currentCorner.getRow())
                self.corner.setCol(currentCorner.getCol())
                self.path.pop(0)
                
                if self.transform.xd > 10.0*(self.walkedPathX+1):
                    self.walkedPathX = self.walkedPathX + 1
                    
                if self.transform.zd > 10.0*(self.walkedPathZ+1):
                    self.walkedPathZ = self.walkedPathZ + 1                                                                
                
                #MOVIMIENTO EN X
                if curveMarkCol != 0:                    
                    self.transform.deltaZ = 0.0
                    if curveMarkCol < 0:
                        self.transform.deltaX = -0.05                                    
                    else:
                        self.transform.deltaX = 0.05
                        
                    if self.dir == 180.0:                        
                        self.transform.deltaX = -self.transform.deltaX
                
                #MOVIMIENTO EN Z        
                if curveMarkRow != 0:
                    self.transform.deltaX = 0.0
                    if curveMarkRow < 0:
                        self.transform.deltaZ = 0.05                
                    else:
                        self.transform.deltaZ = -0.05                        
                        
                    if self.dir == 0.0:                        
                        self.transform.deltaZ = -self.transform.deltaZ
    
                self.transform.deltaTethaY = 0.0
            
            #SE DEFINE EL ANGULO DE GIRO EN LAS ESQUINAS DE LOS EDIFICIOS                    
            elif self.transform.xd > 10.0*(self.walkedPathX+1)-2.3 and curveMarkRow != 0:
                directionX = self.path[0].getCol() - self.corner.getCol()
                                
                if (curveMarkRow > 0 and directionX > 0) or (curveMarkRow < 0 and directionX < 0):
                    self.transform.deltaTethaY = -2.0
                else:     
                    self.transform.deltaTethaY = 2.0                             
                    
            elif self.transform.zd > 10.0*(self.walkedPathZ+1)-2.3 and curveMarkCol != 0:
                directionZ = self.path[0].getRow() - self.corner.getRow()

                if (curveMarkCol > 0 and directionZ > 0) or (curveMarkCol < 0 and directionZ < 0):                                
                    self.transform.deltaTethaY = 2.0
                else:
                    self.transform.deltaTethaY = -2.0  
        elif self.transform.xd > 10.0*(self.walkedPathX+1) or self.transform.zd > 10.0*(self.walkedPathZ+1):
            self.transform.deltaX = 0.0
            self.transform.deltaZ = 0.0
            return                                       

    def drawGL(self):
        GLObject.drawGL(self)        
        glPushMatrix()                            
        glScalef(0.1, 0.1, 0.1)                
        glTranslatef(self.ini.getCol()*10, self.b/2+self.wheel.r, self.ini.getRow()*10)
        glRotatef(self.dir, 0.0, 1.0, 0.0)            
                
        if self.dir == 0.0 or self.dir == 180.0:
            self.horizontalDrive()
        else:            
            self.verticalDrive()
                    
        self.transform.apply()                
        self.back.drawGL()
        glPushMatrix()
        glTranslatef(self.a/2 + self.d/2, 0., 0.)
        self.doors.drawGL()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(self.a/2 + self.d/2, self.b/2 + self.f/2, 0.)
        self.capo.drawGL()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(self.a/2 + self.d + self.e/2, 0., 0.)
        self.front.drawGL()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0., -self.b / 2, self.c/2)
        self.wheel.drawGL()
        glPopMatrix()
        glPushMatrix()
        glScalef(1., 1., -1.)
        glTranslatef(0., -self.b / 2, self.c/2)
        self.wheel.drawGL()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(self.a/2 + self.d + self.e, -self.b / 2, self.c/2)
        self.wheel.drawGL()
        glPopMatrix()
        glPushMatrix()
        glScalef(1., 1., -1.)
        glTranslatef(self.a/2 + self.d + self.e, -self.b / 2, self.c/2)
        self.wheel.drawGL()
        glPopMatrix()
        glPopMatrix()
        
    #METODO QUE DEFINE EL MOVIMIENTO DE LOS AUTOS QUE INICIAN EN 90.0 O 270.0 GRADOS        
    def verticalDrive(self):
        #LOS AUTOS QUE INICAN EN LOS BORDES, GIRAN PARA PODER MOVERSE ADECUADAMENTE
        if len(self.path) == self.pathLength:
            if self.dir == 90.0:                
                if self.path[0].getCol() < self.ini.getCol():                    
                    if self.transform.tethaY < 90:
                        self.transform.deltaTethaY = 2.0
                    else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = -0.05                
                        self.pathLength = -1
                elif self.path[0].getCol() > self.ini.getCol():
                    if self.transform.tethaY > -90:
                        self.transform.deltaTethaY = -2.0
                    else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = 0.05                
                        self.pathLength = -1
                else:
                    self.transform.deltaX = 0.05
                    self.pathLength = -1   
            elif self.dir == 270.0:
                 if self.path[0].getCol() < self.ini.getCol():
                     if self.transform.tethaY > -90:
                        self.transform.deltaTethaY = -2.0
                     else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = 0.05                
                        self.pathLength = -1
                 elif self.path[0].getCol() > self.ini.getCol():
                     if self.transform.tethaY < 90:
                        self.transform.deltaTethaY = 2.0
                     else:
                        self.transform.deltaTethaY = 0.0
                        self.transform.deltaZ = -0.05                
                        self.pathLength = -1
                 else:
                     self.transform.deltaX = 0.05
                     self.pathLength = -1 
        elif len(self.path) > 0:                                 
            nextRow = self.path[0].getRow()
            nextCol = self.path[0].getCol()            
            
            if len(self.path) > 1:
                curveMarkRow = self.path[1].getRow() - nextRow;
                curveMarkCol = self.path[1].getCol() - nextCol;
            elif len(self.path) == 1:
                self.path.pop(0)                                
                return                                                            
            
            #SE DEFINE EL DESPLAZAMIENTO EN EL EJE SOBRE EL CARRO
            if self.transform.xd > 10.0*(self.walkedPathX+1) or self.transform.zd > 10.0*(self.walkedPathZ+1):
                currentCorner = self.path[0]                   
                self.corner.setRow(currentCorner.getRow())
                self.corner.setCol(currentCorner.getCol())
                self.path.pop(0)
                
                if self.transform.xd > 10.0*(self.walkedPathX+1):
                    self.walkedPathX = self.walkedPathX + 1
                    
                if self.transform.zd > 10.0*(self.walkedPathZ+1):
                    self.walkedPathZ = self.walkedPathZ + 1                                                                
                
                #MOVIMIENTO EN X
                if curveMarkCol != 0:                    
                    self.transform.deltaX = 0.0
                    if curveMarkCol < 0:
                        self.transform.deltaZ = -0.05                                    
                    else:
                        self.transform.deltaZ = 0.05   
                        
                    if self.dir == 270.0:                        
                        self.transform.deltaZ = -self.transform.deltaZ                                                                                
                
                #MOVIMIENTO EN Z     
                if curveMarkRow != 0:
                    self.transform.deltaZ = 0.0
                    if curveMarkRow < 0:
                        self.transform.deltaX = 0.05                
                    else:
                        self.transform.deltaX = -0.05
                        
                    if self.dir == 270.0:                        
                        self.transform.deltaX = -self.transform.deltaX                                                                    
    
                self.transform.deltaTethaY = 0.0
                                
            elif self.transform.zd > 10.0*(self.walkedPathZ+1)-2.3 and curveMarkRow != 0:
                directionZ = self.path[0].getCol() - self.corner.getCol()
                                
                if (curveMarkRow > 0 and directionZ > 0) or (curveMarkRow < 0 and directionZ < 0):
                    self.transform.deltaTethaY = -2.0
                else:     
                    self.transform.deltaTethaY = 2.0                             
                    
            elif self.transform.xd > 10.0*(self.walkedPathX+1)-2.3 and curveMarkCol != 0:
                directionX = self.path[0].getRow() - self.corner.getRow()

                if (curveMarkCol > 0 and directionX > 0) or (curveMarkCol < 0 and directionX < 0):                                
                    self.transform.deltaTethaY = 2.0
                else:
                    self.transform.deltaTethaY = -2.0                   
        elif self.transform.xd > 10.0*(self.walkedPathX+1) or self.transform.zd > 10.0*(self.walkedPathZ+1):
            self.transform.deltaX = 0.0
            self.transform.deltaZ = 0.0
            return
         
#ESTRUCTURA DE DATOS QUE ALMACENA LA FILA Y COLUMNA DE UNA ESQUINA EN LA CIUDAD
class Corner():
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def getRow(self):
        return self.row
    def getCol(self):
        return self.col
    def setRow(self, row):
        self.row = row
    def setCol(self, col):
        self.col = col

#CLASE QUE DETERMINA EL CAMINO A SEGUIR DADO UNA ESQUINA DE INICIO Y UNA DE FIN
class Path():
    def __init__(self, dir, ini, end, m, n):
        self.dir = dir
        self.ini = ini    
        self.end = end
        self.path = []
        self.m = m
        self.n = n
        
    #METODO QUE DETERMINA EL CAMINO A SEGUIR POR UN VEHICULO
    #LA FORMA DE DETERMINAR EL CAMINO, DEPENDE DE LA DIRECCION EN LA QUE INICIA EL AUTO, YA QUE SUS EJES CAMBIAN 
    def getPath(self):
        row = self.ini.getRow() 
        col = self.ini.getCol()
        if self.dir == 0.0 or self.dir == 180.0:                        
            if self.dir == 0.0:                            
                if self.ini.getRow() == self.end.getRow() and self.ini.getCol() > self.end.getCol():
                    if col+1 <= self.n:                    
                        col = col+1
                        self.path.append(Corner(row, col))
                    if row-1 >= 0:
                        row = row-1
                    elif row+1 <= self.m:
                        row = row+1
                elif self.ini.getCol() >= self.end.getCol():
                    if col+1 <= self.n:                    
                        col = col+1
                        self.path.append(Corner(row, col))
                    if self.ini.getRow() > self.end.getRow():                
                        row = row-1
                    elif self.ini.getRow() < self.end.getRow():
                        row = row+1
                elif self.ini.getCol() < self.end.getCol():
                    col = col+1                                                       
                    
            elif self.dir == 180.0:
                if self.ini.getRow() == self.end.getRow() and self.ini.getCol() < self.end.getCol():
                    if col-1 >= 0:
                        col=col-1
                        self.path.append(Corner(row, col))
                    if row-1 >=0:
                        row = row-1
                    elif row+1 <= self.m:
                        row = row+1
                elif self.ini.getCol() <= self.end.getCol():
                    if col-1 >= 0:
                        col=col-1
                        self.path.append(Corner(row, col))
                    if self.ini.getRow() > self.end.getRow():
                        row = row-1
                    elif self.ini.getRow() < self.end.getRow():
                        row = row+1
                elif self.ini.getCol() > self.end.getCol():
                    col = col-1
            
            self.path.append(Corner(row, col))
            
            currentCorner = self.path[len(self.path)-1]                        
                                                                                    
            while currentCorner.getCol() != self.end.getCol():
                if self.end.getCol() > currentCorner.getCol():
                    self.path.append(Corner(currentCorner.getRow(), currentCorner.getCol()+1))
                else:
                    self.path.append(Corner(currentCorner.getRow(), currentCorner.getCol()-1))
                
                currentCorner = self.path[len(self.path)-1]

            while currentCorner.getRow() != self.end.getRow():
                if self.end.getRow() > currentCorner.getRow():                
                    self.path.append(Corner(currentCorner.getRow()+1, currentCorner.getCol()))
                else:
                    self.path.append(Corner(currentCorner.getRow()-1, currentCorner.getCol()))
                
                currentCorner = self.path[len(self.path)-1]
        
        elif self.dir == 90.0 or self.dir == 270.0:
            if self.dir == 90.0:
                if self.ini.getCol() == self.end.getCol() and self.ini.getRow() < self.end.getRow():
                    if row-1 >= 0:
                        row = row-1
                        self.path.append(Corner(row, col))
                    if col-1 >= 0:
                        col = col-1
                    elif col+1 <= self.n:
                        col = col+1
                elif self.ini.getRow() <= self.end.getRow():
                    if row-1 >= 0:
                        row = row-1
                        self.path.append(Corner(row, col))
                    if col-1 >= 0:
                        col = col-1
                    elif col+1 <= self.n:
                        col = col+1
                elif self.ini.getRow() > self.end.getRow():
                    row = row-1
                    
            elif self.dir == 270.0:
                if self.ini.getCol() == self.end.getCol() and self.ini.getRow() > self.end.getRow():
                    if row+1 <= self.m:
                        row = row+1
                        self.path.append(Corner(row, col))
                    if col-1 >= 0:
                        col = col-1
                    elif col+1 <= self.n:
                        col = col+1
                elif self.ini.getRow() >= self.end.getRow():
                    if row+1 <= self.m:
                        row = row+1
                        self.path.append(Corner(row, col))
                    if col-1 >= 0:
                        col = col-1
                    elif col+1 <= self.n:
                        col = col+1      
                elif self.ini.getRow() < self.end.getRow():
                    row = row+1
            
            self.path.append(Corner(row, col))
            
            currentCorner = self.path[len(self.path)-1]
            
            while currentCorner.getRow() != self.end.getRow():
                if self.end.getRow() > currentCorner.getRow():                
                    self.path.append(Corner(currentCorner.getRow()+1, currentCorner.getCol()))
                else:
                    self.path.append(Corner(currentCorner.getRow()-1, currentCorner.getCol()))
                
                currentCorner = self.path[len(self.path)-1]
                
            while currentCorner.getCol() != self.end.getCol():
                if self.end.getCol() > currentCorner.getCol():
                    self.path.append(Corner(currentCorner.getRow(), currentCorner.getCol()+1))
                else:
                    self.path.append(Corner(currentCorner.getRow(), currentCorner.getCol()-1))
                
                currentCorner = self.path[len(self.path)-1]
            
        return self.path                     

#CLASE QUE REPRESENTA LAS CALLES Y EDIFICIOS DE LA CIUDAD       
class City(GLObject):
    def __init__(self, m, n, s):
        self.m = m
        self.n = n
        self.s = s
        self.square = Quad(self.s, self.s)
        self.boxes = []        
        self.child = [self.square]
        self.setTextureFile("calle.bmp")
        
        #SE CONSTRUYEN M*N EDIFICIOS
        for i in range(0,self.m):
            for j in range(0,self.n):
                buildingHeight = Decimal(self.s)*Decimal(str(randint(1,2)+random()))
                box = Box(Decimal(self.s)/Decimal("1.5"), Decimal(self.s)/Decimal("1.5"), Decimal(buildingHeight)/Decimal("2"))
                
                textureChoice = randint(1,2)
                
                #SE ELIGE UNA TEXTURA ALEATORIA PARA EL EDIFICIO
                if textureChoice == 1:
                    box.cube.front.setTextureFile("edificio.bmp")
                    box.cube.right.setTextureFile("edificio.bmp")
                    box.cube.left.setTextureFile("edificio.bmp")
                    box.cube.top.setTextureFile("edificio.bmp")
                    box.cube.bottom.setTextureFile("edificio.bmp")
                    box.cube.back.setTextureFile("edificio_techo.bmp")
                else:
                    box.cube.front.setTextureFile("casa.bmp")
                    box.cube.right.setTextureFile("casa.bmp")
                    box.cube.left.setTextureFile("casa.bmp")
                    box.cube.top.setTextureFile("casa.bmp")
                    box.cube.bottom.setTextureFile("casa.bmp")
                    box.cube.back.setTextureFile("casa_techo.bmp")
                self.boxes.append(box)
                self.child.append(box)
        
    def drawGL(self):        
        w = self.n*self.s
        d = Decimal(self.s)/Decimal("2.0")               
        glPushMatrix()                                        
        glTranslatef(d, 0.0, d)
        glRotate(90.0, 1.0, 0.0, 0.0)  
        k=0          
        for i in range(0, self.m):    
            for j in range(0, self.n):
                glPushMatrix()
                glTranslatef(self.s*j, self.s*i, 0.0)
                self.square.drawGL()
                glPushMatrix()            
                glTranslatef(0.0, 0.0, -Decimal(str(self.boxes[k].c))/Decimal("2"))
                self.boxes[k].drawGL()
                k = k+1
                glPopMatrix()
                glPopMatrix()                
        glPopMatrix()

class DemoIlum(GLObject):
    def __init__(self):
        GLObject.__init__(self)
        self.sphere1 = Sphere(0.5)        
        
        self.sphere2 = Sphere(0.5)        
        
        self.sphere3 = Sphere(0.5)
        
        self.sphere4 = Sphere(0.5)
        
        self.sphere1.transform.deltaTethaY = 2.0
        self.sphere2.transform.deltaTethaY = 2.0
        self.sphere3.transform.deltaTethaY = 2.0
        self.sphere4.transform.deltaTethaY = 2.0
        self.child = [self.sphere1, self.sphere2, self.sphere3, self.sphere4]
        
    def drawGL(self):
        GLObject.drawGL(self)
        
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -6.0)
        
        glPushMatrix()
        glTranslatef(-0.7, 0.7, 0.0)
        self.sphere1.material.setMaterialAmbient()
        self.sphere1.material.setHighShininess()        
        self.sphere1.drawGL()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.7, 0.7, 0.0) 
        self.sphere2.material.setMaterialDiffuse()
        self.sphere2.material.setLowShininess()       
        self.sphere2.drawGL()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-0.7, -0.7, 0.0)  
        self.sphere3.material.setMaterialSpecular()
        self.sphere3.material.setHighShininess()      
        self.sphere3.drawGL()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.7, -0.7, 0.0)        
        self.sphere4.drawGL()
        glPopMatrix()

"""
 Set of classes for building an airplane.
"""
    
class Plane(GLObject):
    def __init__(self, w, h, d):
        GLObject.__init__(self)
        self.w = w
        self.h = h
        self.d = d
        self.body = Cylinder(d, w)
        self.flightDeck = Sphere(d)
        self.tail = Sphere(d)
        self.fin = Box(d, 2.0*h/3.0, 0.01)
        self.finTop = Box(0.0707, 0.0707, 0.01)
        self.rightWing = Box(3.0*d/2.0, w/2.0, 0.01)
        self.leftWing = Box(3.0*d/2.0, w/2.0, 0.01)
        self.rightRearWing = Box(d/2.0, w/4.0, 0.01)
        self.leftRearWing = Box(d/2.0, w/4.0, 0.01)
        self.rearWheels = PlaneRearWheels(d/4.0, w/4.0, d)
        self.frontWheels = PlaneFrontWheels(d/5.0, d)
        self.child = [self.body, self.flightDeck, self.tail, self.fin, self.finTop, self.rightWing, self.leftWing, self.rightRearWing, self.leftRearWing, self.rearWheels, self.frontWheels]
        
    def drawGL(self):
        GLObject.drawGL(self)                                                
        
        glPushMatrix()
        glRotate(90.0, 0.0, 0.0, 1.0)
        self.body.drawGL()
        glPopMatrix()
        
        glPushMatrix()        
        glTranslatef(self.body.h/2.0, 0.0, 0.0)
        self.flightDeck.drawGL()
        glTranslatef(-self.body.h, 0.0, 0.0)
        self.tail.drawGL()
        glPopMatrix()            
        
        glPushMatrix()
        glTranslatef(-self.w/2.0, self.d*2-(self.d/1.5), 0.0)
        glRotatef(45.0, 0.0, 0.0, 1.0)
        self.fin.drawGL()         
        glRotatef(45.0, 0.0, 0.0, -1.0)
        glTranslatef(-self.finTop.a, self.finTop.b, 0.0)        
        self.finTop.drawGL()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.0, 0.0, (self.rightWing.b/2.0)-0.05)
        glRotate(90.0, 1.0, 0.0, 0.0)
        glRotate(45.0, 0.0, 0.0, 1.0)
        self.rightWing.drawGL()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.0, 0.0, -((self.leftWing.b/2.0)-0.05))
        glRotate(90.0, 1.0, 0.0, 0.0)
        glRotate(45.0, 0.0, 0.0, -1.0)        
        self.leftWing.drawGL()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-0.5, 0.0, (self.rightRearWing.b/2.0)-0.05)
        glRotate(90.0, 1.0, 0.0, 0.0)
        glRotate(45.0, 0.0, 0.0, 1.0)
        self.rightRearWing.drawGL()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-0.5, 0.0, -((self.leftRearWing.b/2.0)-0.05))
        glRotate(90.0, 1.0, 0.0, 0.0)
        glRotate(45.0, 0.0, 0.0, -1.0)        
        self.leftRearWing.drawGL()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.0, -self.h/3.0, 0.0)
        self.rearWheels.drawGL()                    
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(self.w/2.0, -self.h/3.0, 0.0)
        self.frontWheels.drawGL()
        glPopMatrix()  
    
class PlaneFrontWheels(GLObject):
    def __init__(self, r, h):
        GLObject.__init__(self)
        self.r = r
        self.h = h
        self.verticalBar = Box(0.005, h+0.01, 0.005)
        self.wheel1 = Tire(r)
        self.wheel2 = Tire(r)
        self.horizontalBar = Box(0.005, h/2.0, 0.005)
        self.child = [self.verticalBar, self.wheel1, self.wheel2, self.horizontalBar]        
        
    def drawGL(self):
        GLObject.drawGL(self)
        
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBar.b/2, 0.0)
        self.verticalBar.drawGL()
        
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBar.b/2, 0.0)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        self.horizontalBar.drawGL()
        glRotatef(90.0, -1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0.0, 0.0, -self.horizontalBar.b/2)
        self.wheel1.drawGL()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 0.0, self.horizontalBar.b/2)
        self.wheel2.drawGL()
        glPopMatrix()
        glPopMatrix()
        
        glPopMatrix()
        
        
class PlaneRearWheels(GLObject):
    def __init__(self, r, w, h):
        GLObject.__init__(self)
        self.r = r
        self.h = h
        self.w = w
        self.wheel1 = Tire(r)
        self.wheel2 = Tire(r)
        self.wheel3 = Tire(r)
        self.wheel4 = Tire(r)
        self.verticalBar = Box(0.005, h/2.0, 0.005)
        self.horizontalBar = Box(0.005, w, 0.005)
        self.verticalBarLeftWheels = Box(0.005, h/2.0, 0.005)
        self.horizontalBarLeftWheels = Box(0.005, h/2.0, 0.005)
        self.verticalBarRightWheels = Box(0.005, h/2.0, 0.005)
        self.horizontalBarRightWheels = Box(0.005, h/2.0, 0.005)
        self.child = [self.wheel1, self.wheel2, self.wheel3, self.wheel4, self.verticalBar, self.horizontalBar, self.verticalBarLeftWheels, self.verticalBarRightWheels, self.horizontalBarLeftWheels, self.horizontalBarRightWheels]
    def drawGL(self):
        GLObject.drawGL(self)
        
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBar.b/2, 0.0)
        self.verticalBar.drawGL()
        
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBar.b/2.0, 0.0)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        self.horizontalBar.drawGL()
        glRotatef(90.0, -1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBarLeftWheels.b/2, (self.horizontalBar.b/2)-self.verticalBarLeftWheels.a/2)
        self.verticalBarLeftWheels.drawGL()
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBarLeftWheels.b/2, 0.0)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        self.horizontalBarLeftWheels.drawGL()
        glRotatef(90.0, -1.0, 0.0, 0.0)
        glPushMatrix()    
        glTranslatef(0.0, 0.0, -self.horizontalBarRightWheels.b/2)
        self.wheel2.drawGL()
        glPopMatrix()
        glPushMatrix()    
        glTranslatef(0.0, 0.0, +self.horizontalBarRightWheels.b/2)
        self.wheel1.drawGL()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBarRightWheels.b/2, -((self.horizontalBar.b/2)-self.verticalBarRightWheels.a/2))
        self.verticalBarRightWheels.drawGL()
        glPushMatrix()
        glTranslatef(0.0, -self.verticalBarRightWheels.b/2, 0.0)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        self.horizontalBarRightWheels.drawGL()
        glRotatef(90.0, -1.0, 0.0, 0.0)
        glPushMatrix()    
        glTranslatef(0.0, 0.0, -self.horizontalBarRightWheels.b/2)
        self.wheel4.drawGL()
        glPopMatrix()
        glPushMatrix()    
        glTranslatef(0.0, 0.0, +self.horizontalBarRightWheels.b/2)
        self.wheel3.drawGL()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()        
        glPopMatrix()   
        
        glPopMatrix()         
        
class Airport(GLObject):
    def __init__(self):
        GLObject.__init__(self)
        self.airplane = Plane(1, 0.3, 0.1)        
        self.child = [self.airplane] 
        
    def drawGL(self):
        GLObject.drawGL(self)
        self.airplane.transform.deltaX = 1.0
        self.airplane.transform.deltaY = 1.0
        self.airplane.transform.deltaZ = 1.0
        self.airplane.transform.deltaTethaX = 1.0
        self.airplane.drawGL()
