.. _installation:

============
Installation
============

Stable releases of the ``jwst`` package are registered at
`PyPI <https://pypi.org/project/jwst/>`_. The development version of `jwst` is
installable from the
`Github repository <https://github.com/spacetelescope/jwst>`_.

Detailed Installation Instructions
==================================

The `jwst` package can be installed into a virtualenv or conda environment via
`pip`. We recommend that for each installation you start by creating a fresh
environment that only has Python installed and then install the `jwst` package
and its dependencies into that bare environment. If using conda environments,
first make sure you have a recent version of Anaconda or Miniconda
`installed <https://docs.conda.io/en/latest/miniconda.html>`_.. If desired, you
can create multiple environments to allow for switching between different
versions of the `jwst` package (e.g. a released version versus the current
development version).

In all cases, the installation is generally a 3-step process:

	1. Create a conda environment
	2. Activate that environment
	3. Install the desired version of the `jwst` package into that environment

Details are given below on how to do this for different types of installations,
including tagged releases, DMS builds used in operations, and development
versions. Remember that all conda operations must be done from within a bash/zsh
shell.


Installing Latest Release
-------------------------

You can install the latest released version via `pip`.  From a bash/zsh shell:

    | >> conda create -n <env_name> python
    | >> conda activate <env_name>
    | >> pip install jwst

Installing Previous Releases
----------------------------

You can also install a specific version (from `jwst 0.17.0` onward):

    | >> conda create -n <env_name> python
    | >> conda activate <env_name>
    | >> pip install jwst==1.3.3

Installing specific versions before `jwst 0.17.0` need to be installed from Github:

    | >> conda create -n <env_name> python
    | >> conda activate <env_name>
    | >> pip install git+https://github.com/spacetelescope/jwst@0.16.2


Installing the Development Version from Github
----------------------------------------------

You can install the latest development version (not as well tested) from the
Github master branch:

    | >> conda create -n <env_name> python
    | >> conda activate <env_name>
    | >> pip install git+https://github.com/spacetelescope/jwst


**For more install instructions, including how to install jwst for development**
**or how to install a DMS operational build, see** `the Github README <https://github.com/spacetelescope/jwst>`_.