import numpy as np
from math import exp
from numpy import log, log10
def consolidation_settlement(H, delta_sigma,gamma, Cc, e0):
    '''
    H - Thickness of clay
    delta_sigma - added loading at the top of the clay
    cc - compression index in log10 
    e0 - initial void ratio
    gamma - effective unit weight of the MD
    '''
    sigma_b = H*gamma
    return Cc/(1+e0)*(H*log10((delta_sigma+sigma_b)/sigma_b)- delta_sigma/gamma*log10(delta_sigma) + delta_sigma/gamma*log10(delta_sigma+sigma_b))

# @handcalc(jupyter_display = True, precision = 2)
@np.vectorize
def DoC_Barren_avg(c_h, t, d, D_e):
    '''
    Return the average degree of consolidation
    c_h: ratial coefficient of consolidation
    t: time 
    d: equivalent diameter of the PVD
    D_e: equivalent diameter of the tributary area
    
    '''
    T_h = c_h*t/D_e**2
    n = D_e/d
    F_n = n**2/(n**2-1)*log(n-(3*n**2-1)/(4*n**2))
    U_h = 1-exp(-8*T_h/F_n)
    return U_h