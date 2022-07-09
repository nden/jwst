.. _parameters:

Pipeline/Step Parameters
============================

All pipelines and steps have **parameters** that can be set to change various
aspects of how they execute. To see what parameters are available for any given
pipeline or step, use the ``-h`` option on ``strun``. Some examples are:
::

   $ strun calwebb_detector1 -h
   $ strun jwst.dq_init.DQInitStep -h

To set a parameter, simply specify it on the command line. For example, to have
:ref:`calwebb_detector1 <calwebb_detector1>` save the calibrated ramp files, the
``strun`` command would be as follows:
::

   $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits --save_calibrated_ramp=true

To specify parameter values for an individual step when running a pipeline
use the syntax ``--steps.<step_name>.<parameter>=value``.
For example, to override the default selection of a dark current reference
file from CRDS when running a pipeline:
::

    $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits
          --steps.dark_current.override_dark='my_dark.fits'

If there is need to re-use a set of parameters often, parameters can be stored
in **parameter files**. See :ref:`parameter_files` for more information.

Universal Parameters
--------------------

The set of parameters that are common to all pipelines and steps are referred to
as **universal parameters** and are described below.