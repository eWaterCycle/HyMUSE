MPIFC ?= mpif90

LIBNAME = libheat.a

OBJS = bmi.o heat.o bmi_heat.o

all:$(LIBNAME)

FCFLAGS += -fPIC

$(LIBNAME): $(OBJS)
	ar -r  $(LIBNAME) $^
	ranlib $(LIBNAME)
	
%.o: %.f90
	$(MPIFC) $(FCFLAGS) -c -o $@ $<

clean:
	rm -Rf *.o *.a *.mod

distclean: clean
