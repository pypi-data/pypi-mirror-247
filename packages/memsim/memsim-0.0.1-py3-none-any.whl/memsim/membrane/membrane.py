# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:06:49 2023

@author: Hedi
"""

#from pymem.config import __config__ as cf

from . import*
__R__ = 8.314 # J/mol/K
import time
from tabulate import tabulate
from numpy import exp,linspace,concatenate,array,reshape,split,zeros,vectorize,linspace,absolute
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


class res_membrane:
    @property
    def Vr_out(self):
        return self.Vr[-1]
    @property
    def Vp_out(self):
        return self.Vp[-1]
    @property
    def Cr_out(self):
        return self.Cr[:,-1]
    @property
    def Cp_out(self):
        return self.Cp[:,-1]
    @property
    def net_balance(self):
        return self.parent.Vin-self.Vr_out-self.Vp_out
    @property
    def solute_net_balance(self):
        return array(self.parent.Cin)*self.parent.Vin-self.Cp[:,-1]*self.Vp[-1]-self.Cr[:,-1]*self.Vr[-1]
    @property
    def FRV(self):
        return self.parent.Vin/self.Vr
    @property
    def T(self):
        return self.Cp/self.Cr
    @property
    def R(self):
        return 1 - self.T
    @property
    def FRV_out(self):
        return self.FRV[-1]
    @property
    def T_out(self):
        return self.T[:,-1]
    @property
    def R_out(self):
        return self.R[:,-1]
    

class spiral_membrane(cf.__obj__):
    def __init__(self,**args):
        super().__init__(res_membrane)
        for k,v in args.items():
            if k in list(self.__dict__.keys()):
                setattr(self, k, v)

    def calcul(self):
        st = time.process_time()
        Cin,Vin,B,k=self.Cin,self.Vin,self.B,self.k
        T=self.T+273.15
        α=self.S/self.L
        DPL=self.DP/self.L
        n_solutes = Cin.shape[0]
        def sysdiff(t,y):
            p,Vp,Vr,VCp,VCr=*y[0:3],*split(y[3:],2)
            dpdx=-DPL
            Cr=VCr/Vr
            if Vp:
                Cp=VCp/Vp
            else:
                Cp=zeros(n_solutes)
            
            Cm,Jw, = self.mass_layer(p,Cp,Cr,diffusion=t)[0:2]
            dVpdx=Jw*α
            dVrdx=-dVpdx
            dCpdx=B*(Cm-Cp)*α
            dCrdx=-dCpdx
            return concatenate(([dpdx,dVpdx,dVrdx],dCpdx,dCrdx))
        self.res.x=linspace(0,self.L,100)
        sol = solve_ivp(sysdiff, (0,self.L),
                          concatenate(([self.Pin,0.0,Vin],[0]*n_solutes,Vin*Cin)),
                          method="BDF",t_eval=self.res.x )   
        self.res.p,self.res.Vp,self.res.Vr,Cp,Cr=*sol.y[0:3],*split(sol.y[3:],2)
        self.res.Cr=Cr/self.res.Vr
        self.res.Cp=Cp
        self.res.Cp[:,1:]=self.res.Cp[:,1:]/self.res.Vp[1:]
        self.res.Cm=zeros(self.res.Cp.shape)
        self.res.Jw=zeros(self.res.Cp.shape[1])
        self.res.DP=zeros(self.res.Cp.shape)
        self.res.PIm=zeros(self.res.Cp.shape)
        self.res.PIp=zeros(self.res.Cp.shape)
        self.res.DP=zeros(self.res.Cp.shape)
        for i in range(self.res.x.shape[0]):
            self.res.Cm[:,i],self.res.Jw[i],self.res.PIm[:,i],self.res.PIp[:,i],self.res.DP[:,i], = self.mass_layer(self.res.p[i],self.res.Cp[:,i],self.res.Cr[:,i],diffusion=i)
        self.res.calculation_time = time.process_time()-st
    def mass_layer(self,p,Cp,Cr,diffusion=False):
        k=array(self.k)
        T=self.T+273.15
        PIp=__R__*T*1e-5*Cp # bar
        if diffusion:
            def fm(c):
                PIm=__R__*T*1e-5*c # bar
                DPi=PIm-PIp
                Jw=(p-self.Patm-DPi.sum())*self.Aw
                return abs(c-Cp-(Cr-Cp)*exp(Jw/k))
            Cm=fsolve(fm,Cr)
        else:
            Cm=Cr
        PIm=__R__*T*1e-5*Cm # bar
        DPi=PIm-PIp
        Jw=(p-self.Patm-DPi.sum())*self.Aw
        return Cm,Jw,PIm,PIp,DPi
