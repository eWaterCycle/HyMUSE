from hymuse.units import units

from hymuse.community.interface import bmi
from hymuse.community.interface.bmi import BMIImplementation, BMIPythonInterface, BMI

from toymodel.toymodel_lumped_bmi import toy_bmi as _BMI

try:
  from toymodel.toymodel_lumped_bmi import toy_bmi as _BMI
except:
  _BMI=None

bmi.udunit_to_amuse={ "1" : units.none, "none":units.none, "s":units.s, "K":units.K, "-":units.none,
                  "m.day-1" : units.m/units.day, "m3": units.m**3, "m3.day-1" : units.m**3/units.day,
                  "m." : units.m, "m":units.m, "m3.s-1": units.m**3/units.s, "degrees Celcius": units.K,
                  "undefined" : units.none, 'days since 1901-01-01' : units.day, 'm2' : units.m**2,
                  "mm/d" : 0.001*units.m/units.day, "m3/s" : units.m**3/units.s, "days" : units.day}

class Implementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI()

class GRPCImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=bmi.grpc_factory(_BMI)()

class Docker_GRPCImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=bmi.docker_grpc_factory(_BMI)('ewatercycle/toymodel-grpc4bmi:latest', image_port=55555, input_dir="./input", output_dir="./output")

class Interface(BMIPythonInterface):
    def __init__(self, **options):
        mode=options.get("bmi_mode", "direct")
        if mode=="direct":
          implementation=Implementation
          worker="toymodel_worker"
        elif mode=="grpc":
          implementation=GRPCImplementation
          worker="toymodel_worker_grpc"
        elif mode in ["grpc+docker", "docker+grpc"]:
          implementation=Docker_GRPCImplementation
          worker="toymodel_worker_grpc_docker"
        else:
          raise Exception("unknown")
        BMIPythonInterface.__init__(self, implementation, worker, **options)

class Toymodel(BMI):
    _axes_names=["lat","lon"]
    _axes_unit=[units.deg, units.deg, units.none]

    def __init__(self, **options):
        self._ini_file=options.get("ini_file","")
        BMI.__init__(self, Interface(**options))
  
