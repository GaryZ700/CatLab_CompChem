#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University
#Diatomic Constants Class is meant to provide a convient method to access all of the Diatomic Constants
#for a particular diatomic molecule

from compChemGlobal.plot import widgets
from collections import namedtuple

diatomicConstants = namedtuple(
    "diatomicConstants", 
    "state T w wx wy wz B a y D re u"
)

###################################################################################

def buildDiatomicConstant(state, T, a, B, w, wx, wy, wz, y, D, re, u):
    return diatomicConstants(
        state, T, w, wx, wy, wz, B, a, y, D, re, u
    )

###################################################################################

#Generates a Python Widget Object that is used to build a diatomic constants tuple
#Default Values are for COX from the Diatomic Molecule Notebook provided by Dr. Jerry LaRue
def diatomicConstantsWidget(state="ground", T=0, w=2169.81358, wx=13.28831, wy=0, wz=0, a=0.01750441, B=1.93128087, y=0, D=0, re=1.128323, u=6.857143, bindingFunction=buildDiatomicConstant):
    
      #Default value is for COX from the Matematica Notebook
            stateInput = widgets.Combobox(value=state, description="State", options=["ground", "excited"])
            TInput = widgets.FloatText(description="$T_e$ in $cm^{-1}$", value=T)
            wInput = widgets.FloatText(description="$w_e$ in $cm^{-1}$", value=w)
            wxInput = widgets.FloatText(description="$w_ex_e$ in $cm^{-1}$", value=wx)
            wyInput = widgets.FloatText(description="$w_ey_e$ in $cm^{-1}$", value=wy)
            wzInput = widgets.FloatText(description="$w_ez_e$ in $cm^{-1}$", value=wz)
            BInput = widgets.FloatText(description="$B_e$ in $cm^{-1}$", value=B)
            aInput = widgets.FloatText(description="$alpha_e$ in $cm^{-1}$", value=a) 
            yInput = widgets.FloatText(description="$y_e$ in $cm^{-1}$", value=y)
            DInput = widgets.FloatText(description="$D_e$ in $cm^{-1}$", value=D)
            reInput = widgets.FloatText(description="$r_e$  in $\stackrel{\circ}{A}$", value=re)
            uInput = widgets.FloatText(description="$\mu$ in AMU", value=u)

            return widgets.interactive(
                    bindingFunction,
                    state = stateInput,
                    T = TInput,
                    w = wInput, 
                    wx = wxInput,
                    wy = wyInput,
                    wz = wzInput,
                    B = BInput,
                    a = aInput,
                    y = yInput,
                    D = DInput,
                    re = reInput,
                    u = uInput
                )