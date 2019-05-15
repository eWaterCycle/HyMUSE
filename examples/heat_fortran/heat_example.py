from hymuse.units import units

from hymuse.community.heat_fortran.interface import Heat
  
from matplotlib import pyplot  
    
h=Heat(redirection="none")

pyplot.ion()
f=pyplot.figure()
pyplot.show()

h.commit_parameters()

#~ tnow=h.model_time
tend=10 | units.s
dt=h.time_step
tnow=h.model_time

print "grid:", h.grid_0
print "grid:", h.grid_1

print tnow,tend, dt

while tnow<tend:
    h.evolve_model(tnow+dt)
    tnow=h.model_time
    print tnow
    
    f.clf()
    temp=h.grid_0.plate_surface__temperature
    print temp
    pyplot.imshow(temp.value_in(units.K).T,origin='lower')
    pyplot.draw()
    pyplot.pause(0.01)

