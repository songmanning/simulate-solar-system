from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image as Image
import numpy

def init():
    LightPos = [0, 0, 0, 1]
    LightAmb = [0.5, 0.5, 0.5, 1.0]  # RGBA of Ambient Light 环境光
    LightDiff = [1.0, 1.0, 1.0, 1.0]  # RGBA of Diffuse Light 漫射光
    LightSpec = [1, 1, 1, 1.0]  # RGBA of Specular Light 反射光

    global MatShn
    MatShn = [128]

    #创建光源glLightfv（光源，属性，参数值）
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDiff)
    glLightfv(GL_LIGHT0, GL_SPECULAR, LightSpec)

    #渲染中使用光照
    glEnable(GL_LIGHTING)
    #使用0号光
    glEnable(GL_LIGHT0)

    glClearColor(0, 0, 0, 1)

    glMatrixMode(GL_PROJECTION) # GL_PROJECTION,对投影矩阵应用随后的矩阵操作.
    glLoadIdentity() # 重置当前指定的矩阵为单位矩阵

    gluPerspective(60,1,0.1,100) #指定了观察的视景体在世界坐标系中的具体大小
    gluLookAt(10,10,30, 0,0,0, 0,1,0) #定义一个视图矩阵，并与当前矩阵相乘
    glEnable(GL_DEPTH_TEST) #启用深度测试。根据坐标的远近自动隐藏被遮住的图形（材料）

def draw_planet_solidsphere(sun_dist, radius, angle, r,g,b):
    global MatShn
    glLoadIdentity()
    MatAmb = [r, g, b, 1]  # reflection of the material 材料的反射
    MatDif = [r, g, b, 1]
    MatSpec = [r, g, b, 1]

    # glMaterialfv()设置材质属性
    glMaterialfv(GL_FRONT, GL_AMBIENT, MatAmb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, MatDif)
    glMaterialfv(GL_FRONT, GL_SPECULAR, MatSpec)
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn)

    glColor(0.3, 0.3, 0.3)
    glutSolidTorus(0.01, sun_dist, 30, 30) #圆环
    glColor(r,g,b)
    glRotate(angle,0,0,1) #旋转
    glTranslate(sun_dist,0,0) #动当前绘图原点,（x,y,z）
    glutSolidSphere(radius,30,30) #渲染一个球体,(半径，经线，纬线)

def read_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)#图片字节数据序列
    textID = glGenTextures(1)#生成纹理的函数
    #建立一个绑定到目标纹理的有名称的纹理glBindTexture（目标，纹理名称）
    glBindTexture(GL_TEXTURE_2D, textID)
    #对齐像素字节glPixelStorei()
    #默认4字节对齐，即一行的图像数据字节数必须是4的整数倍，即读取数据时，读取4个字节用来渲染一行，之后读取4字节数据用来渲染第二行。
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    #纹理过滤函数glTexParameteri()
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    #glTexEnvf函数用来指定纹理函数，GL_DECAL是贴花
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    '''
    生成一个2D纹理
    glTexImage2D(target, level, internalformat, width, height, border, format, type, * pixels);
    target 指定目标纹理，这个值必须是GL_TEXTURE_2D。
    level 执行细节级别。0是最基本的图像级别，n表示第N级贴图细化级别。
    internalformat 指定纹理中的颜色组件
    width 指定纹理图像的宽度
    height 指定纹理图像的高度
    border 指定边框的宽度。必须为0
    format 像素数据的颜色格式, 参考internalformat
    type 指定像素数据的数据类型
    pixels 指定内存中指向图像数据的指针
    '''
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

