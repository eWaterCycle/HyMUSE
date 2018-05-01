from amuse.units import units

from interface import HeatInterface, Heat
  
from matplotlib import pyplot  
  
h=Heat(redirection='none')

pyplot.ion()
f=pyplot.figure()
pyplot.show()

tnow=h.model_time
tend=10
dt=h.time_step

while tnow<tend:
    h.evolve_model(tnow+dt)
    tnow=h.get_current_time()
    print tnow
    
    f.clf()
    temp=h.grid_0.plate_surface__temperature
    pyplot.imshow(temp.value_in(units.K).T,origin='lower')
    pyplot.draw()

raw_input()
