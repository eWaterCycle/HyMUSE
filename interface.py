from amuse.units import units

from heat import BmiHeat as _BMI

# bmi to land at hymuse.community.interface.bmi eventually? 
import bmi

# override predefined unit dict
bmi.udunit_to_amuse={ "none":units.none, "s":units.s, "K":units.K, "-":units.none}

from bmi import BMIImplementation, BMIPythonInterface, BMI

class HeatImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI()

class HeatInterface(BMIPythonInterface):
    def __init__(self, **options):
        BMIPythonInterface.__init__(self, HeatImplementation,  **options)

class Heat(BMI):
    def __init__(self, **options):
        BMI.__init__(self,HeatInterface(**options))
  
