import numpy
from matplotlib import pyplot

from hymuse.community.pcrglobwb.interface import PCRGlobWB

ini_file="setup_natural_test.ini"

p=PCRGlobWB()

p.parameters.ini_file=ini_file

print "parameters:"
print p.parameters

print "data stores:"
print p.data_store_names()

grid=getattr(p, p.data_store_names()[0])

minpos=grid.get_minimum_position()
maxpos=grid.get_maximum_position()
extent=[minpos[1].number,maxpos[1].number,minpos[0].number,maxpos[0].number]

tbegin=p.model_time
dt=p.time_step
tend=tbegin+3*dt

f=pyplot.figure()
pyplot.ion()
pyplot.show()

while p.model_time<tend:
    p.evolve_model(p.model_time+p.time_step)
  
    ussd=grid.upper_soil_saturation_degree
    pyplot.clf()
    pyplot.imshow(ussd.number, origin="lower",vmin=0, vmax=1, extent=extent)
    pyplot.title(str(p.model_time-tbegin))
    cb=pyplot.colorbar()
    cb.set_label("upper soil saturation")
    pyplot.draw()
    pyplot.pause(0.1)

p.stop()

print "done"
