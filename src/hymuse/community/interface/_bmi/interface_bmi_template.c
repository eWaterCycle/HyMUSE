#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <CODE_BMI_HEADER>
#include <bmi/bmilib.h>

BMI_Model model_;
BMI_Model *model=&model_;

int initialize(char *filename){

  REGISTER_FUNCTION(model);

  if(strlen(filename))
    return BMI_Initialize(model, filename);
  else
    return BMI_Initialize(model, NULL);
}
  
int update(){
  return BMI_Update(model);
}

int update_until(double t){
  return BMI_Update_until(model, t);
}

int update_frac(double frac){
  return BMI_Update_frac(model, frac);
}

int finalize(){
  return BMI_Finalize(model);
}

int get_component_name(char ** name){
  int result;
  static char name_[BMI_MAX_COMPONENT_NAME];
  result=BMI_Get_component_name(model, name_);
  *name=name_;
  return result;
}

int get_output_var_name_count(int * count){
  return BMI_Get_output_var_name_count(model, count);
}

int get_output_var_name(int i, char **name){
  int result, count, j;
  static char name_[BMI_MAX_VAR_NAME];
  char **names;
  result=BMI_Get_output_var_name_count(model, &count);
  names = (char**) malloc (sizeof(char *) * count);
  for (j=0; j<count; j++) names[j] = (char*) malloc (sizeof(char) * BMI_MAX_VAR_NAME);

  result|=BMI_Get_output_var_names(model,names);
  strncpy(name_, names[i], BMI_MAX_VAR_NAME);
  *name=name_;

  for (j=0; j<count; j++) free (names[j]);
  free (names);

  return result;
}

int get_input_var_name_count(int * count){
  return BMI_Get_input_var_name_count(model, count);
}

int get_input_var_name(int i, char **name){
  int result, count, j;
  static char name_[BMI_MAX_VAR_NAME];
  char **names;
  result=BMI_Get_input_var_name_count(model, &count);
  names = (char**) malloc (sizeof(char *) * count);
  for (j=0; j<count; j++) names[j] = (char*) malloc (sizeof(char) * BMI_MAX_VAR_NAME);

  result|=BMI_Get_input_var_names(model,names);
  strncpy(name_, names[i], BMI_MAX_VAR_NAME);
  *name=name_;

  for (j=0; j<count; j++) free (names[j]);
  free (names);

  return result;
}

int get_start_time(double *t){
  return BMI_Get_start_time(model,t);
}

int get_end_time(double *t){
  return BMI_Get_end_time(model,t);
}

int get_current_time(double *t){
  return BMI_Get_current_time(model,t);
}

int get_time_step(double *t){
  return BMI_Get_time_step(model,t);
}

int get_time_units( char ** unit){
  int result;
  static char unit_[BMI_MAX_UNITS_NAME];
  result=BMI_Get_time_units(model,unit_);
  *unit=unit_;
  return result;
}

int get_var_type( char* var_name, char **var_type){
  int result;
  static char type_[BMI_MAX_TYPE_NAME];
  result=BMI_Get_var_type(model,var_name, type_);
  *var_type=type_;
  return result;
}

int get_var_units(char *var_name, char **unit){
  int result;
  static char unit_[BMI_MAX_UNITS_NAME];
  result=BMI_Get_var_units(model,var_name, unit_);
  *unit=unit_;
  return result;
}

int get_var_itemsize(char * var_name, int *size){
  return BMI_Get_var_itemsize(model, var_name, size);
}

int get_var_nbytes(char * var_name, int *nbytes){
  return BMI_Get_var_nbytes(model, var_name, nbytes);
}

int get_var_grid(char * var_name, int * grid_id){
  return BMI_Get_var_grid(model, var_name, grid_id);
}

int get_value_at_indices_float(char ** var_name, int *index, double* value, int N){
  return BMI_Get_value_at_indices(model, var_name[0], value, index,N);
}

int set_value_at_indices_float(char ** var_name, int *index, double* value, N){
  return BMI_Set_value_at_indices(model, var_name[0], index,N, value);
}

int get_grid_rank(int grid_id, int *rank){
  return BMI_Get_grid_rank(model, grid_id, rank);
}

int get_grid_size(int grid_id, int *size){
  return BMI_Get_grid_size(model, grid_id, size);
}

int get_grid_type(int grid_id, char ** type){
  int result;
  char type_[BMI_MAX_TYPE_NAME];
  result=BMI_Get_grid_type(model, grid_id, type_);
  *type=type_;
  return result;
}

int get_grid_shape(int grid_id, int dim, int *size){
  int result;
  static int size_[8]; // ugh, hard coded max dimension...
  result=BMI_Get_grid_shape(model, grid_id, size_);
  if(result==BMI_SUCCESS) *size=size_[dim];
  return result;
}

int get_grid_spacing(int grid_id, int dim, double *spacing){
  int result;
  static double spacing_[8]; // ugh, hard coded max dimension...
  result=BMI_Get_grid_spacing(model, grid_id, spacing_);
  if(result==BMI_SUCCESS) *spacing=spacing_[dim];
  return result;
}

int get_grid_origin(int grid_id, int dim, double *o){
  int result;
  static double o_[8]; // ugh, hard coded max dimension...
  result=BMI_Get_grid_spacing(model, grid_id, o_);
  if(result==BMI_SUCCESS) *o=o_[dim];
  return result;
}

int get_grid_x(int grid_id, int i, double *x){
  double *x_; // may need malloc?
  int result;
  result=BMI_Get_grid_x(model, grid_id, x_);
  if(result==BMI_SUCCESS) *x=x_[i];
  return result;
}

int get_grid_y(int grid_id, int i, double *x){
  double *x_; // may need malloc?
  int result;
  result=BMI_Get_grid_y(model, grid_id, x_);
  if(result==BMI_SUCCESS) *x=x_[i];
  return result;
}

int get_grid_z(int grid_id, int i, double *x){
  double *x_; // may need malloc?
  int result;
  result=BMI_Get_grid_z(model, grid_id, x_);
  if(result==BMI_SUCCESS) *x=x_[i];
  return result;
}
