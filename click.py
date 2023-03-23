# https://stackoverflow.com/questions/63641971/how-to-handle-node-click-in-pyviz-datashader-network-samples

import pandas as pd

import networkx as nx
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graphistry
from pylab import *
import dask.dataframe as dd

class AnnoteFinder:  # thanks to http://www.scipy.org/Cookbook/Matplotlib/Interactive_Plotting
    """
    callback for matplotlib to visit a node (display an annotation) when points are clicked on.  The
    point which is closest to the click and within xtol and ytol is identified.
    """
    def __init__(self, xdata, ydata, annotes, callback = None, threshold=None, axis=None, xtol=None, ytol=None):
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None: xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
        if ytol is None: ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
        self.xtol = xtol
        self.ytol = ytol
        if axis is None: axis = gca()
        self.axis= axis
        self.drawnAnnotations = {}
        self.links = []
        self.callback = callback
        self.threshold = threshold if threshold else 1.0e-3

    def __call__(self, event):
        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
            if self.axis is None or self.axis==event.inaxes:
                annotes = []
                smallest_x_dist = float('inf')
                smallest_y_dist = float('inf')
                for x,y,a in self.data:
                    if abs(clickX-x)<=smallest_x_dist and abs(clickY-y)<=smallest_y_dist :
                        dx, dy = x - clickX, y - clickY
                        annotes.append((dx*dx+dy*dy,x,y, a) )
                        smallest_x_dist=abs(clickX-x)
                        smallest_y_dist=abs(clickY-y)
                if annotes:
                    annotes.sort() # to select the nearest node
                    distance, x, y, annote = annotes[0]
                    print(distance)
                    if distance < self.threshold:
                        if self.callback:
                            self.callback(annote)

class App(tk.Tk):
    def __init__(self, fig):
        super().__init__()
        self.title("Matplotlib in Tkinter")

        # Create a sample matplotlib figure
        self.fig = fig

        # Add the figure to the Tkinter app using a canvas
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def my_callback(node_id):
    print(f'Clicked {node_id}')

# Build your graph
G = nx.karate_club_graph()
pos = nx.spring_layout(G,k=0.1, iterations=20)  # the layout gives us the nodes position x,y,annotes=[],[],[] for key in pos:
x, y, annotes = [], [], []
for key in pos:
    d = pos[key]
    annotes.append(key)
    x.append(d[0])
    y.append(d[1])

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

nx.draw(G, pos, font_size=6, node_color='skyblue', edge_color='#BB0000', width=0.5, node_size=200, with_labels=True)


af = AnnoteFinder(x, y, annotes, my_callback)
connect('button_press_event', af)

class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion

scale = 1.1
zp = ZoomPan()
figZoom = zp.zoom_factory(ax, base_scale = scale)
figPan = zp.pan_factory(ax)

app = App(fig)
app.mainloop()
