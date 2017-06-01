from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from qtRangeSlider import QHSpinBoxRangeSlider


# Subventana de parámetros
class SVParametros(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch(0)

        # lista dropdown de contenedores
        LDcont = QComboBox()
        nombrecont = QLabel("Tipo de contenedor:")
        layout.addWidget(nombrecont)
        layout.addStretch(1)
        layout.addWidget(LDcont)
        LDcont.addItem(None)
        LDcont.addItem("Cúbico/Cilíndrico")
        LDcont.activated[str].connect(self.LDpick)

        # Slider Temperatura
        SliderT = QHSpinBoxRangeSlider([-25, 125, 0.1], [0, 15])
        nombreT = QLabel("Rango de Temperatura:")
        layout.addWidget(nombreT)
        layout.addStretch(1)
        layout.addWidget(SliderT)
        SliderT.setEmitWhileMoving(False)
        SliderT.min_spin_box.valueChanged.connect(self.RITSBchange)
        SliderT.max_spin_box.valueChanged.connect(self.RSTSBchange)
        SliderT.range_slider.rangeChanged.connect(self.RTSchange)

        # Slider Porcentaje Volumen
        SliderV = QHSpinBoxRangeSlider([0, 100, 0.1], [5, 15])
        nombreV = QLabel("Rango de Volumen:")
        layout.addWidget(nombreV)
        layout.addStretch(1)
        layout.addWidget(SliderV)
        SliderV.setEmitWhileMoving(False)
        SliderV.min_spin_box.valueChanged.connect(self.RIVSBchange)
        SliderV.max_spin_box.valueChanged.connect(self.RSVSBchange)
        SliderV.range_slider.rangeChanged.connect(self.RVSchange)

        # Textboxes para base y altura del contenedor
        TextBoxBase = QLineEdit()
        nombrebase = QLabel("Área basal del contenedor:")
        layout.addWidget(nombrebase)
        layout.addStretch(1)
        rotuladorbase = QHBoxLayout()
        rotuladorbase.addStretch(1)
        rotuladorbase.addWidget(TextBoxBase)
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
        medidaaltura = QLabel("cm")
        rotuladoraltura.addStretch(0)
        rotuladoraltura.addWidget(medidaaltura)
        rotuladoraltura.addStretch(1)
        layout.addLayout(rotuladoraltura)
        TextBoxAltura.textChanged[str].connect(self.TBAchanged)

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
        rotuladorframe.addWidget(TextBoxTecho)
        rotuladorframe.addStretch(0)

        medidatecho = QLabel("cm^2")
        rotuladorframe.addWidget(medidatecho)
        rotuladorframe.addStretch(1)

        TextBoxTecho.textChanged[str].connect(self.TBTchanged)
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

    #Funciones de actualización. Seguro se pueden resumir pero no se ocupar connect asi que no me atrevo
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

    def RITSBchange(self, valor):
        global G_TI
        G_TI = valor
        self.util.setText("Rango inferior de temperatura actualizado a" + str(G_TI))

    def RSTSBchange(self, valor):
        global G_TS
        G_TS = valor
        self.util.setText("Rango superior de temperatura actualizado a" + str(G_TS))

    def RTSchange(self,valor_min,valor_max):
        global G_TI
        global G_TS
        G_TI = valor_min
        G_TS = valor_max
        self.util.setText("Rango de temperatura actualizado a " + str(G_TI) + " - "+ str(G_TS))

    def RIVSBchange(self, valor):
        global G_VI
        G_VI = valor
        self.util.setText("Rango inferior de volumen actualizado a" + str(G_VI))

    def RSVSBchange(self, valor):
        global G_VS
        G_VS = valor
        self.util.setText("Rango superior de volumen actualizado a" + str(G_VS))

    def RVSchange(self,valor_min,valor_max):
        global G_VI
        global G_VS
        G_VI = valor_min
        G_VS = valor_max
        self.util.setText("Rango de volumen actualizado a " + str(G_VI) + " - "+ str(G_VS))


# Subventana de interpretación
class SVInterpretacion(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
