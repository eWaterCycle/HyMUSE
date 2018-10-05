import os.path
from functools import partial

from amuse.units import units

from amuse.datamodel import CartesianGrid

from amuse.support.interface import InCodeComponentImplementation
from amuse.rfi.core import  PythonCodeInterface, CodeInterface, legacy_function, \
                            LegacyFunctionSpecification, remote_function

try:
    from grpc4bmi.bmi_grpc_client import BmiClient
    from grpc4bmi.bmi_client_subproc import BmiClientSubProcess
    from grpc4bmi.bmi_client_docker import BmiClientDocker
    HAVE_GRPC4BMI=True
except:
    HAVE_GRPC4BMI=False

def grpc_factory(_BMI):
    if not HAVE_GRPC4BMI:
        raise Exception("import of grpc4bmi failed - not installed?") 
    return partial(BmiClientSubProcess, _BMI.__module__+"."+_BMI.__name__)

def docker_grpc_factory(_BMI):
    if not HAVE_GRPC4BMI:
        raise Exception("import of grpc4bmi failed - not installed?") 
    return BmiClientDocker


# from hymuse.units.udunits import udunit_to_amuse ?
# in practice it turns out that this converter dict needs tailoring to codes -> override in interface.py
udunit_to_amuse={}

# dict to get AMUSE grid class
grid_class=dict(uniform_rectilinear_grid=CartesianGrid)

# not necessary for numpy >= 1.6
def ravel_index(pos, shape):
    res = 0
    acc = 1
    for pi, si in zip(reversed(pos), reversed(shape)):
        res += pi * acc
        acc *= si
    return res

def generate_c_interface_file(include_file, register_function_name):
    srcdir=os.path.dirname(os.path.abspath(__file__))
    
    f=open(os.path.join(srcdir,"interface_bmi_template.c"),"r")
    filestring=f.read()
    f.close()
    
    filestring=filestring.replace("CODE_BMI_HEADER", include_file)
    filestring=filestring.replace("REGISTER_FUNCTION", register_function_name)
    
    f=open("interface.c","w")
    f.write(filestring)
    f.close()

class BMIImplementation(object):
    def __init__(self):
        raise Exception("__init__ of BMIImplementation not implemented")

# base BMI functions
    def initialize(self, filename):
        self._BMI.initialize(str(filename) or None)
        return 0

    def update(self):
        self._BMI.update()
        return 0

    def update_until(self,time):
        self._BMI.update_until(time)
        return 0
        
    def update_frac(self,time_frac=0.):
        self._BMI.update(time_frac)
        return 0

    def finalize(self):
        self._BMI.finalize()
        return 0        
        
# BMI info functions

    def get_component_name(self,name):
        name.value=self._BMI.get_component_name()
        return 0

    def get_output_var_name_count(self,count):
        count.value=len(self._BMI.get_output_var_names())
        return 0

    def get_output_var_name(self,i,name):
        name.value=self._BMI.get_output_var_names()[i]
        return 0

    def get_input_var_name_count(self,count):
        count.value=len(self._BMI.get_input_var_names())
        return 0

    def get_input_var_name(self,i,name):
        name.value=self._BMI.get_input_var_names()[i]
        return 0

# BMI time management functions

    def get_start_time(self,start_time):
        start_time.value=self._BMI.get_start_time()
        return 0
        
    def get_end_time(self,end_time):
        end_time.value=self._BMI.get_end_time()
        return 0
        
    def get_time_step(self,time_step):
        time_step.value=self._BMI.get_time_step()
        return 0
        
    def get_current_time(self,time):
        time.value=self._BMI.get_current_time()
        return 0

    def get_time_units(self, unit):
        unit.value=self._BMI.get_time_units() or "none"
        return 0

