# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR ?= ../../../..
-include $(AMUSE_DIR)/config.mk

CODE_GENERATOR = $(AMUSE_DIR)/build.py

CODEDIR = pcrglobwb

# DOWNLOAD_CODES=all will checkout entire repo with ssh, intended for developers of the components.
# DOWNLOAD_CODES=latest will (shallow) checkout latest revision only
# DOWNLOAD_CODES=<anythin else> will (shallow) checkout release tag ..
GIT_DEFAULT_TAG = bmi_fixes
GIT_CLONE_CMD = git clone -b $(GIT_DEFAULT_TAG) --single-branch --depth=1
GIT_REPO = https://github.com/eWaterCycle/PCR-GLOBWB_model.git
ifeq ($(DOWNLOAD_CODES), all)
    GIT_CLONE_CMD = git clone
    GIT_REPO = git@github.com:eWaterCycle/PCR-GLOBWB_model.git
endif
ifeq ($(DOWNLOAD_CODES), latest)
    GIT_CLONE_CMD = git clone --depth=1
endif

.PHONY: download

all: pcrglobwb_worker_grpc_docker

$(CODEDIR): PCR-GLOBWB_model
	ln -s PCR-GLOBWB_model/model $(CODEDIR)
	touch $(CODEDIR)/__init__.py

pcrglobwb_worker: $(CODEDIR) interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.pcrglobwb.interface Interface Implementation -o $@

pcrglobwb_worker_grpc: $(CODEDIR) interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.pcrglobwb.interface Interface GRPCImplementation -o $@

pcrglobwb_worker_grpc_docker: interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.pcrglobwb.interface Interface Docker_GRPCImplementation -o $@

ifdef DOWNLOAD_CODES
PCR-GLOBWB_model: download
else
PCR-GLOBWB_model:
	@echo "ERROR: need to download PCR-GLOBWB, but DOWNLOAD_CODES is not set" 
	@false 
endif

update: $(CODEDIR) 
	cd $(CODEDIR); git pull

clean:
	$(RM) -f *.pyc pcrglobwb_worker*
	$(RM) -rf $(CODEDIR)

distclean: clean
	$(RM) -rf PCR-GLOBWB_model

download:
	$(GIT_CLONE_CMD) $(GIT_REPO)

