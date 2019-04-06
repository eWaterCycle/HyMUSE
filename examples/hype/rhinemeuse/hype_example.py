from hymuse.units import units

from hymuse.community.hype.interface import Hype

h=Hype(redirection="none")

h.parameters.ini_file="info.txt"

print h.data_store_names()

print h.grid_1

print "time: ", h.model_time

print "evolve.."
h.evolve_model(h.model_time + (400. | units.day))

print "time: ", h.model_time

print getattr(h.grid_1, "comp outflow olake")

h.stop()

