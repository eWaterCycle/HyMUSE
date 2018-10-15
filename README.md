# HyMUSE

HyMUSE is a Python framework for interfacing and coupling hydrological models. It is based on the MUSE framework (https://github.com/eWaterCycle/AMUSE-framework).

## installation ##

```
python setup.py build
python setup.py install --prefix
```

## prerequisites ##

It needs a working AMUSE or AMUSE-framework installation. If the gRPC based interfaces are used GRPC4BMI is needed. If thee interfaces are to be approached natively, the any code prerequisites need to be installed. For the interfacing the containerized interfaced, the Python docker module is needed.  

## contributing ##
