from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
import pylab as py
from matplotlib import animation, rc
from IPython.display import HTML
import time
import argparse
import sys

# initialization animation function: plot the background of each frame
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])    
    return line1,line2,line3,

def circle(r,phi):
    return np.array([r*np.cos(phi), r*np.sin(phi)])

def update_polar(phi):
    line1.set_xdata(phi)
    line1.set_ydata(r1)
    line2.set_xdata(phi+np.pi)
    line2.set_ydata(r2)
    line3.set_xdata(phi)
    line3.set_ydata(0)
    return (line1,line2,line3)

def update_cartesian(phi):
    x1,y1 = circle(r1,phi)
    x2,y2 = circle(r2,phi+np.pi)
    line1.set_data(x1,y1)
    line2.set_data(x2,y2)
    line3.set_data(0,0)
    return (line1,line2,line3)

ap = argparse.ArgumentParser()
ap.add_argument("-m1", "--M1", required=False, help="Mass of first component (in units 'x')", default=1)
ap.add_argument("-m2", "--M2", required=False, help="Mass of second component (in same units 'x')", default=1)
ap.add_argument("-key", "--key", required=False, help="gif(1)/mp4(0)/show(-1)", default=-1)
ap.add_argument("-ms", "--marker_size", required=False, help="Base size of the marker", default=15)
ap.add_argument("-plot", "--plot_type", required=False, help="Type of plot (polar/cartesian)", default="cartesian")
ap.add_argument("-prop", "--proportionality", required=False, help="Marker size mass proportionality (log/lin)", default="lin")
ap.add_argument("-a", "--a", required=False, help="Separation between the binary componenets", default=2.5)
args = vars(ap.parse_args())

m1 = float(args["M1"])
m2 = float(args["M2"])
a = float(args["a"])
marker_size = float(args["marker_size"])
if(m1<0 or m2<0):
	print("Negative Mass input encountered (Mass cannot be negative!)")
	sys.exit()

plot_type = str(args["plot_type"]) 
proportionality = str(args["proportionality"]) 
ratio = m1/m2

key = int(args["key"])

tic = time.time()
r1 = a*(m2/(m1+m2));
r2 = a*(m1/(m1+m2));
PHI = np.linspace(0,2*np.pi,360, endpoint=False)

if(plot_type == "polar"):
	fig = plt.figure(figsize=(6,6))
	ax = plt.subplot(111, polar=True)
	ax.set_ylim(0,2*max(r1,r2))
	ax.plot(0,0,'+',markersize = 9, markerfacecolor = "#FDB813",markeredgecolor ="#FD7813" )
	plt.polar(PHI,r1*np.ones(PHI.size),'-', color = '#d2eeff', markerfacecolor = '#0077BE')
	plt.polar(PHI,r2*np.ones(PHI.size),'-', color = '#e3dccb', markerfacecolor = '#f66338')

elif(plot_type == "cartesian"):
	fig, ax = py.subplots()
	ax.axis('square')
	lim = 2*max(r1,r2) + 0.5
	ax.set_xlim((-lim, lim))
	ax.set_ylim((-lim, lim))
	ax.get_xaxis().set_ticks([])    # enable this to hide x axis ticks
	ax.get_yaxis().set_ticks([])    # enable this to hide y axis ticks
	ax.plot(r1*np.cos(PHI),r1*np.sin(PHI),'-', color = '#d2eeff', markerfacecolor = '#0077BE')
	ax.plot(r2*np.cos(PHI),r2*np.sin(PHI),'-', color = '#d2eeff', markerfacecolor = '#f66338')


if(proportionality == "lin"):
	marker_1 = (ratio/(1.0 + ratio))
	marker_2 = (1.0/(1.0 + ratio))

if(proportionality == "log"):
	if(ratio >= 1):
		marker_1 = np.log10(10*ratio)
		marker_2 = np.log10(10*1)
	if(ratio < 1):
		marker_1 = np.log10(10*1)
		marker_2 = np.log10(10*(1./ratio))

	
line1, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = marker_size*marker_1, markevery=10000, markerfacecolor = '#0077BE',lw=2)
line2, = ax.plot([], [], 'o-',color = '#e3dccb',markersize = marker_size*marker_2, markerfacecolor = '#f66338',lw=2,markevery=10000) 
line3, = ax.plot([], [], '+',color = 'r',markersize = 10, markerfacecolor = 'r',lw=2,markevery=10000) 
lgnd = ax.legend((line1, line2, line3), ('Binary Component 1', 'Binary Component 2', 'Center of mass'), loc="lower right")
lgnd.legendHandles[0]._legmarker.set_markersize(6)
lgnd.legendHandles[1]._legmarker.set_markersize(6)
lgnd.legendHandles[2]._legmarker.set_markersize(6)

if(plot_type == "polar"):
	anim = FuncAnimation(fig, update_polar, frames=PHI, interval=10,blit=True)
elif(plot_type == "cartesian"):
	anim = animation.FuncAnimation(fig, update_cartesian, init_func=init, frames=PHI, interval=10, blit=True, repeat=True)

if(key == -1):
	plt.show()
if(key == 0):
	anim.save('orbit_{}_{}.mp4'.format(m1,m2), fps=30,dpi = 500, extra_args=['-vcodec', 'libx264'])
#HTML(anim.to_html5_video())
elif(key == 1):
	anim.save('orbit_{}_{}.gif'.format(m1,m2), writer='imagemagick', fps=30)
toc = time.time()
print("Total time taken: {}s".format(np.round(toc-tic,2)))
