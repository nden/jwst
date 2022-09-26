.. _run_from_cli:

=================================================
Running the JWST pipeline: Command Line Interface
=================================================

.. note::

   For seasoned users who are familiar with using ``collect_pipeline_cfgs`` and
   running pipelines by the default configuration (CFG) files, please note that
   this functionality has been deprecated. Please read :ref:`CFG Usage
   Deprecation Notice<cfg_usage_deprecation_notice>`.

Individual steps and pipelines (consisting of a series of steps) can be run
from the command line using the ``strun`` command:
::

    $ strun <pipeline_name, class_name, or parameter_file> <input_file>

The first argument to ``strun`` must be one of either a pipeline name, python
class of the step or pipeline to be run, or the name of a parameter file for the
desired step or pipeline (see :ref:`parameter_files`). The second argument to
``strun`` is the name of the input data file to be processed.

For example, the Stage 1 pipeline is implemented by the class
:ref:`jwst.pipeline.Detector1Pipeline <calwebb_detector1>`. The command to run this pipeline is as
follows:
::

  $ strun jwst.pipeline.Detector1Pipeline jw00017001001_01101_00001_nrca1_uncal.fits

Pipeline classes also have a **pipeline name**, or **alias**, that can be used instead of the
full class specification. For example, ``jwst.pipeline.Detector1Pipeline`` has the
alias ``calwebb_detector1`` and can be run as
::

  $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits

A full list of pipeline aliases can be found in :ref:`Pipeline Stages <pipelines>`.

Exit Status
-----------
``strun`` produces the following exit status codes:

- 0: Successful completion of the step/pipeline
- 1: General error occurred
- 64: No science data found

The "No science data found" condition is returned by the ``assign_wcs`` step of
the ``calwebb_spec2`` pipeline when, after successfully determining the WCS
solution for a file, the WCS indicates that no science data will be found. This
condition most often occurs with NIRSpec's Multi-object Spectroscopy (MOS) mode:
There are certain optical and MSA configurations in which dispersion will not
cross one or the other of NIRSpec's detectors.

Parameters
==========

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

.. _intro_output_directory:

Output Directory
^^^^^^^^^^^^^^^^

By default, all pipeline and step outputs will drop into the current
working directory, i.e., the directory in which the process is
running. To change this, use the ``output_dir`` parameter. For example, to
have all output from ``calwebb_detector1``, including any saved
intermediate steps, appear in the sub-directory ``calibrated``, use
::
   
    $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits
        --output_dir=calibrated

``output_dir`` can be specified at the step level, overriding what was
specified for the pipeline. From the example above, to change the name
and location of the ``dark_current`` step, use the following
::

    $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits
        --output_dir=calibrated
        --steps.dark_current.output_file='dark_sub.fits'
        --steps.dark_current.output_dir='dark_calibrated'

.. _intro_output_file:

Output File
^^^^^^^^^^^

When running a pipeline, the ``stpipe`` infrastructure automatically passes the
output data model from one step to the input of the next step, without
saving any intermediate results to disk. If you want to save the results from
individual steps, you have two options:

  - Specify ``save_results``.
    This option will save the results of the step, using a filename
    created by the step.

  - Specify a file name using ``output_file <basename>``.
    This option will save the step results using the name specified.

For example, to save the result from the dark current step of
``calwebb_detector1`` in a file named based on ``intermediate``, use

::

    $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits
        --steps.dark_current.output_file='intermediate'

A file, ``intermediate_dark_current.fits``, will then be created. Note that the
suffix of the step is always appended to any given name.

You can also specify a particular file name for saving the end result of
the entire pipeline using the ``--output_file`` parameter also
::

    $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits
        --output_file='stage1_processed'

In this situation, using the default configuration, three files are created:

  - ``stage1_processed_trapsfilled.fits``
  - ``stage1_processed_rate.fits``
  - ``stage1_processed_rateints.fits``


Override Reference File
^^^^^^^^^^^^^^^^^^^^^^^

For any step that uses a calibration reference file you always have the
option to override the automatic selection of a reference file from CRDS and
specify your own file to use. Parameters for this are of the form
``--override_<ref_type>``, where ``ref_type`` is the name of the reference file
type, such as ``mask``, ``dark``, ``gain``, or ``linearity``. When in doubt as to
the correct name, just use the ``-h`` argument to ``strun`` to show you the list
of available override parameters.

To override the use of the default linearity file selection, for example,
you would use:
::

  $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits
          --steps.linearity.override_linearity='my_lin.fits'

Skip
^^^^

Another parameter available to all steps in a pipeline is ``skip``. If
``skip=True`` is set for any step, that step will be skipped, with the output of
the previous step being automatically passed directly to the input of the step
following the one that was skipped. For example, if you want to skip the
linearity correction step, one can specify the ``skip`` parameter for the
``strun`` command:
::

    $ strun calwebb_detector1 jw00017001001_01101_00001_nrca1_uncal.fits
        --steps.linearity.skip=True

Alternatively, if using a :ref:`parameter file<parameter_files>`, edit the
file to add the following snippet:
::

  steps:
  - class: jwst.linearity.linearity_step.LinearityStep
    parameters:
      skip: true