# BMI variable info functions

    def get_var_type(self,var_name, var_type):
        var_type.value=self._BMI.get_var_type(var_name)
        return 0

    def get_var_units(self,var_name,var_unit):
        var_unit.value=self._BMI.get_var_units(var_name) or "none"
        return 0

    def get_var_itemsize(self,var_name,size):
        value=self._BMI.get_var_itemsize(var_name)
        if value is not None:
            size.value=value
            return 0
        else:
            size.value=0
            return -1

    def get_var_nbytes(self,var_name,nbytes):
        nbytes.value=self._BMI.get_var_nbytes(var_name)
        return 0

    def get_var_grid(self,var_name,grid_id):
        grid_id.value=self._BMI.get_var_grid(var_name)
        return 0

# BMI getters and setters
# atm handle only float 

    def get_value_at_indices_float(self, var_name, index, value, N):
        # add check that all var_name are the same?
        value.value=self._BMI.get_value_at_indices(var_name[0],index)
        return 0

    def set_value_at_indices_float(self,var_name, index, value):
        # add check that all var_name are the same?
        value.value=self._BMI.get_value_at_indices(var_name,[index])
        return 0

# BMI grid information

    def get_grid_rank(self, grid_id,rank):
        value=self._BMI.get_grid_rank(grid_id)
        if value is not None:
            rank.value=value
            return 0
        else:
            rank.value=0
            return -1

    def get_grid_size(self,grid_id,grid_size):
        grid_size.value=self._BMI.get_grid_size(grid_id)
        return 0

    def get_grid_type(self, grid_id,grid_type):
        grid_type.value=self._BMI.get_grid_type(grid_id)
        return 0

    def get_grid_x(self, grid_id, index, grid_x):
        grid_x.value=self._BMI.get_grid_x(grid_id)[int(index)]
        return 0

    def get_grid_y(self, grid_id, index, grid_y):
        grid_y.value=self._BMI.get_grid_y(grid_id)[int(index)]
        return 0

    def get_grid_z(self, grid_id, index, grid_z):
        grid_z.value=self._BMI.get_grid_z(grid_id)[int(index)]
        return 0

# BMI uniform rectilinear

    def get_grid_shape(self,grid_id, dim, shape):
        shape.value=self._BMI.get_grid_shape(grid_id)[dim]
        return 0

    def get_grid_spacing(self,grid_id, dim,spacing):
        spacing.value=self._BMI.get_grid_spacing(grid_id)[dim]
        return 0
#~ 
    def get_grid_origin(self,grid_id, dim, origin):
        origin.value=self._BMI.get_grid_origin(grid_id)[dim]
        return 0

# below can mostly also be used for other languages

class BMIInterface(CodeInterface):
    include_headers = ['worker_code.h']
# base BMI functions

    def commit_parameters(self, ini_file):
        return self.initialize(ini_file)

    @remote_function
    def initialize(filename="s"):
        pass

    @remote_function        
    def update():
        pass

    @remote_function
    def update_until(time=0.):
        pass

    @remote_function
    def update_frac(time_frac=0.):
        pass

    @remote_function
    def finalize():
        pass

# BMI info functions

    @remote_function
    def get_component_name():
        returns (name="s")

    @remote_function
    def get_output_var_name_count():
        returns (count=0)

    @remote_function(can_handle_array=True)
    def get_output_var_name(i=0):
        returns (name="s")

    @remote_function
    def get_input_var_name_count():
        returns (count=0)

    @remote_function(can_handle_array=True)
    def get_input_var_name(i=0):
        returns (name="s")

# BMI time management functions

    @remote_function
    def get_start_time():
        returns (start_time=0.)

    @remote_function    
    def get_end_time(self):
        returns (end_time=0.)

    @remote_function
    def get_time_step(self):
        returns (time_step=0.)

    @remote_function
    def get_current_time():
        returns (time=0.)
 
    @remote_function
    def get_time_units():
        returns (unit='s')

# BMI variable info functions

    @remote_function
    def get_var_type(var_name='s'):
        returns (var_type='s')

    @remote_function
    def get_var_units(var_name='s'):
        returns (unit='s')

    @remote_function
    def get_var_itemsize(var_name='s'):
        returns (size=0)

    @remote_function
    def get_var_nbytes(var_name='s'):
        returns (nbytes=0)

    @remote_function
    def get_var_grid(var_name='s'):
        returns (grid_id=0)

