import numpy as np
from numpy import arange
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,FFMpegWriter
import matplotlib.colors as mcolors
from IPython import display
import concurrent.futures
from tqdm import tqdm

fig = plt.figure()
fig.set_size_inches(5, 5, True)
  
ax = plt.axes()
ax.set_facecolor('k')

line, = ax.plot(0, 0)

def circle(radius,time_period,time):
    phase = 2*np.pi*time/time_period
    x_corr = radius*np.cos(phase)
    y_corr = radius*np.sin(phase)
    return x_corr,y_corr

def elipse(major_ax,minor_ax,time_period,time):
    phase = 2*np.pi*time/time_period
    x_corr = major_ax*np.cos(phase)
    y_corr = minor_ax*np.sin(phase)
    x_corr_shifted = major_ax*np.cos(phase) + major_ax/2
    return x_corr_shifted,y_corr

time_periods     = {'mer':0.241 ,'ven': 0.615,'ear': 1,'mar':1.88,'jup':11.9,'sat':29.4,'ura':83.7,'nep':163.7,'plu':247.9}
distance_fromsun = {'mer':0.387 ,'ven': 0.723,'ear': 1,'mar':1.52,'jup':5.20,'sat':9.58,'ura':19.20,'nep':30.05,'plu':39.48}
colors = {'mer':'gold','ven': 'red','ear': 'w','mar':'darkred','jup':'brown','sat':'peru','ura':'dodgerblue','nep':'royalblue','plu':'k'}

present_time = 0

def animate(time_duration):
    time_period = time_periods['ear']
    radius = distance_fromsun['ear']
    global present_time
    xe_array = [circle(radius,time_period,time)[0] for time in arange(present_time,time_duration,0.001)]
    ye_array = [circle(radius,time_period,time)[1] for time in arange(present_time,time_duration,0.001)]
    
    def fun(planet):
        #print(present_time)
        time_period = time_periods[planet]
        radius = distance_fromsun[planet]
        
        xy_corr = [circle(radius,time_period,time) for time in arange(present_time,time_duration,0.001)]
        xj_array = [x for x,_ in xy_corr]
        yj_array = [y for _,y in xy_corr]

        xj_xe = [ji-ei for ji,ei in zip(xj_array,xe_array)]
        yj_ye = [jj-ej for jj,ej in zip(yj_array,ye_array)]
        line.set_xdata(xj_xe)
        line.set_ydata(yj_ye)
        plt.plot(xj_xe,yj_ye,colors[planet])

    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executer:
        executer.map(fun,list(distance_fromsun.keys())[:4])
    
    present_time = time_duration

def _write(ani):
    writervideo = FFMpegWriter(fps=30)
    ani.save('actual_innerplanets.mp4', writer=writervideo,dpi=300)
    plt.close()



frames = [i for i in arange(0,30,0.05)]
ani = FuncAnimation(plt.gcf(),animate,frames=tqdm(frames,total=len(frames)))
plt.show()

