from functools import partial

from hymuse.units import units

try:
    from grpc4bmi.bmi_grpc_client import BmiClient
    from grpc4bmi.bmi_client_subproc import BmiClientSubProcess
    HAVE_GRPC4BMI=True
except:
    HAVE_GRPC4BMI=False
    

from hymuse.community.interface import bmi
from hymuse.community.interface.bmi import BMIImplementation, BMIPythonInterface, BMI

from heat import BmiHeat

# override predefined unit dict
bmi.udunit_to_amuse={ "none":units.none, "s":units.s, "K":units.K, "-":units.none}

_BMI=BmiHeat
if HAVE_GRPC4BMI:
    _BMI_GRPC=partial(BmiClientSubProcess, "hymuse.community.heat.heat.BmiHeat")

class HeatImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI()

class HeatGRPCImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI_GRPC()

class HeatInterface(BMIPythonInterface):
    def __init__(self, **options):
        mode=options.get("mode", "local")
        if mode=="local":
          implementation=HeatImplementation
        elif mode=="grpc":
          implementation=HeatGRPCImplementation
        else:
          raise Exception("unknown")
        BMIPythonInterface.__init__(self, implementation,  **options)

class Heat(BMI):
    def __init__(self, **options):
        BMI.__init__(self,HeatInterface(**options))
  
