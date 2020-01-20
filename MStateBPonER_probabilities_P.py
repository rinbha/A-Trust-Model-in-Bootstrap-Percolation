# -*- coding: utf-8 -*-
"""
Runs the m-state r-neighbor T-BP across varying values of p for a fixed number of trials
Generates a comparison between the initial probability of infection, p, and the fraction percolated
Can use this to find the value for the critical probability of infection, p_c, given parameters n, m, r, and den

@author: rinni
"""

import MStateBPonER_P
import numpy as np
import pandas as pd
import eccpy

class stateBPOnERfpvp:
    
    def __init__(self, den = .005, n = 10000, m = 3, r = 2, trials = 100, inc = 30):
        self.n = n #number of nodes
        self.den = den #density of ER graph
        self.m = m #m state
        self.r = r #r neighbor
        self.trials = trials #number of times the T-BP is run
        self.inc = inc #how many values of p are tested
        self.probabilities = np.zeros((inc,3)) #initialize chart of p, average fraction percolated, average time steps taken
        self.p_c = 0 #initialize average fraction infected
    
    def getdata(self):
        #make chart        
        for b in range(self.inc):
            #num_perc = 0
            frac_tot = 0
            perc_time_tot = 0
            p = 0.0003 + (b)/(self.inc*371) #varying values of initial probability of infection, p
            self.probabilities[b,0] = p #first column of chart is p
            for a in range(self.trials): 
                perc = MStateBPonER_P.stateBPOnER(self.n, self.den, p, self.m, self.r)
                perc.percolate()
#                if perc.frac_perc > 0.8:
#                    num_perc += 1
                perc_time_tot += perc.t
                frac_tot += perc.frac_perc
#            probability_of_percolation = num_perc/self.trials
#            self.probabilities[b,1] = probability_of_percolation
            avg_time_perc = perc_time_tot/self.trials
            avg_frac_perc = frac_tot/self.trials
            self.probabilities[b,1] = avg_frac_perc #second column of chart is average fraction percolated
            self.probabilities[b,2] = avg_time_perc #third column of chart is average time of percolation
            df = pd.DataFrame(self.probabilities)
            df.to_csv("mBP_probabilities.csv")
        return self.probabilities
            
    def pc(self):
        #plot chart and find p_c by fitting to dose-response curves
        mat = self.probabilities.copy()
        ps = pd.DataFrame(mat[:,0]) #the dose (p)
        percp = pd.DataFrame(mat[:,1]) #the response (probability of percolation)
        x = ['eccpy|xlsx|generic|vertical']
        x = pd.DataFrame(x)
        writer = pd.ExcelWriter('input.xlsx')
        ps.to_excel(writer, 'dose', index = None, header = ["test"])
        percp.to_excel(writer, 'response', index = None, header = ["test"])
        x.to_excel(writer, 'template_identifier', index = None, header = None)
        writer.save()
        settings = r"C:\Python\ECCpy_settings.xlsx"
        eccpy.run_curvefit(settings)
        xls = pd.ExcelFile(r'C:\Python\pcoutput\input\input.xlsx')
        sheetX = xls.parse(0)
        var1 = sheetX['EC50']
        self.p_c = var1[0]
        print(self.p_c)
        return self.p_c 
    
def main():
    perc = stateBPOnERfpvp()
    perc.getdata()
    perc.pc()
    
if __name__ == "__main__": main()