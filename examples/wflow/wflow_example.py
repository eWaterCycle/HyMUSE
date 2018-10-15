import numpy
from matplotlib import pyplot

from hymuse.units import units
from hymuse.community.wflow.interface import Wflow

ini_file="wflow_sbm.ini"

p=Wflow(redirection="none")

p.parameters.ini_file=ini_file

print "parameters:"
print p.parameters

print "data stores:"
print p.data_store_names()

grid=getattr(p, p.data_store_names()[0])

print grid

minpos=grid.get_minimum_position()
maxpos=grid.get_maximum_position()
extent=[minpos[1].number,maxpos[1].number,minpos[0].number,maxpos[0].number]

tbegin=p.model_time
dt=p.time_step
tend=tbegin+10*dt

f=pyplot.figure()
pyplot.ion()
pyplot.show()

while p.model_time<tend:
    p.evolve_model(p.model_time+p.time_step)
  
    ussd=grid.WaterLevel
    pyplot.clf()
    pyplot.imshow(ussd.value_in(units.m), origin="lower",vmin=0, vmax=5, extent=extent)
    pyplot.title(str((p.model_time-tbegin).in_(units.day)))
    cb=pyplot.colorbar()
    cb.set_label("water level (m)")
    pyplot.draw()
    pyplot.pause(0.1)

p.stop()

print "done"
