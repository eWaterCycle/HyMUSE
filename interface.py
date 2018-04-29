from amuse.units import units

from heat import BmiHeat as _BMI

from amuse.support.interface import InCodeComponentImplementation
from amuse.rfi.core import  PythonCodeInterface,legacy_function, \
                            LegacyFunctionSpecification, remote_function

udunit_to_amuse=dict(none=units.none, s=units.s, K=units.K)

class BMIImplementation(object):
    def __init__(self):
        self._BMI=_BMI()

# base BMI functions
    def initialize(self, filename):
        self._BMI.initialize(filename or None)
        return 0

    def update(self):
        self._BMI.update()
        return 0

    def update_until(self,time):
        self._BMI.update(time)
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

    def get_value_at_indices_float(self, var_name, index, value):
        value.value=self._BMI.get_value_at_indices(var_name,[index])
        return 0

    def set_value_at_indices_float(self,var_name, index, value):
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

class BMIInterface(PythonCodeInterface):
    def __init__(self, **options):
        PythonCodeInterface.__init__(self, BMIImplementation,  **options)

# base BMI functions

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

    @remote_function(can_handle_array=True)    
    def get_value_at_indices_float(var_name="s", index=0):
        returns (value=0.)

    @remote_function(can_handle_array=True)    
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
    def get_grid_x(self, grid_id, i=0):
        returns(x=0.)
    @remote_function(can_handle_array=True)
    def get_grid_y(self, grid_id, j=0):
        returns(y=0.)
    @remote_function(can_handle_array=True)
    def get_grid_z(self, grid_id, k=0):
        returns(z=0.)

# TODO: structured quad and unstructured


    evolve_model=update_until

class BMI(InCodeComponentImplementation):

    def __init__(self, **options):
        InCodeComponentImplementation.__init__(self,BMIInterface(**options))
  
    def initialize_code(self):
        self.initialize("")

        self._input_var_count=self.get_input_var_name_count()
        self._output_var_count=self.get_output_var_name_count()
        self._input_var_names=[]
        self._output_var_names=[]
        self._input_var_units=dict()
        self._output_var_units=dict()
        for i in range(self._input_var_count):
            name=self.get_input_var_name(i)
            unit=udunit_to_amuse[self.get_var_units(name)]
            self._input_var_names.append(name)
            self._input_var_units[name]=unit
        for i in range(self._output_var_count):
            name=self.get_output_var_name(i)
            unit=udunit_to_amuse[self.get_var_units(name)]
            self._output_var_names.append(name)
            self._output_var_units[name]=unit

        self._time_unit=udunit_to_amuse[self.get_time_units()]

        handler=self.get_handler("METHOD")
        self.define_additional_methods(handler)
        
    def cleanup_code(self):
        self.finalize()
        
    def define_state(self, object):
        object.set_initial_state('UNINITIALIZED')
        object.add_transition('UNINITIALIZED', 'INITIALIZED', 'initialize_code')
        object.add_method('INITIALIZED', 'before_get_parameter')
        object.add_method('INITIALIZED', 'before_set_parameter')
        object.add_method('END', 'before_get_parameter')
        object.add_transition('!UNINITIALIZED!STOPPED', 'END', 'cleanup_code')
        object.add_transition('END', 'STOPPED', 'stop', False)
        object.add_method('STOPPED', 'stop')

        object.add_method('INITIALIZED', 'evolve_model')
        object.add_method('INITIALIZED', 'finalize')

    def define_methods(self, object):
        pass

    def define_additional_methods(self,object):
        object.add_method(
            'get_time',
            (),
            (self._time_unit,object.ERROR_CODE)
        )
        object.add_method(
            'get_time_step',
            (),
            (self._time_unit,object.ERROR_CODE)
        )        

