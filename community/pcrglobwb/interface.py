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

from pcrglobwb.bmiPcrglobwb import BmiPCRGlobWB as _BMI

bmi.udunit_to_amuse={ "1" : units.none, "none":units.none, "s":units.s, "K":units.K, "-":units.none,
                  "m.day-1" : units.m/units.day, "m3": units.m**3, "m3.day-1" : units.m**3/units.day,
                  "m." : units.m, "m":units.m, "m3.s-1": units.m**3/units.s, "degrees Celcius": units.K,
                  "undefined" : units.none, 'days since 1901-01-01' : units.day}

if HAVE_GRPC4BMI:
    _BMI_GRPC=partial(BmiClientSubProcess, "hymuse.community.pcrglobwb.pcrglobwb.bmiPcrglobwb.BmiPCRGlobWB")

class Implementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI()

class GRPCImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI_GRPC()

class PCRGlobWBInterface(BMIPythonInterface):
    def __init__(self, **options):
        mode=options.get("mode", "local")
        if mode=="local":
          implementation=Implementation
        elif mode=="grpc":
          implementation=GRPCImplementation
        else:
          raise Exception("unknown")
        BMIPythonInterface.__init__(self, implementation,  **options)

class PCRGlobWB(BMI):
    _axes_names=["lon","lat"]
    _axes_unit=[units.deg, units.deg, units.none]

    def __init__(self, **options):
        self._ini_file=options.get("ini_file","")
        BMI.__init__(self,PCRGlobWBInterface(**options))
  
