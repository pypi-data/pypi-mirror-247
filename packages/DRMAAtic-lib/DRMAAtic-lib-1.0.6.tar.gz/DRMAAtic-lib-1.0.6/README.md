# DRMAAtic-lib
Scheduling libraries for DRMAAtic @BioCompUP, wrapping the ``drmaa-python`` library and adding the implementations
for Slurm and SGE.

## Installation
```shell
pip install DRMAAtic-lib
```
This will also pull the ``drmaa-python`` library. You can see the latest version of the library [here](https://pypi.org/project/DRMAAtic-lib/).

## Requirements
- Slurm or SGE installed
- ``libslurm-dev`` library for Slurm or ``gridengine-dev`` for SGE, both downloadable with apt
- ``libdrmaa`` C bindings for Slurm or SGE
  - [slurm-drmaa](https://github.com/natefoo/slurm-drmaa) for Slurm
- ``drmaa-python`` python library

## ENV variables
Set the env variables for the ``drmaa-python`` library. With PyCharm you can set this env variables in the run configuration.

### SGE
```shell
export SGE_ROOT=/path/to/gridengine
export SGE_CELL=default
```
### SLURM
Set the path to the libdrmaa library C binding
```shell
export DRMAA_LIBRARY_PATH=/usr/lib/slurm-drmaa/libdrmaa.so
```
