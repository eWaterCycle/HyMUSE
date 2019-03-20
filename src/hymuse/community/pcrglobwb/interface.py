from hymuse.units import units

from hymuse.community.interface import bmi
from hymuse.community.interface.bmi import BMIImplementation, BMIPythonInterface, BMI, ravel_index

from amuse.support.parameter_tools import CodeWithIniFileParameters

try:
  from pcrglobwb.bmiPcrglobwb import BmiPCRGlobWB as _BMI
except Exception as ex:
  print ex
  _BMI=None

bmi.udunit_to_amuse={ "1" : units.none, "none":units.none, "s":units.s, "K":units.K, "-":units.none,
                  "m.day-1" : units.m/units.day, "m3": units.m**3, "m3.day-1" : units.m**3/units.day,
                  "m." : units.m, "m":units.m, "m3.s-1": units.m**3/units.s, "degrees Celcius": units.Celsius,
                  "undefined" : units.none, 'days since 1901-01-01' : units.day}

parameters=(
    dict(name="use_interface_forcing", group_name="globalOptions", short="use_interface_forcing", dtype="bool", default=False, 
          description="flag to use forcing from interface", ptype="ini"),
)

class Implementation(BMIImplementation):
    def __init__(self):
        self._BMI=_BMI()

class GRPCImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=bmi.grpc_factory(_BMI)()

class Docker_GRPCImplementation(BMIImplementation):
    def __init__(self):
        self._BMI=bmi.docker_grpc_factory(_BMI)('ewatercycle/pcrg-grpc4bmi:latest', image_port=55555, input_dir="./input", output_dir="./output")

class Interface(BMIPythonInterface):
    def __init__(self, **options):
        mode=options.get("bmi_mode", "direct")
        if mode=="direct":
          implementation=Implementation
          worker="pcrglobwb_worker"
        elif mode=="grpc":
          implementation=GRPCImplementation
          worker="pcrglobwb_worker_grpc"
        elif mode in ["grpc+docker", "docker+grpc"]:
          implementation=Docker_GRPCImplementation
          worker="pcrglobwb_worker_grpc_docker"
        else:
          raise Exception("unknown")
        BMIPythonInterface.__init__(self, implementation, worker, **options)

class PCRGlobWB( BMI, CodeWithIniFileParameters):
    _axes_names=["lat","lon"]
    _axes_unit=[units.deg, units.deg, units.none]
    _forcings_var_names=["precipitation", "temperature"]

    def __init__(self, **options):
        self._ini_file=options.get("ini_file","")
        CodeWithIniFileParameters.__init__(self, parameters)
        BMI.__init__(self, Interface(**options))
        self.parameters.ini_file=self._ini_file

    def configuration_file_set(self):
        self.read_inifile_parameters(self.parameters.ini_file)
        handler=self.get_handler('PARAMETER')
        CodeWithIniFileParameters.define_parameters(self,handler)

    def define_additional_grids(self,object):
        BMI.define_additional_grids(self, object)
        grid=0
        name="forcings"#+str(grid)
        if self._grid_types[grid] in ["uniform_rectilinear_grid", "uniform_rectilinear"]:
          shape=self.get_grid_shape(grid, range(self.get_grid_rank(grid)) )
          self.define_additional_cartesian_grid(object,grid, name, shape)
        elif self._grid_types[grid] in ["UNKNOWN"]:
          size=self.get_grid_size(grid)
          shape=(size,)
          self.define_additional_unstructured_grid(object,grid, name, size)
        else:
          raise Exception("grid type {0} not implemented yet".format(self._grid_types[grid]))

        def setter_fac(flat_setter):                   
            def f(self, *index_and_value):
                flat_index=ravel_index(index_and_value[:-1],shape)
                value=index_and_value[-1]
                return getattr(self, flat_setter)(flat_index,value)
            return f

        for var in self._forcings_var_names:
            if self.get_var_grid(var)==grid:
                setter='set_'+var
                flat_setter='set_'+var+'_flat'
                setattr( self, setter, setter_fac(flat_setter).__get__(self) )
                object.add_setter(name, setter, names=[var])

        def getter_fac(flat_getter):
            def f(self, *index):
                flat_index=ravel_index(index,shape)
                return getattr(self, flat_getter)(flat_index)
            return f
                
        for var in self._forcings_var_names:
            if self.get_var_grid(var)==grid:
                getter='get_'+var
                flat_getter='get_'+var+'_flat'
                setattr( self, getter, getter_fac(flat_getter).__get__(self) )
                object.add_getter(name, getter, names=[var])