def draw_planet_Textured(sun_dist, radius, angle, r,g,b, filename):
    global MatShn
    glLoadIdentity()
    MatAmb = [r, g, b, 1]  # reflection of the material 材料的反射
    MatDif = [r, g, b, 1]
    MatSpec = [r, g, b, 1]

    #glMaterialfv指定用于光照计算的当前材质属性
    glMaterialfv(GL_FRONT, GL_AMBIENT, MatAmb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, MatDif)
    glMaterialfv(GL_FRONT, GL_SPECULAR, MatSpec)
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn)

    glColor(0.3, 0.3, 0.3)
    glutSolidTorus(0.01, sun_dist, 30, 30) #画圆环
    glColor(r,g,b)
    glRotate(angle,0,0,1) #绕z轴旋转
    glTranslate(sun_dist,0,0) #动当前绘图原点,（x,y,z）

    # Textured thing
    tex = read_texture(filename)
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)
    gluSphere(qobj, radius, 50, 50)
    gluDeleteQuadric(qobj)
    glDisable(GL_TEXTURE_2D)

angle = [0, 0, 0, 0]

def display_solidsphere():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #清除颜色缓冲以及深度缓冲

    glMatrixMode(GL_MODELVIEW) #对模型视景矩阵堆栈应用随后的矩阵操作
    glLoadIdentity()

    #sun 太阳
    MatAmb = [1, 0, 0, 1]  # reflection of the material 材料的反射
    MatDif = [1, 0, 0, 1]
    MatSpec = [1, 0, 0, 1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, MatAmb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, MatDif)
    glMaterialfv(GL_FRONT, GL_SPECULAR, MatSpec)
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn)
    glutSolidSphere(1,30,30)

    #mercury 水星
    draw_planet_solidsphere(3.87, 0.35, angle[0], 0.7,0.3,0)
    angle[0] = (angle[0] % 360) +4.09

    #venus 金星
    draw_planet_solidsphere(7.23, 0.87, angle[1], 0.9,0.7,0.3)
    angle[1] = (angle[1] % 360) + 1.6

    # earth 地球
    draw_planet_solidsphere(10, 0.91, angle[2], 0,0,1)
    angle[2] = (angle[2] % 360) + 0.99

    # mars 火星
    draw_planet_solidsphere(15.2, 0.49, angle[3], 0.7,0.6,0.2)
    angle[3] = (angle[3] % 360) + 0.52

    glutSwapBuffers()

def display_textured():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #清除颜色缓冲以及深度缓冲

    glMatrixMode(GL_MODELVIEW) #对模型视景矩阵堆栈应用随后的矩阵操作
    glLoadIdentity()

    #sun 太阳
    MatAmb = [1, 1, 0, 1]  # reflection of the material 材料的反射
    MatDif = [1, 1, 0, 1]
    MatSpec = [1, 1, 0, 1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, MatAmb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, MatDif)
    glMaterialfv(GL_FRONT, GL_SPECULAR, MatSpec)
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn)

    # Textured thing
    tex = read_texture('sun.jpg')
    qobj = gluNewQuadric()#创建一个新的二次方程对象，并返回一个指向他的指针
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)
    gluSphere(qobj, 1, 50, 50)#画球
    gluDeleteQuadric(qobj)#//销毁二次方程对象，释放内存
    glDisable(GL_TEXTURE_2D)#关闭glEnable打开的功能

    #mercury 水星
    draw_planet_Textured(3.87, 0.35, angle[0], 1,1,1, 'mercury.png')
    angle[0] = (angle[0] % 360) + 4.09*10

    #venus 金星
    draw_planet_Textured(7.23, 0.87, angle[1], 1,1,1, 'venus.jpg')
    angle[1] = (angle[1] % 360) + 1.6*10

    # earth 地球
    draw_planet_Textured(10, 0.91, angle[2], 1,1,1, 'earth.jpg')
    angle[2] = (angle[2] % 360) + 0.99*10

    # mars 火星
    draw_planet_Textured(15.2, 0.49, angle[3], 1, 1, 1, 'mars.jpeg')
    angle[3] = (angle[3] % 360) + 0.52*10

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH) # 设置初始显示模式
glutInitWindowSize(800,800)
glutCreateWindow(b'solar system')

#纯色的光照
glutDisplayFunc(display_solidsphere) #注册一个绘图函数
glutIdleFunc(display_solidsphere) #设置全局的回调函数

#添加纹理
#glutDisplayFunc(display_textured) #注册一个绘图函数
#glutIdleFunc(display_textured) #设置全局的回调函数

init()
glutMainLoop() #进入GLUT事件处理循环
