#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <bmi_class.h>
#include <CODE_BMI_HEADER>

Bmi* model;

extern "C" int initialize(char *filename){

  model = new BMI_CLASS();

  if(strlen(filename))
    return model->initialize(filename);
  else
    return model->initialize(NULL);
}
  
extern "C" int update(){
  return model->update();
}

extern "C" int update_until(double t){
  return model->update_until( t);
}

extern "C" int update_frac(double frac){
  return model->update_frac( frac);
}

extern "C" int finalize(){
  return model->finalize();
}

extern "C" int get_component_name(char ** name){
  int result;
  static char name_[BMI_MAX_COMPONENT_NAME];
  result=model->get_component_name( name_);
  *name=name_;
  return result;
}

extern "C" int get_output_var_name_count(int * count){
  return model->get_output_var_name_count( count);
}

extern "C" int get_output_var_name(int i, char **name){
  int result, count, j;
  static char name_[BMI_MAX_VAR_NAME];
  char **names;
  result=model->get_output_var_name_count( &count);
  names = (char**) malloc (sizeof(char *) * count);
  for (j=0; j<count; j++) names[j] = (char*) malloc (sizeof(char) * BMI_MAX_VAR_NAME);

  result|=model->get_output_var_names(names);
  strncpy(name_, names[i], BMI_MAX_VAR_NAME);
  *name=name_;

  for (j=0; j<count; j++) free (names[j]);
  free (names);

  return result;
}

extern "C" int get_input_var_name_count(int * count){
  return model->get_input_var_name_count( count);
}

extern "C" int get_input_var_name(int i, char **name){
  int result, count, j;
  static char name_[BMI_MAX_VAR_NAME];
  char **names;
  result=model->get_input_var_name_count( &count);
  names = (char**) malloc (sizeof(char *) * count);
  for (j=0; j<count; j++) names[j] = (char*) malloc (sizeof(char) * BMI_MAX_VAR_NAME);

  result|=model->get_input_var_names(names);
  strncpy(name_, names[i], BMI_MAX_VAR_NAME);
  *name=name_;

  for (j=0; j<count; j++) free (names[j]);
  free (names);

  return result;
}

extern "C" int get_start_time(double *t){
  return model->get_start_time(t);
}

extern "C" int get_end_time(double *t){
  return model->get_end_time(t);
}

extern "C" int get_current_time(double *t){
  return model->get_current_time(t);
}

extern "C" int get_time_step(double *t){
  return model->get_time_step(t);
}

extern "C" int get_time_units( char ** unit){
  int result;
  static char unit_[BMI_MAX_UNITS_NAME];
  result=model->get_time_units(unit_);
  *unit=unit_;
  return result;
}

extern "C" int get_var_type( char* var_name, char **var_type){
  int result;
  static char type_[BMI_MAX_TYPE_NAME];
  result=model->get_var_type(var_name, type_);
  *var_type=type_;
  return result;
}

extern "C" int get_var_units(char *var_name, char **unit){
  int result;
  static char unit_[BMI_MAX_UNITS_NAME];
  result=model->get_var_units(var_name, unit_);
  *unit=unit_;
  return result;
}

extern "C" int get_var_itemsize(char * var_name, int *size){
  return model->get_var_itemsize( var_name, size);
}

extern "C" int get_var_nbytes(char * var_name, int *nbytes){
  return model->get_var_nbytes( var_name, nbytes);
}

extern "C" int get_var_grid(char * var_name, int * grid_id){
  return model->get_var_grid( var_name, grid_id);
}

extern "C" int get_value_at_indices_float(char ** var_name, int *index, double* value, int N){
  return model->get_value_at_indices( var_name[0], value, index,N);
}

extern "C" int set_value_at_indices_float(char ** var_name, int *index, double* value, int N){
  return model->set_value_at_indices( var_name[0], index, N, value);
}

extern "C" int get_grid_rank(int grid_id, int *rank){
  return model->get_grid_rank( grid_id, rank);
}

extern "C" int get_grid_size(int grid_id, int *size){
  return model->get_grid_size( grid_id, size);
}

extern "C" int get_grid_type(int grid_id, char ** type){
  int result;
  char type_[BMI_MAX_TYPE_NAME];
  result=model->get_grid_type( grid_id, type_);
  *type=type_;
  return result;
}

extern "C" int get_grid_shape(int grid_id, int dim, int *size){
  int result;
  static int size_[8]; // ugh, hard coded max dimension...
  result=model->get_grid_shape( grid_id, size_);
  if(result==BMI_SUCCESS) *size=size_[dim];
  return result;
}

extern "C" int get_grid_spacing(int grid_id, int dim, double *spacing){
  int result;
  static double spacing_[8]; // ugh, hard coded max dimension...
  result=model->get_grid_spacing( grid_id, spacing_);
  if(result==BMI_SUCCESS) *spacing=spacing_[dim];
  return result;
}

extern "C" int get_grid_origin(int grid_id, int dim, double *o){
  int result;
  static double o_[8]; // ugh, hard coded max dimension...
  result=model->get_grid_spacing( grid_id, o_);
  if(result==BMI_SUCCESS) *o=o_[dim];
  return result;
}

extern "C" int get_grid_x(int *grid_id, int *index, double *x, int N){
  double *x_= (double*)malloc(sizeof(double)*N);; 
  int result;
  result=model->get_grid_x( grid_id[0], x_);
  if(result==BMI_SUCCESS) {
    for(int i=0;i<N;i++) x[i]=x_[index[i]];
  }
  return result;
}

extern "C" int get_grid_y(int *grid_id, int *index, double *x, int N){
  double *x_= (double*)malloc(sizeof(double)*N);; 
  int result;
  result=model->get_grid_y( grid_id[0], x_);
  if(result==BMI_SUCCESS) {
    for(int i=0;i<N;i++) x[i]=x_[index[i]];
  }
  return result;
}

extern "C" int get_grid_z(int *grid_id, int *index, double *x, int N){
  double *x_= (double*)malloc(sizeof(double)*N);; 
  int result;
  result=model->get_grid_z( grid_id[0], x_);
  if(result==BMI_SUCCESS) {
    for(int i=0;i<N;i++) x[i]=x_[index[i]];
  }
  return result;
}
