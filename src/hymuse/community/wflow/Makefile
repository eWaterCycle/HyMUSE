# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR ?= ../../../..
-include $(AMUSE_DIR)/config.mk

CODE_GENERATOR = $(AMUSE_DIR)/build.py

CODEDIR = wflow

# DOWNLOAD_CODES=all will checkout entire repo with ssh, intended for developers of the components.
# DOWNLOAD_CODES=latest will (shallow) checkout latest revision only
# DOWNLOAD_CODES=<anythin else> will (shallow) checkout release tag ..
GIT_DEFAULT_TAG = bmi_fixes
GIT_CLONE_CMD = git clone -b $(GIT_DEFAULT_TAG) --single-branch --depth=1
GIT_REPO = https://github.com/eWaterCycle/wflow.git
ifeq ($(DOWNLOAD_CODES), all)
    GIT_CLONE_CMD = git clone
    GIT_REPO = git@github.com:eWaterCycle/wflow.git
endif
ifeq ($(DOWNLOAD_CODES), latest)
    GIT_CLONE_CMD = git clone --depth=1
endif

.PHONY: download

all: wflow_worker wflow_worker_grpc wflow_worker_grpc_docker

$(CODEDIR): $(CODEDIR)_repo
	ln -s $(CODEDIR)_repo/wflow-py/wflow $(CODEDIR)
	touch $(CODEDIR)_repo/__init__.py

wflow_worker: $(CODEDIR) interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.wflow.interface Interface Implementation -o $@

wflow_worker_grpc: $(CODEDIR) interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.wflow.interface Interface GRPCImplementation -o $@

wflow_worker_grpc_docker: interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.wflow.interface Interface Docker_GRPCImplementation -o $@

ifdef DOWNLOAD_CODES
$(CODEDIR)_repo: download
else
$(CODEDIR)_repo:
	@echo "ERROR: need to download WFLOW, but DOWNLOAD_CODES is not set" 
	@false 
endif

update: $(CODEDIR) 
	cd $(CODEDIR); git pull

clean:
	$(RM) -f *.pyc wflow_worker*
	$(RM) -rf $(CODEDIR)

distclean: clean
	$(RM) -rf $(CODEDIR)_repo

download:
	$(GIT_CLONE_CMD) $(GIT_REPO) $(CODEDIR)_repo