# BMI getters and setters
# atm handle only float 

    @remote_function(must_handle_array=True)    
    def get_value_at_indices_float(var_name="s", index=0):
        returns (value=0.)

    @remote_function(must_handle_array=True)    
    def set_value_at_indices_float(var_name="s", index=0):
        returns (value=0.)

# BMI grid information functions

    @remote_function
    def get_grid_rank(grid_id=0):
        returns (rank=0)
    
    @remote_function
    def get_grid_size(grid_id=0):
        returns (grid_size=0)

    @remote_function
    def get_grid_type(grid_id=0):
        returns (grid_type='s')

# BMI uniform rectilinear grid

    @remote_function(can_handle_array=True)
    def get_grid_shape(grid_id=0, dim=0):
        returns (shape=0)

    @remote_function(can_handle_array=True)
    def get_grid_spacing(grid_id=0, dim=0):
        returns (spacing=0.)

    @remote_function(can_handle_array=True)
    def get_grid_origin(grid_id=0, dim=0):
        returns (origin=0.)

# BMI rectilinear grid

    @remote_function(can_handle_array=True)
    def get_grid_x(self, grid_id=0, i=0):
        returns(x=0.)
    @remote_function(can_handle_array=True)
    def get_grid_y(self, grid_id=0, j=0):
        returns(y=0.)
    @remote_function(can_handle_array=True)
    def get_grid_z(self, grid_id=0, k=0):
        returns(z=0.)

    def cleanup_code(self):
        self.finalize()


# TODO: structured quad and unstructured

class BMIPythonInterface(PythonCodeInterface, BMIInterface):
    pass
    #~ def __init__(self, **options):
        #~ PythonCodeInterface.__init__(self, BMIImplementation,  **options)

class BMI(InCodeComponentImplementation):

    _ini_file=""
    _axes_names="xyz"
    _axes_unit=[units.none]*3

    #~ def __init__(self, **options):
        #~ InCodeComponentImplementation.__init__(self,BMIInterface(**options))
  
    def initialize_code(self):
        pass
  
    def commit_parameters(self):
        self.overridden().commit_parameters(self.parameters.ini_file)

        self._input_var_count=self.get_input_var_name_count()
        self._output_var_count=self.get_output_var_name_count()
        self._input_var_names=set()
        self._output_var_names=set()
        self._input_var_units=dict()
        self._output_var_units=dict()
        for i in range(self._input_var_count):
            name=self.get_input_var_name(i)
            unit=udunit_to_amuse[self.get_var_units(name)]
            self._input_var_names.add(name)
            self._input_var_units[name]=unit
        for i in range(self._output_var_count):
            name=self.get_output_var_name(i)
            unit=udunit_to_amuse[self.get_var_units(name)]
            self._output_var_names.add(name)
            self._output_var_units[name]=unit
        self._var_names=self._input_var_names.union(self._output_var_names)

        self._grids=set()
        for var in self._var_names:
            self._grids.add(self.get_var_grid(var))

        self._grid_types=dict()
        for grid in self._grids:
            self._grid_types[grid]=self.get_grid_type(grid)

        self._time_unit=udunit_to_amuse[self.get_time_units()]

        handler=self.get_handler("METHOD")
        self.define_additional_methods(handler)
        handler=self.get_handler("DATASETS")
        self.define_additional_grids(handler)
        
    def define_state(self, object):
        object.set_initial_state('UNINITIALIZED')
        object.add_transition('UNINITIALIZED', 'INITIALIZED', 'initialize_code')
        object.add_transition('INITIALIZED', 'COMMIT', 'commit_parameters')
        object.add_method('!UNINITIALIZED', 'before_get_parameter')
        object.add_method('INITIALIZED', 'before_set_parameter')
        object.add_transition('!UNINITIALIZED!STOPPED', 'END', 'cleanup_code')
        object.add_transition('END', 'STOPPED', 'stop', False)
        object.add_method('STOPPED', 'stop')

        object.add_method('COMMIT', 'get_current_time')
        object.add_method('COMMIT', 'get_time_step')
        object.add_method('COMMIT', 'evolve_model')
        object.add_method('COMMIT', 'finalize')
        object.add_method('COMMIT', 'before_get_data_store_names')

    def define_methods(self, object):
        pass

    def define_grids(self,object):
        pass
    
    def define_parameters(self,object):
        object.add_interface_parameter(
            "ini_file",
            "configuration file with simulation setup",
            self._ini_file
        )        
    
    def define_additional_methods(self,object):
        object.add_method(
            'get_current_time',
            (),
            (self._time_unit,object.ERROR_CODE)
        )
        object.add_method(
            'get_time_step',
            (),
            (self._time_unit,object.ERROR_CODE)
        )  
        object.add_method(
            'get_grid_x',
            (object.INDEX, object.INDEX),
            (self._axes_unit[0],object.ERROR_CODE)
        )            
        object.add_method(
            'get_grid_y',
            (object.INDEX, object.INDEX),
            (self._axes_unit[1],object.ERROR_CODE)
        )           
        object.add_method(
            'get_grid_z',
            (object.INDEX, object.INDEX),
            (self._axes_unit[2],object.ERROR_CODE)
        )                             
        object.add_method(
            'update_until',
            (self._time_unit,),
            (object.ERROR_CODE,)
        )

        self.evolve_model=self.update_until

        def getter_fac(var):
            def f(self,index):
                unit=self._output_var_units[var]
                return self.get_value_at_indices_float(var,index) | unit
            return f

        for var in self._output_var_names:
            setattr( self, 'get_'+var+'_flat' , getter_fac(var).__get__(self) )
            
        def setter_fac(var):
            def f(self,index,val):
              unit=self._input_var_units[var]
              val=val.value_in(unit)
