from hymuse.units import units

from hymuse.community.interface import bmi
from hymuse.community.interface.bmi import BMIImplementation, BMIPythonInterface, BMI

from heat import BmiHeat as _BMI

# override predefined unit dict
bmi.udunit_to_amuse={ "none":units.none, "s":units.s, "K":units.K, "-":units.none}

class Implementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI()

class GRPCImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=bmi.grpc_factory(_BMI)()

class Interface(BMIPythonInterface):
    def __init__(self, **options):
        mode=options.get("bmi_mode", "direct")
        if mode=="direct":
          implementation=Implementation
        elif mode=="grpc":
          implementation=GRPCImplementation
        else:
          raise Exception("unknown")
        BMIPythonInterface.__init__(self, implementation,  **options)

class Heat(BMI):
    def __init__(self, **options):
        BMI.__init__(self,Interface(**options))
  
