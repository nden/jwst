.. _run_from_python:

===========================================
Running the JWST pipeline: Python Interface
===========================================

.. Important:: The use of the ``run`` method to run a pipeline or step is not
   reccomended. Please see :ref:`Run vs. Call methods<run_vs_call>` for more details.::

The Python interface to the JWST pipeline has each `pipeline` and `step` as
objects that can be imported into your Python session, configured, and used to
process input data.

You can execute a pipeline or a step from within Python by importing and using the
``call`` method of the class. Some examples are shown below. For more information,
see :ref:`Execute via call()<call_examples>`::

 from jwst.pipeline import Detector1Pipeline
 result = Detector1Pipeline.call('jw00017001001_01101_00001_nrca1_uncal.fits')

 from jwst.linearity import LinearityStep
 result = LinearityStep.call('jw00001001001_01101_00001_mirimage_uncal.fits')

The above examples are the most basic: they run a pipeline and a step
(respectivley) 'out-of-the-box' using the best reference files and parameters as
determined by CRDS, and running all required steps - the following sections will
describe the Python interface to the JWST pipeline in more detail.


Inputs and Returns, and Outputs
===============================

Both `step` and `pipeline` in the Python interface accept the following input types:
  
  1. A string path to a single `fits` file
  2. A string path to `asn.json` file, for an association of exposures.
  3. A `datamodel` object.

The output from running a `pipeline` or `step` in Python (usually a `datamodel` object)
is returned in-memory. By default, running the pipeline writes out no final or
intermediate products to disk, but it can be directed to do so or you can save the
output datamodel with `ASDF`. 


Configuring the Pipeline in Python
==================================

The first example in this section showed how to run a pipeline/step in its default
configuration, the following sections will demonstrate how to configure the pipeline 
for custom processing (i.e changing parameters, skipping steps, etc.)

**There are two general options for configuring a run of the pipeline or step when running in Python:
overrides can be done directly on a `step` or `pipeline` object, or parameters/directives can be set in 
a parameter file. All the examples below will show how to configure a pipeline/step both ways.** 

If you choose to use a paramter file for configuration, it is suggested that you create a new one
and pass it to the pipeline/step rather than modifying the file in the CRDS cache. See <reference>
for instructions on how to pass in your own parameter file. 


Setting Step Parameters
-----------------------

Note that because there are two ways to set parameters, there is
a hierarchy involved - overrides set on a pipeline or step object will take precendce
over anything in a parameter file. See :ref:`Parameter Precedence` for a full description of
how a parameter gets its final value. The following examples will show how to make various
changes to the setup of a pipeline or step using both by modifying the Python object 
as well as by using parameter files. 


**On Pipeline / Step Object**

When running a single step, keyword arguments can be passed in directly. Parameters
passed in this way will override any step defaults or values in a parameter file.
For example, to change the parameter 'threshold' for the jump detection step:

::
	
	from jwst.jump import JumpStep
	result = JumpStep.call('jw00017001001_01101_00001_nrca1_uncal.fits', threshold=12.0)

When running a pipeline, changing step parameters is done in a similar way but because a pipeline
consists of many steps, individual step parameters are passed in through a keyword argument called `steps`,
which is a nested dictionary keyed by each step name and then by parameter name. To make the same change to
the jump threshold as above when running the full Detector1Pipeline:

::

	from jwst.pipeline import Detector1Pipeline
	result = Detector1Pipeline.call('jw00017001001_01101_00001_nrca1_uncal.fits', steps={'jump' : {'threshold':12.0)}})


**Using a Parameter File**

Alternatively, if using a :ref:`parameter file<parameter_files>`, edit the
file to add the following snippet:

::

  steps:
  - class: jwst.jump.jump_step.JumpStep
    parameters:
      threshold : 12





Overriding Reference Files
--------------------------

By default, when the pipeline or step is run, CRDS will determine the best set of 
reference files based on file metadata and the current CRDS mapping (also known
as 'context'). If you would like to override these files and point the pipeline to
use different files, there are a few options.

**On Pipeline / Step Object**

The first option is to pass in your desired reference files as a keyword argument
to the `steps` parameter when invoking the pipeline/step's ``call`` method.
For example, to override the saturation reference file to a custom file called
'new_saturation_ref_file.fits' when running the `Detector1Pipeline`

::

	 from jwst.pipeline import Detector1Pipeline
	 result = Detector1Pipeline.call('jw00017001001_01101_00001_nrca1_uncal.fits',
	 							  steps={"saturation" : {"override_saturation": '/path/to/new_saturation_ref_file.fits'}})

If you want to override a reference file for a standalone step:

::

	 from jwst.linearity import SaturationStep
	 SaturationStep.call('jw00017001001_01101_00001_nrca1_uncal.fits',
	 					 override_saturation='/path/to/new_saturation_ref_file.fits')


**Using a Parameter File**

Alternatively, if using a :ref:`parameter file<parameter_files>`, edit the
file to add the following snippet:
::

  steps:
  - class: jwst.linearity.linearity_step.LinearityStep
    parameters:
      skip: true

and then run the call the pipeline, which will according to the parameter
precedence rules use values in the parameter file :

::
	result = Detector1Pipeline.call('jw00017001001_01101_00001_nrca1_uncal.fits')


To use an entire set of past reference files from a previous CRDS mapping, see <REFERENCE>.

Skipping a Pipeline Step
------------------------

When using the Python interface you wish to run a pipeline but skip some of the
steps contained in that pipeline, this can be done in two different ways.

**On Pipeline / Step Object**

**Using a Parameter File**

.. _run_vs_call:
Run vs. Call Methods
--------------------
blah blah, blahblahblah