# todo: select data type              
              return self.set_value_at_indices_float(var,index,val)
            return f

        for var in self._input_var_names:
            setattr( self, 'set_'+var+'_flat', setter_fac(var).__get__(self) )
            
    def define_additional_grids(self,object):
        for grid in self._grids:
            name="grid_"+str(grid)
            if self._grid_types[grid] in ["uniform_rectilinear_grid", "uniform_rectilinear"]:
              shape=self.get_grid_shape(grid, range(self.get_grid_rank(grid)) )
              self.define_additional_cartesian_grid(object,grid, name, shape)
            else:
              raise Exception("grid type {0} not implemented yet".format(self._grid_types[grid]))

            def setter_fac(flat_setter):                   
                def f(self, *index_and_value):
                    flat_index=ravel_index(index[:-1],shape)
                    value=index_and_value[-1]
                    return getattr(self, flat_setter)(flat_index,value)
                return f

            for var in self._input_var_names:
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
                    
            for var in self._output_var_names:
                if self.get_var_grid(var)==grid:
                    getter='get_'+var
                    flat_getter='get_'+var+'_flat'
                    setattr( self, getter, getter_fac(flat_getter).__get__(self) )
                    object.add_getter(name, getter, names=[var])

    def define_additional_cartesian_grid(self, object, grid, name, shape):
        
        def func(self):
          r=()
          for s in shape:
              r+=(0,s-1)
          return r
                  
        grid_range_getter='get_'+name+'_range'
        setattr( self, grid_range_getter, func.__get__(self) )
        object.define_grid(name,axes_names=self._axes_names, grid_class=CartesianGrid)
        object.set_grid_range(name,grid_range_getter)

        def getter(self, *index):
          x=self.get_grid_x(grid, index[0])
          if len(index)==1: return (x,)
          y=self.get_grid_y(grid, index[1])
          if len(index)==2: return (x,y)
          z=self.get_grid_z(grid, index[2])
          return (x,y,z)

        grid_position_getter="get_"+name+"_position"
        setattr( self, grid_position_getter, getter.__get__(self))
        object.add_getter(name, grid_position_getter, names=self._axes_names)

    def define_properties(self, object):
        object.add_property('get_current_time', public_name = "model_time")
        object.add_property('get_time_step', public_name = "time_step")
    
