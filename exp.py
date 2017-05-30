import sys
import auxlib
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from qtRangeSlider import QHSpinBoxRangeSlider

#Parámetros globales (¿será muy peligroso esto?)
G_cont = None  # Tipo de contenedor
G_PVI = "0"  # Rango inferior de porcentaje volumétrico
G_PVS = "0"  # Rango superior de porcentaje volumétrico
G_TI = "0"  # Rango inferior de temperatura
G_TS = "0"  # Rango superior de temperatura
G_base = 0  # Área basal
G_altura = 0  # Altura
G_techo = 0  # Área del techo

# Actualmente trabajando en: subventana de parámetros, marcado y desmarcado de botones
# Pendientes: subventanas de display, botones de flujo de datos, meter los
#             cálculos y vínculos a Arduino, estilizar

# Thread para conectar el software principal con nuestra interfaz gráfica
class Thread(QThread):
    def __init__(self):
        super().__init__()
        self.p = auxlib.Principal()

    def set_main_window(self, w):
        self.m = w

    def set_vol_label(self, label):
        self.vollabel = label

    def set_temp_label(self, label):
        self.templabel = label

    def set_flux_label(self, label):
        self.fluxlabel = label

    def run(self):
        while True:
            self.p.principal_loop()
            self.vollabel.setText(str(self.p.vol))
            self.templabel.setText(str(self.p.temp))
            self.fluxlabel.setText(str(self.p.flux))


# La ventana principal de la interfaz gráfica
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interfaz de Análisis de Datos')

        self.statusBar()
        self.menu_bar_init()

        self.Graf = Grafica()
        self.setCentralWidget(self.Graf)

        # Puedo jugar después a esto gdi
