# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR ?= ../../../..
-include $(AMUSE_DIR)/config.mk

CODE_GENERATOR = $(AMUSE_DIR)/build.py

CODEDIR = toymodel
REPODIR = ewatercycle-toymodels

# DOWNLOAD_CODES=all will checkout entire repo with ssh, intended for developers of the components.
# DOWNLOAD_CODES=latest will (shallow) checkout latest revision only
# DOWNLOAD_CODES=<anythin else> will (shallow) checkout release tag ..
GIT_DEFAULT_TAG = no_xarray
GIT_CLONE_CMD = git clone -b $(GIT_DEFAULT_TAG) --single-branch --depth=1
GIT_REPO = https://github.com/eWaterCycle/ewatercycle-toymodels.git
ifeq ($(DOWNLOAD_CODES), all)
    GIT_CLONE_CMD = git clone
    GIT_REPO = git@github.com:eWaterCycle/ewatercycle-toymodels.git
endif
ifeq ($(DOWNLOAD_CODES), latest)
    GIT_CLONE_CMD = git clone --depth=1
endif

.PHONY: download

all: toymodel_worker_grpc_docker

$(CODEDIR): $(REPODIR)
	mkdir $(CODEDIR)
	cp $(REPODIR)/*.py $(CODEDIR)/
	cp -r $(REPODIR)/bmi/bmi $(CODEDIR)/

toymodel_worker: $(CODEDIR) interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.toymodel.interface Interface Implementation -o $@

toymodel_worker_grpc: $(CODEDIR) interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.toymodel.interface Interface GRPCImplementation -o $@

toymodel_worker_grpc_docker: interface.py
	$(CODE_GENERATOR) --type=py --mode=mpi -x hymuse.community.toymodel.interface Interface Docker_GRPCImplementation -o $@

ifdef DOWNLOAD_CODES
$(REPODIR): download
else
$(REPODIR):
	@echo "ERROR: need to download code, but DOWNLOAD_CODES is not set" 
	@false 
endif

update: $(CODEDIR) 
	cd $(CODEDIR); git pull

clean:
	$(RM) -f *.pyc toymodel_worker*
	$(RM) -rf $(CODEDIR)

distclean: clean $(REPODIR)
	$(RM) -rf $(REPODIR)

download:
	$(GIT_CLONE_CMD) $(GIT_REPO)

