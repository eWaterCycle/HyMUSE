# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR?=../../../..
-include ${AMUSE_DIR}/config.mk

CODE_GENERATOR = $(AMUSE_DIR)/build.py

BUILDDIR=build

CMAKE_DEPS=CMakeLists.txt ./bmi/CMakeLists.txt ./heat/CMakeLists.txt

BMICODE=heat
INTERFACE=HeatInterface

WORKER=bmi_$(BMICODE)_worker

BMIINC= -I$(BUILDDIR)
BMILIBDIR=
BMILIB= 

FCFLAGS+=$(FS_FLAGS) $(BMIINC)
LIBS+=

all: $(WORKER)

.FORCE:

$(BUILDDIR):
	mkdir -p $(BUILDDIR)
	cp src/*  $(BUILDDIR)

clean:
	rm -f *.pyc worker_code.f90 worker_code.h interface.o interface.f90 *.mod
	make -C $(BUILDDIR) clean

distclean: 
	rm -f *.pyc worker_code.f90 worker_code.h interface.o interface.f90 *.mod
	rm -rf $(BUILDDIR) $(WORKER)

$(BUILDDIR)/libheat.a: $(BUILDDIR)  
	make -C $(BUILDDIR) FCFLAGS="$(FCFLAGS)"

$(WORKER): $(BUILDDIR)/libheat.a worker_code.f90 interface.o
	$(MPIFC) -I$(BUILDDIR) $(FCFLAGS) $(LDFLAGS) worker_code.f90 interface.o  -o $@ $(BUILDDIR)/libheat.a  $(FS_LIBS) 
 
worker_code.f90: interface.py
	$(CODE_GENERATOR) --type=f90 interface.py $(INTERFACE) -o $@

%.o: %.f90
	$(MPIFC) $(FCFLAGS) -c -o $@ $<

interface.f90: .FORCE
	$(PYTHON) -c "import interface; interface.generate_interface_file()"
