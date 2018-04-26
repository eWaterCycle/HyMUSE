from interface import BMIInterface, BMI

h=BMIInterface(redirection="none")

h.initialize("")

print h.get_input_var_name_count()

var,err=h.get_input_var_name(0)

print h.get_var_itemsize(var)
print h.get_var_nbytes(var)
print h.get_var_type(var)
grid_id,err= h.get_var_grid(var)
rank,err=h.get_grid_rank(grid_id)
print h.get_grid_rank(grid_id)
grid_size,err=h.get_grid_size(grid_id)
print h.get_grid_size(grid_id)
print h.get_grid_type(grid_id)
print h.get_grid_shape(grid_id,range(rank))
print h.get_grid_spacing(grid_id,range(rank))
print h.get_grid_origin(grid_id,range(rank))

print h.get_value_at_indices_float(var,range(grid_size))

print h.get_time_units()

h.finalize()

h.stop()

h=BMI()

print dir(h)
