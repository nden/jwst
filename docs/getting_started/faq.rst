.. _faq:

==========================
Frequently Asked Questions
==========================

Installation and Setup
=======================

How do I install the pipeline?
------------------------------

The most simple way to install the pipeline is to obtain the latest released
version via. pip and install this into a Python environment. See the
:ref:`QuickStart guide<quickstart>`for basic installation instructions.

It is also possible to install older released versions, or the development version
from Github. For more detailed install instructions, see :ref:`here<installation>`.

How can I grab recent changes (i.e a bug fix) to the pipeline that aren't yet in a public release?
--------------------------------------------------------------------------------------------------

The absolute most up-to-date version of `jwst` is the master branch of the Github
repository. Changes are merged here on a regular basis, and this branch is
constantly evolving between releases. If, for example, a bug is fixed
in the pipeline and you would like to use this fixed version now rather than
waiting for the next release, you will want to install this development version.
See see :ref:`Installing the Development Version from Github<installing_dev>`
for instructions on how to do this.

How do I install an older version of the pipeline?
------------------------------------------------

See :ref:`Installing Previous Releases<installing_previous_release>`.

How do I simultaneously install the development version of `jwst` and one or all of its dependencies?
-----------------------------------------------------------------------------------------------------

If you are in a scenario in which you need both the unreleased, development
version of JWST and the unreleased, development version of one of it's dependency
 packages for recently merged changes that span both packages, first
:ref:`install the development version<installing_dev>` of `jwst`. This will
also install the minimum required versions of dependency packages
(specified by setup.cfg) which will usually be one of the last releases.
Then, uninstall the dependency package that you wish to
have the latest development branch of, and re-install it from Github.

For example, if you need both the dev versions of `jwst` and `stcal` to obtain
recent changes to a step that spans both packages:

	| >> pip install git+https://github.com/spacetelescope/jwst
	| >> pip uninstall stcal
	| >> pip install git+https://github.com/spacetelescope/stcal

As always, this should be done in a Python environment (conda) to keep this
customized install isolated from other environments with stable installations.

If I've already installed `jwst`, how do I update my install?
-------------------------------------------------------------

See :ref:` Upgrading Installed Version<upgrade_install>`. Note that we reccomend
NOT to use `pip --upgrade` as it does not properly update dependency packages.


Running the pipeline
=====================

How do I run the pipeline?
--------------------------

There are two options for running the JWST pipeline - by using the Python
interface, or the Command Line interface (called `strun`).

When using Python, pipeline steps and pipeline modules are imported into a Python
session, at which point they can be configured to set parameters, specifiy skips
and overrides etc., and run on input data. See
:ref:`Running the JWST pipeline: Python Interface<run_from_python>` for more
information.

Alternativley, users can choose to use the command line interface to the pipeline.
With this interface, parameters, overrides, and skips can also be set to customize
processing. See :ref:`Running the JWST pipeline: Command Line Interface<run_from_cli>`
for more information.

Is it better to run the pipline in Python or to use the Command Line Interface?
-------------------------------------------------------------------------------

Both interfaces access the same underyling code and the choice is up to personal
preference.


What do the different Pipelines accept as input?
------------------------------------------------

The pipeline (or an individual pipeline step) accepts a single exposure
or an association of exposures as input. Level 1 and 2 pipelines accept both
single exposure files (`fits`) and association files (`asn.json`), and most Level 3
pipelines require an association.

When using `strun` to run a pipeline/step, the second argument is a path to the
data file.

When using the Python interface, input to a pipeline/step can either be a string
path to a data file, or an opened file in the form of a `Datamodel` object.



Can I substitute reference files when running the pipeline?
-----------------------------------------------------------

Yes. The CRDS-chosen reference file can be overridden when running the pipeline.
If using the Python interface, see <REF>.

How do I use an older version of a reference file when running the pipeline?
----------------------------------------------------------------------------

If you would like to use an older version of a reference file (or roll back to
an entire set of reference files)

Is it possible to run a pipeline stage, but skip one or some of the steps in that Pipeline?
-------------------------------------------------------------------------------------------

The general answer is yes, steps can be skipped in a pipeline. The caveat is that
some steps expect or require a previous step to have been run, and therefore won't
run unless that previous step has been run. For example `resample` requires that the
`assign_wcs` step has already been run.

For directions on how to skip a pipeline step when running in Python, see :ref:`here<skip_step_python>`.
For the command line interface, see :ref:`here<skip_step_cli>`.


General
=======

Can I create my own pipeline? # note to reviewer, is this answer right?
-----------------------------

While you can't define a new Pipeline class, you can define, configure,
and string together Step classes in succession to effectivley create your own pipeline
consisting of the combination and order of steps you choose.


What are the dependency packages of `jwst`?
-------------------------------------------

`jwst` has several dependency packages. The full list of dependencies and their
required minimum versions are specified in the `setup.cfg` file in the top-level
directory of the repository. See <REF> for a description of the major dependency
packages.

What should I do if I find a bug?
---------------------------------

Bugs can be reported on the Issues tab <REF> of the Github repository. If you
aren't sure, contact the `JWST Help Desk <https://jwsthelp.stsci.edu>`_.

If you have implemented a fix for a bug, see `the Github Contribution Guide <https://github.com/spacetelescope/jwst/blob/master/CONTRIBUTING.md>`_
for instructions on how to have your bugfix reviewed and merged.

