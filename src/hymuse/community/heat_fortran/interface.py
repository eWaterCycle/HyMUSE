from hymuse.units import units

from hymuse.community.interface import bmi
from hymuse.community.interface.bmi import BMIInterface, BMI, generate_fortran_interface_file

# note the spaces and /timestep unit (not handled)
# fix in code
bmi.udunit_to_amuse={ "-" : units.none, "K" : units.K, "m2 s-1" : units.m**2/units.s,
                      "s" : units.s}

def generate_interface_file():
    generate_fortran_interface_file("bmiheatf","bmi_heat")

class HeatInterface(BMIInterface):
    def __init__(self, **options):
        BMIInterface.__init__(self, name_of_the_worker="bmi_heat_worker",  **options)

class Heat(BMI):
    _axes_names=["x","y"]
    _axes_unit=[units.m, units.m, units.none]
    def __init__(self, **options):
        BMI.__init__(self,HeatInterface(**options))
