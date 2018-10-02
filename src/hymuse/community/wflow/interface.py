from hymuse.units import units

from hymuse.community.interface import bmi
from hymuse.community.interface.bmi import BMIImplementation, BMIPythonInterface, BMI

from wflow.wflow_bmi import wflowbmi_csdms as _BMI

# note the spaces and /timestep unit (not handled)
# fix in code
bmi.udunit_to_amuse={ "1" : units.none, "none":units.none, "s":units.s, "K":units.K, "-":units.none,
                  "m.day-1" : units.m/units.day, "m3": units.m**3, "m3.day-1" : units.m**3/units.day,
                  "m." : units.m, "m":units.m, "m3.s-1": units.m**3/units.s, "degrees Celcius": units.K,
                  "undefined" : units.none, 'days since 1901-01-01' : units.day, " mm": units.mm,
                  " m^3/s" : units.m**3/units.s, " oC" : units.K, " m" : units.m, " mm/timestep" : units.mm/units.s,
                  "m^3/s" : units.m**3/units.s, " -" : units.none,
                  "seconds since 1970-01-01 00:00:00.0 00:00" : units.s}

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
          worker="wflow_worker"
        elif mode=="grpc":
          implementation=GRPCImplementation
          worker="wflow_worker_grpc"
        else:
          raise Exception("unknown")
        BMIPythonInterface.__init__(self, implementation, worker, **options)

class Wflow(BMI):
    _axes_names=["lon","lat"]
    _axes_unit=[units.deg, units.deg, units.none]

    def __init__(self, **options):
        self._ini_file=options.get("ini_file","")
        BMI.__init__(self, Interface(**options))
  
