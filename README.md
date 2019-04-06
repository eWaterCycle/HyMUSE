# HyMUSE

HyMUSE is a Python framework for interfacing and coupling hydrological 
models. It is based on the AMUSE framework 
(https://github.com/eWaterCycle/AMUSE-framework).

## Installation ##

```
python setup.py build
python setup.py install [--prefix install_dir ]
```

## Prerequisites ##

HyMUSE always needs a working AMUSE or AMUSE-framework installation. If the 
gRPC based interfaces are used, GRPC4BMI is needed. If the interfaces are 
to be approached natively, then the code prerequisites need to be 
installed. For the interfacing the containerized interfaced, the Python 
docker module is needed.  

## Current state ##

- BMI interface generator
- PCRGLOB-WB BMI based interface
- WFLOW BMI based interface
- HYPE BMI based interface
- Heat code example BMI based interface
- units

## Contributing ##

Contributions are welcomed.

## License ##

Copyright (c) 2018, Netherlands eScience Center & Delft University of Technology

Apache Software License 2.0
