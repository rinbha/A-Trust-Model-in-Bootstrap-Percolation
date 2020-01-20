# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 08:39:53 2018

@author: rinni
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json
import os

class stateBPOnER:
    
    def __init__(self,n,den,p,m,r):
        self.n = n #number of vertices
        self.den = den #probability of an edge
        self.p = p #probability of infection
        self.m = m #number of total states
        self.r = r #number of states needed for infection
        self.t = 0 #time
        self.graph = nx.fast_gnp_random_graph(n,den) #create underlying graph
        #label nodes as infected or not
        counter = 0
        for i in range(n):
            if np.random.random() < p:
                self.graph.add_node(i,val = np.random.randint(1,m+1)) #positive means infected
                counter += 1
            else:
                self.graph.add_node(i,val = -1*np.random.randint(1,m+1)) #negative means uninfected
        self.end = False
#        counter = 0
#        for i in range(n):
#            if self.graph.node[i]['val'] > 0: #if a vertex is infected
#                counter += 1
        self.frac_perc = counter/n #the fraction of the vertices that are infected 
        self.frac = [self.frac_perc] #start a list of the fraction of the graph that is infected at each time step
        
    def update(self, garbage=None, im=None):
        n = self.n
        r = self.r
        inf_neighbors = np.zeros((self.m))
        self.end = True
        graph = self.graph
        for i in range(n):
            if self.graph.node[i]['val'] < 0: #if it is uninfected, proceed
                edg = list(self.graph.neighbors(i)) #make a list of the neighbors to check
                count = 0
                for x in edg:
                    if self.graph.node[x]['val'] > 0:
                        if inf_neighbors[self.graph.node[x]['val']-1] == 0:    
                            inf_neighbors[self.graph.node[x]['val']-1] = 1
                            count += 1 #keep running count of number of infected types
                    #We use different graphs to check and to update because the update occurs on the whole graph at once at each time step
                            if count > r-1: 
                                graph.node[i]['val'] *= -1 #infect new vertex
                                self.end = False
                                break
            inf_neighbors = np.zeros((self.m))
        self.graph = graph
        self.t += 1
        counter = 0
        for i in range(n):
            if self.graph.node[i]['val'] > 0:
                counter += 1
        self.frac_perc = counter/n
#        print(self.frac_perc)
        if im:
            im.set_array(self.graph)
            return im,
        else:
            return self.graph
        
    def percolate(self, anim=False, fps=4, dpi=None):
    
        if anim:
            
            # make a custom 2-colour colormap
            cmap = colors.ListedColormap([(225/255,225/255,225/255), (0/255,50/255,100/255)])
            bounds=[-2,0,2]
#            norm = colors.BoundaryNorm(bounds, cmap.N)
        
            # initialize the image
            if not os.path.exists('randtest'):
                os.makedirs('randtest')
            i = 1
            while not self.end:
                plt.ion()
                fig, ax = plt.subplots()
                ax.axis("off")
                #for ind in range(0,10):
                nx.draw_kamada_kawai(self.graph, node_color = [self.graph.node[node]['val'] for node in self.graph], cmap=cmap, ax = ax, node_size = 10, figsize = (30,30))
                plt.savefig(r'C:\Users\rinni\Documents\Python\randtest\randtest_%s.png' % i, format = "PNG")
                self.update()
                i = i + 1
                
            os.system("ffmpeg -r 1 -i C:\\Users\\rinni\\Documents\\Python\\randtest\\randtest_%1d.png -vcodec mpeg4 -y randtest\\randtest.mp4")
            
        else:
            while not self.end:
                self.frac.append(self.frac_perc)
                self.update()
                print(self.frac_perc)
    
def main():
    perc = stateBPOnER(10000,.005,.0003,3,2)
    perc.percolate() 

    
if __name__ == "__main__": 
    main()