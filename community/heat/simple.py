from hymuse.units import units

from hymuse.community.heat.interface import Heat
  
from matplotlib import pyplot  

#~ import logging
#~ logging.basicConfig(level=logging.DEBUG)
#~ logging.getLogger("code").setLevel(logging.DEBUG)

  
h=Heat(channel_type="mpi")#redirection='none',channel_type="sockets", debugger="xterm")

pyplot.ion()
f=pyplot.figure()
pyplot.show()

tnow=h.model_time
tend=10
dt=h.time_step

print h.grid_0

raw_input()

while tnow<tend:
    h.evolve_model(tnow+dt)
    tnow=h.model_time
    print tnow
    
    f.clf()
    temp=h.grid_0.plate_surface__temperature
    pyplot.imshow(temp.value_in(units.K).T,origin='lower')
    pyplot.draw()

raw_input()
