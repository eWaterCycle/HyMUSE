# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR?=../../../..
-include ${AMUSE_DIR}/config.mk

CODE_GENERATOR = $(AMUSE_DIR)/build.py

all: heat_worker heat_worker_grpc

heat_worker: heat/heat.py interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.heat.interface Interface Implementation -o $@

heat_worker_grpc: heat/heat.py interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.heat.interface Interface GRPCImplementation -o $@

	
clean:
	$(RM) -f *.bck *.pyc
	$(RM) -f heat_worker heat_worker_grpc
	
distclean: clean 
