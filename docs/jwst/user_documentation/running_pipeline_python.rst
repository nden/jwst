.. _run_from_python:

===========================================
Running the JWST pipeline: Python Interface
===========================================

.. Important:: The use of the ``run`` method to run a pipeline or step is not
   reccomended. Please see :ref:`Run vs. Call methods<run_vs_call>` for more details.:

The Python interface to the JWST pipeline has each `pipeline` and `step` as
objects that can be imported into your Python session, configured, and used to
process input data.

You can execute a pipeline or a step from within Python by importing and using the
``call`` method of the class with an input file (string path or `Datamodel` object)
as the only required argument.

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
intermediate products to disk, but it can be directed to do so or you can
manually save the output datamodel # note to reviewer, what is the reccomended way to do this?


Configuring the Pipeline in Python
==================================

The first example in this section showed how to run a pipeline/step in its default
configuration - when only the input dataset to be processed is passed in as input,
default values for step and pipeline parameters are used and the 'best' reference files
are chosen based on the CRDS context. These, however, can be changed for custom
processing of data - the following sections will demonstrate how to configure the pipeline 
for custom processing (i.e changing parameters, skipping steps, etc.).

**There are two general options for configuring a run of the pipeline or step when running in Python:
overrides can be done directly on a `step` or `pipeline` object, or parameters/directives can be set in 
a parameter file. All the examples below will show how to configure a pipeline/step both ways.** 

Note that if you choose to use a parameter file for configuration, it is suggested that you create a new one
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

When running a pipeline, changing step parameters is done in a similar way but
because a pipeline consists of many steps, individual step parameters are passed
in through a keyword argument called `steps`, which is a nested dictionary keyed
by each step name and then by parameter name. To make the same change to
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


To use an entire set of past reference files from a previous CRDS mapping, see :ref:`here<crds_context>`.

.. _skip_step_python:
Skipping a Pipeline Step
------------------------

When using the Python interface you wish to run a pipeline but skip some of the
steps contained in that pipeline, this can be done in two different ways.

**On Pipeline / Step Object**

Every step in a pipeline has a 'skip' flag that when set to true, will entirely
skip that step. For example, to skip the saturation step in the Detector1Pipeline:
::

	 from jwst.pipeline import Detector1Pipeline
	 result = Detector1Pipeline.call('jw00017001001_01101_00001_nrca1_uncal.fits',
	 							  steps={"saturation" : {"skip": True}})

**Using a Parameter File**

The equivilant to the above example can be done by adding the following snippet
to your parameter file:

	steps:
	- class: jwst.linearity.linearity_step.LinearityStep
	  parameters:
	    skip: true

.. _run_vs_call:
Run vs. Call Methods
--------------------

The `.call` method however, which is the recommended way to run the pipeline,
is slightly different and involves some additional setup internally to allow it
to seamlessly work with parameter files.

When the `.call` method is called on a pipeline instance, a new instance of that
pipeline is created internally. The values in the parameter file are set as
attributes on this new instance, the pipeline is run with these values, and
then it is disposed of and the final result is returned. This is the recommended
way to run the pipeline since it is intended to be configured via parameter files.

The first two options - `.run` and calling the instance directly - are equivalent.

When 'pipe.run' or simply 'pipe()' are called, the instance you created is directly
used. So, any attributes set on that pipeline will be the ones used to direct the processing.
The additional setup done in `call` to set the parameter file as
attributes on the pipeline is not done, you will have to set each pipeline parameter
individually as an attribute on the pipeline instance you created before running it.
For example, if you wanted to use `.run` and configure and call the `tweakreg` step,
that would be done like this:

::

	pipe3 = Image3Pipeline()

	pipe3.brightest = 50
	pipe3.kernel_fwhm = 2.302
	pipe3.minobj = 15
	pipe3.nclip = 2
	pipe3.searchrad = 1.0
	pipe3.separation = 0.5
	pipe3.sigma = 3.0
	pipe3.snr_threshold = 5


	pipe3.run('jw42424001001_01101_00001_nrca5_cal.fits')

Whereas if you used `call`, you could just modify these values in a parameter file.
If you wanted to change only one or two of these parameters, it is much easier to
do so with a parameter file - if you set them directly you will have to set ALL of
the parameters for that step to the default value in the parameter file, then you
can change the ones you desire.

In short, **``call``** is the recommended way to use the pipeline and it uses parameter
files to direct processing, while ``run`` requires you to do all that set up yourself.
