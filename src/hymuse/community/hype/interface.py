from hymuse.units import units

from hymuse.community.interface import bmi
from hymuse.community.interface.bmi import BMIInterface, BMI, generate_cpp_interface_file

# note the spaces and /timestep unit (not handled)
# fix in code
bmi.udunit_to_amuse={ "m3/s" : units.m**3/units.s, 
                      "degree Celsius" : units.K,
                      "degree Celcius" : units.K,
                      "mm water" : units.mm,
                      "g/cm3" : units.g/units.cm**3,
                      "fraction" : units.none,
                      "cm" : units.cm,
                      "mm" : units.mm,
                      "hours since blabla" : units.hour,
                      }

def generate_interface_file():
    generate_cpp_interface_file("build/hype_bmi.h","HypeBmi")

class HypeInterface(BMIInterface):
    def __init__(self, **options):
        BMIInterface.__init__(self, name_of_the_worker="bmi_hype_worker",  **options)

class Hype(BMI):
    _axes_names=["lon","lat"]
    _axes_unit=[units.deg, units.deg, units.none]
    def __init__(self, **options):
        BMI.__init__(self,HypeInterface(**options))
