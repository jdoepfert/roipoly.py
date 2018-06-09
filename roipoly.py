'''Draw polygon regions of interest (ROIs) in matplotlib images,
similar to Matlab's roipoly function.

See the file example.py for an application. 

Created by Joerg Doepfert 2014 based on code posted by Daniel
Kornhauser.

'''

import sys
import logging

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath


logger = logging.getLogger(__name__)


class Roipoly():

    def __init__(self, fig=None, ax=None, roicolor='b'):
        if fig is None:
            fig = plt.gcf()

        if ax is None:
            ax = plt.gca()

        self.previous_point = []
        self.allxpoints = []
        self.allypoints = []
        self.start_point = []
        self.end_point = []
        self.line = None
        self.roicolor = roicolor
        self.fig = fig
        self.ax = ax

        self.__ID1 = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.__motion_notify_callback)
        self.__ID2 = self.fig.canvas.mpl_connect(
            'button_press_event', self.__button_press_callback)

        if sys.flags.interactive:
            plt.show(block=False)
        else:
            plt.show()

    def get_mask(self, current_image):
        ny, nx = np.shape(current_image)
        poly_verts = [(self.allxpoints[0], self.allypoints[0])]
        for i in range(len(self.allxpoints)-1, -1, -1):
            poly_verts.append((self.allxpoints[i], self.allypoints[i]))

        # Create vertex coordinates for each grid cell...
        # (<0,0> is at the top left of the grid in this system)
        x, y = np.meshgrid(np.arange(nx), np.arange(ny))
        x, y = x.flatten(), y.flatten()
        points = np.vstack((x,y)).T

        roi_path = mplPath.Path(poly_verts)
        grid = roi_path.contains_points(points).reshape((ny,nx))
        return grid
      
    def display_roi(self, **linekwargs):
        l = plt.Line2D(self.allxpoints +
                     [self.allxpoints[0]],
                     self.allypoints +
                     [self.allypoints[0]],
                     color=self.roicolor, **linekwargs)
        ax = plt.gca()
        ax.add_line(l)
        plt.draw()

    def display_mean(self, current_image, **textkwargs):
        mask = self.get_mask(current_image)
        mean = np.mean(np.extract(mask, current_image))
        std = np.std(np.extract(mask, current_image))
        string = "%.3f +- %.3f" % (mean, std)
        plt.text(self.allxpoints[0], self.allypoints[0],
                 string, color=self.roicolor,
                 bbox=dict(facecolor='w', alpha=0.6), **textkwargs)

    def __motion_notify_callback(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if (event.button == None or event.button == 1) and self.line != None: # Move line around
                self.line.set_data([self.previous_point[0], x],
                                   [self.previous_point[1], y])
                self.fig.canvas.draw()


    def __button_press_callback(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            ax = event.inaxes
            if event.button == 1 and event.dblclick == False:  # If you press the left button, single click
                if self.line == None: # if there is no line, create a line
                    self.line = plt.Line2D([x, x],
                                           [y, y],
                                           marker='o',
                                           color=self.roicolor)
                    self.start_point = [x,y]
                    self.previous_point =  self.start_point
                    self.allxpoints=[x]
                    self.allypoints=[y]
                                                
                    ax.add_line(self.line)
                    self.fig.canvas.draw()
                    # add a segment
                else: # if there is a line, create a segment
                    self.line = plt.Line2D([self.previous_point[0], x],
                                           [self.previous_point[1], y],
                                           marker = 'o',color=self.roicolor)
                    self.previous_point = [x,y]
                    self.allxpoints.append(x)
                    self.allypoints.append(y)
                                                                                
                    event.inaxes.add_line(self.line)
                    self.fig.canvas.draw()
            elif ((event.button == 1 and event.dblclick==True) or
                  (event.button == 3 and event.dblclick==False)) and self.line != None: # close the loop and disconnect
                self.fig.canvas.mpl_disconnect(self.__ID1)
                self.fig.canvas.mpl_disconnect(self.__ID2)
                        
                self.line.set_data([self.previous_point[0],
                                    self.start_point[0]],
                                   [self.previous_point[1],
                                    self.start_point[1]])
                ax.add_line(self.line)
                self.fig.canvas.draw()
                self.line = None
                        
                if sys.flags.interactive:
                    pass
                else:
                    #figure has to be closed so that code can continue
                    plt.close(self.fig) 