from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
import pylab as py
from matplotlib import animation, rc
from IPython.display import HTML
import sys
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-m1", "--M1", required=False, help="M1/M_sun", default=1)
ap.add_argument("-m2", "--M2", required=False, help="M2/M_sun", default=1)
ap.add_argument("-key", "--key", required=False, help="gif(1)/mp4(0)/show(-1)", default=-1)
ap.add_argument("-ms", "--marker_size", required=False, help="Base size of the marker", default=100)
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

# initialization animation function: plot the background of each frame
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])    
    return line1,line2,line3,

def circle(r,phi):
    return np.array([r*np.cos(phi), r*np.sin(phi)])

PHI = np.linspace(0,2*np.pi,360, endpoint=False)

def update(phi):
    x1,y1 = circle(r1,phi)
    x2,y2 = circle(r2,phi+np.pi)
    line1.set_data(x1,y1)
    line2.set_data(x2,y2)
    line3.set_data(0,0)
    return (line1,line2,line3)

fig, ax = py.subplots()
ax.axis('square')
lim = 2*max(r1,r2) + 0.5
ax.set_xlim((-lim, lim))
ax.set_ylim((-lim, lim))
ax.get_xaxis().set_ticks([])    # enable this to hide x axis ticks
ax.get_yaxis().set_ticks([])    # enable this to hide y axis ticks

ax.plot(0,0,'+',markersize = 9, markerfacecolor = "#FDB813",markeredgecolor ="#FD7813" )
line1, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = 100*(ratio/(ratio + 1.0)), markevery=10000, markerfacecolor = '#0077BE',lw=2) 
line2, = ax.plot([], [], 'o-',color = '#e3dccb',markersize = 100*(1.0/(ratio + 1.0)), markerfacecolor = '#f66338',lw=2,markevery=10000)  
line3, = ax.plot([], [], '+',color = 'r',markersize = 10, markerfacecolor = 'r',lw=2,markevery=10000)  

ax.plot(r1*np.cos(PHI),r1*np.sin(PHI),'-', color = '#d2eeff', markerfacecolor = '#0077BE')
ax.plot(r2*np.cos(PHI),r2*np.sin(PHI),'-', color = '#d2eeff', markerfacecolor = '#f66338')

lgnd = ax.legend((line1, line2, line3), ('Binary Component 1', 'Binary Component 2', 'Center of mass'), loc="lower right")
lgnd.legendHandles[0]._legmarker.set_markersize(6)
lgnd.legendHandles[1]._legmarker.set_markersize(6)
lgnd.legendHandles[2]._legmarker.set_markersize(6)

anim = animation.FuncAnimation(fig, update, init_func=init, frames=PHI, interval=10, blit=True, repeat=True)

#HTML(anim.to_html5_video())
if(key == -1):
	anim.save('xyz.png'.format(m1,m2), fps=30,dpi = 500, extra_args=['-vcodec', 'libx264'])
	plt.show()
if(key == 0):
	anim.save('orbit_cartesian_linear_{}_{}.mp4'.format(m1,m2), fps=30,dpi = 500, extra_args=['-vcodec', 'libx264'])
if(key == 1):
	anim.save('orbit_cartesian_linear_{}_{}.gif'.format(m1,m2), writer='imagemagick', fps=30)
toc = time.time()
print("Total time taken: {}s".format(np.round(toc-tic,2)))
