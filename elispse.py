import numpy as np
from numpy import arange
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,FFMpegWriter
import matplotlib.colors as mcolors
from IPython import display
import concurrent.futures
from tqdm import tqdm
import pandas as pd

df = pd.read_csv('planets.csv')
semi_major_ax = list(df['Semi-major axis a (AU)'])
semi_minor_ax = list(df['Semi-minor axis b (AU)'])
eccentrities  = list(df['Eccentricity'])

fig = plt.figure()
fig.set_size_inches(5, 5, True)
  
ax = plt.axes()
ax.set_facecolor('k')

line, = ax.plot(0, 0)


def elipse(major_ax,minor_ax,eccentricity,time_period,time):
    phase = 2*np.pi*time/time_period
    x_corr = major_ax*np.cos(phase)
    y_corr = minor_ax*np.sin(phase)
    x_corr_shifted = x_corr - major_ax*eccentricity
    return x_corr_shifted,y_corr

time_periods     = {'mer':0.241 ,'ven': 0.615,'ear': 1,'mar':1.88,'jup':11.9,'sat':29.4,'ura':83.7,'nep':163.7,'plu':247.9}
planets = ['mer', 'ven', 'ear', 'mar', 'jup', 'sat', 'ura', 'nep']
planets_maj_ax = {k:v for k,v in zip(planets,semi_major_ax)}
planets_min_ax = {k:v for k,v in zip(planets,semi_minor_ax)}
planets_ecc = {k:v for k,v in zip(planets,eccentrities)}
colors = {'mer':'gold','ven': 'red','ear': 'w','mar':'darkred','jup':'brown','sat':'peru','ura':'dodgerblue','nep':'royalblue','plu':'k'}

present_time = 0
def animate(time_duration):
    time_period = time_periods['ear']
    maj_ax = planets_maj_ax['ear']
    min_ax = planets_min_ax['ear']
    eccen = planets_ecc['ear']
    global present_time
    xr_array = [elipse(maj_ax,min_ax,eccen,time_period,time)[0] for time in arange(present_time,time_duration,0.001)]
    yr_array = [elipse(maj_ax,min_ax,eccen,time_period,time)[1] for time in arange(present_time,time_duration,0.001)]
    
    def fun(planet):
        #print(present_time)
        time_period = time_periods[planet]
        maj_ax = planets_maj_ax[planet]
        min_ax = planets_min_ax[planet]
        eccen = planets_ecc[planet]
        
        xy_corr = [elipse(maj_ax,min_ax,eccen,time_period,time) for time in arange(present_time,time_duration,0.001)]
        xj_array = [x for x,_ in xy_corr]
        yj_array = [y for _,y in xy_corr]

        xj_xe = [ji-ei for ji,ei in zip(xj_array,xr_array)]
        yj_ye = [jj-ej for jj,ej in zip(yj_array,yr_array)]
        line.set_xdata(xj_xe)
        line.set_ydata(yj_ye)
        plt.plot(xj_xe,yj_ye,colors[planet])

    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executer:
        executer.map(fun,list(planets[4:]))
    
    plt.plot([0],[0], marker="o", markersize=5, markeredgecolor="blue", markerfacecolor="blue")
    present_time = time_duration

def _write(ani):
    writervideo = FFMpegWriter(fps=30)
    ani.save('outerplanets_v2.mp4', writer=writervideo,dpi=300)
    plt.close()



frames = [i for i in arange(0,170,0.05)]
ani = FuncAnimation(plt.gcf(),animate,frames=tqdm(frames,total=len(frames)))
#plt.show()
_write(ani)