#        self.setAutoFillBackground(True)
#        a = self.palette()
#        a.setColor(self.backgroundRole(), QColor(255, 200, 170))
#        self.setPalette(a)

        self.setGeometry(300, 300, 300, 300)
        self.show()

    def menu_bar_init(self):
        exitAction = QAction(QIcon('exit24.png'), 'Salir', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Cierra la aplicación')
        exitAction.triggered.connect(self.close)
        menubar = self.menuBar()

        # definir menús
        menuArchivo = menubar.addMenu('&Archivo')
        menuArchivo.addAction(exitAction)
        menuEdicion = menubar.addMenu('&Edición')
        menuGrafico = menubar.addMenu('&Gráfico')
        menuVentana = menubar.addMenu('&Ventana')
#        par = menubar.addMenu('&Parámetros')
#        lim = menubar.addMenu('&Límites')
        ayuda = menubar.addMenu('&Ayuda')

        # definir acciones
#        volshape = QAction(QIcon('exit.png'), '&Forma del contenedor...', self)
#        volshape.setStatusTip('Permite seleccionar la forma del contenedor que se está controlando.')
#        volcalib = QAction(QIcon('exit.png'), '&Calibrar volumen...', self)
#        volcalib.setStatusTip('Permite calibrar la toma de muestras de volumen.')
#        vollim = QAction(QIcon('exit.png'), '&Establecer limites de volumen...', self)
#        vollim.setStatusTip('Establece límites para alertar en tales situaciones.')
#        templim = QAction(QIcon('exit.png'), '&Establecer limites de temperatura...', self)
#        templim.setStatusTip('Establece límites para alertar en tales situaciones.')
        acercaDe = QAction(QIcon('exit.png'), '&Acerca de...', self)
        acercaDe.setStatusTip('Créditos.')

        # asignar acciones a menús.
#        par.addAction(volshape)
#        par.addAction(volcalib)
#        lim.addAction(vollim)
#        lim.addAction(templim)
        ayuda.addAction(acercaDe)


# Marco de la ventana principal
class Grafica(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def datos_rapidos(self):
        w = QWidget()
        grid = QGridLayout()
        w.setLayout(grid)
        self.volumeLabel = self.add_labels_to_grid(grid, 0, 0, "Porcentaje volumétrico:", "%")
        self.tempLabel = self.add_labels_to_grid(grid, 0, 1, "Temperatura:", "°C")
        self.fluxLabel = self.add_labels_to_grid(grid, 0, 2, "Flujo actual:", "cm3 / s")
        return w

    def add_labels_to_grid(self, grid, row, column, text, datatypetext):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        textlabel = QLabel(text)
        textlabel.setFont(QFont("Arial", 8))
        hbox.addWidget(textlabel)
        temp = QLabel("0")
        temp.setFont(QFont("Arial", 8, QFont.Bold))
        hbox.addStretch(0)
        hbox.addWidget(temp)
        datatype = QLabel(datatypetext)
        datatype.setFont(QFont("Arial", 8, QFont.Bold))
        hbox.addStretch(0)
        hbox.addWidget(datatype)
        hbox.addStretch(1)
        grid.addLayout(hbox, row, column)
        return temp

    def initUI(self):

        self.definido = False  # no se si sea apropiado ponerlo acá...

        # Cuadrícula general del Frame
        mprincipal = QVBoxLayout()
        mprincipal.addStretch(0)

        # Grid de datos rápidos
        datos = self.datos_rapidos()
        mprincipal.addWidget(datos)
        mprincipal.addStretch(0)

        # Corrida de botones de acción
        mbotones = QHBoxLayout()
        mbotones.addStretch(2)

        # Columna de botones de control de flujo
        mflujo = QVBoxLayout()  # m_nombre es el menu
        nflujo = ['Iniciar', 'Detener', 'Reiniciar']  # n_nombre son los nombres de los botones
        bflujo = []  # b_nombre arreglo de acceso a cada botón
        mflujo.addStretch(1)
        for flujo in nflujo:
            aux = QPushButton(flujo)    # Hacer el botón
            mflujo.addWidget(aux)       # Agregarlo a la cuadrícula
            bflujo.append(aux)          # Arreglo de acceso
            mflujo.addStretch(0)
        mflujo.addStretch(1)

        mbotones.addLayout(mflujo)
        mbotones.addStretch(2)
        nbotones = ['Fijar\nParámetros', 'Monitorear\nMediciones', 'Ver Historial\nde Mediciones', 'Panel de \nAlertas']
        self.bbotones = []
        for boton in nbotones:
            aux = QPushButton(boton)    # Hacer el botón
            mbotones.addWidget(aux)     # Agregarlo a la cuadrícula
            mbotones.addStretch(1)
            self.bbotones.append(aux)        # Arreglo de acceso
        mbotones.addStretch(1)

        self.bbotones[0].setCheckable(True)
        # if self.definido:
        self.bbotones[1].setCheckable(True)
        self.bbotones[2].setCheckable(True)
        self.bbotones[3].setCheckable(True)

        #Conectar el slot para mostrar SVPARAMETROS al botón
        self.bbotones[0].clicked.connect(self.mostrar_svparametros)
#        self.bbotones[1].clicked.connect(self.mostrar_svinterpretacion)
#        self.bbotones[2].clicked.connect(self.mostrar_svhistorial)
#        self.bbotones[3].clicked.connect(self.mostrar_svalertas)

        mprincipal.addLayout(mbotones)
        mprincipal.addStretch(1)

        # Aún no compila bien así que he estado trabajando a ciegas hahah kill me pls
#        self.SVParam = SVParametros()
#        mprincipal.addWidget(self.SVParam)

        self.setLayout(mprincipal)

        #Crear svparametros
        self.sv = SVParametros()

        #¿Servirá?
        mprincipal.addWidget(self.sv)
        self.sv.hide()

        #Slot para mostrar svparametros
    def mostrar_svparametros(self, pressed):
        if pressed:
            self.sv.show()
#            self.desmarcar(0)
        else:
            self.sv.hide()
"""
    def mostrar_svinterpretacion(self, pressed):
        if pressed:
            self.desmarcar(1)

    def mostrar_svhistorial(self, pressed):
        if pressed:
            self.desmarcar(2)

    def mostrar_svalertas(self, pressed):
        if pressed:
            self.desmarcar(3)

    def desmarcar(self, excepcion):
        for i in range(0, 4) :
            if i != excepcion :
                if self.bbotones[i].ischecked() :
                    self.bbotones[i].setchecked(False)
                else :
                    continue
"""

# Subventana de parámetros
class SVParametros(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch(2)

        # lista dropdown de contenedores
        LDcont = QComboBox()
        nombrecont = QLabel("Tipo de contenedor:")
        layout.addWidget(nombrecont)
        layout.addStretch(1)
        layout.addWidget(LDcont)
        LDcont.addItem(None)
        LDcont.addItem("Cúbico")
        LDcont.addItem("Cilíndrico")
        LDcont.activated[str].connect(self.LDpick)

        # Slider Temperatura
        SliderT = QHSpinBoxRangeSlider([-25, 125, 0.1], [0, 15])
        nombreT = QLabel("Rango de Temperatura:")
        layout.addWidget(nombreT)
        layout.addStretch(1)
        layout.addWidget(SliderT)
        SliderT.setEmitWhileMoving(False)
        # Falta activarlo pero no he descubierto como y la documentacion de la otra clase no me ayura

        # Slider Porcentaje Volumen
        SliderV = QHSpinBoxRangeSlider([0, 100, 0.1], [5, 15])
        nombreV = QLabel("Rango de Volumen:")
        layout.addWidget(nombreV)
        layout.addStretch(1)
        layout.addWidget(SliderV)
        SliderT.setEmitWhileMoving(False)
        # Falta activarlo

        # Textboxes para base y altura del contenedor
        TextBoxBase = QLineEdit()
        nombrebase = QLabel("Área basal del contenedor:")
        layout.addWidget(nombrebase)
        layout.addStretch(1)
        rotuladorbase = QHBoxLayout()
        rotuladorbase.addStretch(1)
        rotuladorbase.addWidget(TextBoxBase)
        TextBoxBase.setInputMask('0000')   #Debe recibir números de hasta 4 cifras enteras y 2 cifras decimales
        medidabase = QLabel("cm^2")
        rotuladorbase.addStretch(0)
        rotuladorbase.addWidget(medidabase)
        rotuladorbase.addStretch(1)
        layout.addLayout(rotuladorbase)
        TextBoxBase.textChanged[str].connect(self.TBBchanged)

        TextBoxAltura = QLineEdit()
        nombrealtura = QLabel("Altura del contenedor:")
        layout.addWidget(nombrealtura)
        layout.addStretch(1)
        rotuladoraltura = QHBoxLayout()
        rotuladoraltura.addStretch(1)
        rotuladoraltura.addWidget(TextBoxAltura)
        TextBoxAltura.setInputMask('0000')   #Debe recibir números de hasta 4 cifras enteras y 2 cifras decimales
        medidaaltura = QLabel("cm")
        rotuladoraltura.addStretch(0)
        rotuladoraltura.addWidget(medidaaltura)
        rotuladoraltura.addStretch(1)
        layout.addLayout(rotuladoraltura)
        TextBoxBase.textChanged[str].connect(self.TBAchanged)

        # Checkbox y Textbox para el techo del contenedor
        self.CheckBoxTecho = QCheckBox('¿Es el techo del contenedor de área distinta a su base?')
        layout.addWidget(self.CheckBoxTecho)

        self.framelayout = QWidget()
        layoutframe = QVBoxLayout()
        rotuladorframe = QHBoxLayout()
        rotuladorframe.addStretch(1)
        nombretecho = QLabel("Área del techo del contenedor")
        layoutframe.addWidget(nombretecho)
        layoutframe.addStretch(0)
        TextBoxTecho = QLineEdit()
        TextBoxTecho.setInputMask('9')
        rotuladorframe.addWidget(TextBoxTecho)
        rotuladorframe.addStretch(0)
        medidatecho = QLabel("cm^2")
        rotuladorframe.addWidget(medidatecho)
        rotuladorframe.addStretch(1)
        TextBoxBase.textChanged[str].connect(self.TBTchanged)
        self.CheckBoxTecho.stateChanged.connect(self.CBTchanged)
        layoutframe.addLayout(rotuladorframe)
        self.framelayout.setLayout(layoutframe)
        layout.addWidget(self.framelayout)
        layout.addStretch(1)
        self.framelayout.hide()

        # Texto útil
        self.util = QLabel("")
        layout.addWidget(self.util)
        layout.addStretch(2)
        self.setLayout(layout)

    def LDpick(self, pick):
        global G_cont
        G_cont = pick
        self.util.setText("Tipo de contenedor actualizado a " + G_cont)

    def TBAchanged(self, valor):
        global G_altura
        G_altura = float(valor)
        self.util.setText("Altura actualizada a " + str(G_altura))

    def TBBchanged(self, valor):
        global G_base, G_techo
        G_base = float(valor)
        if self.CheckBoxTecho.isChecked() :
            G_techo = G_base
        self.util.setText("Área basal actualizada a " + str(G_base))

    def TBTchanged(self, valor):
        global G_techo
        G_techo = float(valor)
        self.util.setText("Área superior actualizada a " + str(G_techo))

    def CBTchanged(self, state):
        if state == Qt.Checked:
            self.framelayout.show()
        else:
            self.framelayout.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ventana()
    thr = Thread()
    thr.set_main_window(ex)
    thr.set_vol_label(ex.Graf.volumeLabel)
    thr.set_temp_label(ex.Graf.tempLabel)
    thr.set_flux_label(ex.Graf.fluxLabel)
    thr.start()
sys.exit(app.exec_())
