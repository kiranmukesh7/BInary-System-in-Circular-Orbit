from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
import pylab as py
from matplotlib import animation, rc
from IPython.display import HTML
import time

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-m1", "--M1", required=False, help="M1/M_sun", default=1)
ap.add_argument("-m2", "--M2", required=False, help="M2/M_sun", default=1)
ap.add_argument("-key", "--key", required=False, help="gif(1)/mp4(0)/show(-1)", default=-1)
ap.add_argument("-ms", "--marker_size", required=False, help="Base size of the marker", default=20)
args = vars(ap.parse_args())

m1 = float(args["M1"])
m2 = float(args["M2"])
marker_size = float(args["marker_size"])
if(m1<0 or m2<0):
	print("Negative Mass input encountered (Mass cannot be negative!)")
	sys.exit()

ratio = m1/m2

key = int(args["key"])

tic = time.time()
r1 = 1;
r2 = r1*ratio

PHI = np.linspace(0,2*np.pi,360, endpoint=False)

fig = plt.figure(figsize=(6,6))
ax = plt.subplot(111, polar=True)
ax.set_ylim(0,2*max(r1,r2))
ax.plot(0,0,'+',markersize = 9, markerfacecolor = "#FDB813",markeredgecolor ="#FD7813" )
if(ratio >= 1):
	line1, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = marker_size*np.log10(10*ratio), markevery=10000, markerfacecolor = '#0077BE',lw=2)
	line2, = ax.plot([], [], 'o-',color = '#e3dccb',markersize = marker_size*np.log10(10*1), markerfacecolor = '#f66338',lw=2,markevery=10000) 
elif(ratio < 1):
	line1, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = marker_size*np.log10(10*1), markevery=10000, markerfacecolor = '#0077BE',lw=2)
	line2, = ax.plot([], [], 'o-',color = '#e3dccb',markersize = marker_size*np.log10(10*(1.0/ratio)), markerfacecolor = '#f66338',lw=2,markevery=10000) 

line3, = ax.plot([], [], '+',color = 'r',markersize = 10, markerfacecolor = 'r',lw=2,markevery=10000)  

plt.polar(PHI,r1*np.ones(PHI.size),'-', color = '#d2eeff', markerfacecolor = '#0077BE')
plt.polar(PHI,r2*np.ones(PHI.size),'-', color = '#e3dccb', markerfacecolor = '#f66338')

def update(phi):
    line1.set_xdata(phi)
    line1.set_ydata(r1)
    line2.set_xdata(phi+np.pi)
    line2.set_ydata(r2)
    line3.set_xdata(phi)
    line3.set_ydata(0)
    return (line1,line2,line3)


lgnd = ax.legend((line1, line2, line3), ('Binary Component 1', 'Binary Component 2', 'Center of mass'), loc="lower right")
lgnd.legendHandles[0]._legmarker.set_markersize(6)
lgnd.legendHandles[1]._legmarker.set_markersize(6)
lgnd.legendHandles[2]._legmarker.set_markersize(6)

anim = FuncAnimation(fig, update, frames=PHI, interval=10,blit=True)
if(key == -1):
	plt.show()
if(key == 0):
	anim.save('orbit_polar_log_{}_{}.mp4'.format(m1,m2), fps=30,dpi = 500, extra_args=['-vcodec', 'libx264'])
#HTML(anim.to_html5_video())
elif(key == 1):
	anim.save('orbit_polar_log_{}_{}.gif'.format(m1,m2), writer='imagemagick', fps=30)
toc = time.time()
print("Total time taken: {}s".format(np.round(toc-tic,2)))
