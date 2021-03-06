#!/usr/bin/env python
from jwst.stpipe import Pipeline
from jwst import datamodels
import os

# step imports
from jwst.dq_init import dq_init_step
from jwst.saturation import saturation_step
from jwst.ipc import ipc_step
from jwst.superbias import superbias_step
from jwst.refpix import refpix_step
from jwst.reset import reset_step
from jwst.lastframe import lastframe_step
from jwst.linearity import linearity_step
from jwst.dark_current import dark_current_step
from jwst.jump import jump_step
from jwst.ramp_fitting import ramp_fit_step


__version__ = "3.1"

# Define logging
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class SloperPipeline(Pipeline):
    """

    SloperPipeline: Apply all calibration steps to raw JWST
    ramps to produce a 2-D slope product. Included steps are:
    dq_init, saturation, ipc, superbias, refpix, reset,
    lastframe, linearity, dark_current, jump detection, and ramp_fit.

    """

    spec = """
        save_calibrated_ramp = boolean(default=False)
    """

    # Define aliases to steps
    step_defs = {'dq_init' : dq_init_step.DQInitStep,
                 'saturation' : saturation_step.SaturationStep,
                 'ipc' : ipc_step.IPCStep,
                 'superbias' : superbias_step.SuperBiasStep,
                 'refpix' : refpix_step.RefPixStep,
                 'reset' : reset_step.ResetStep,
                 'lastframe' : lastframe_step.LastFrameStep,
                 'linearity' : linearity_step.LinearityStep,
                 'dark_current' : dark_current_step.DarkCurrentStep,
                 'jump' : jump_step.JumpStep,
                 'ramp_fit' : ramp_fit_step.RampFitStep,
                 }


    # start the actual processing
    def process(self, input):

        log.info('Starting calwebb_sloper ...')

        # open the input
        input = models.open(input)

        # apply dq_init, saturation, and ipc steps
        input = self.dq_init(input)
        input = self.saturation(input)
        input = self.ipc(input)

        # apply superbias subtraction to all except MIRI data
        if input.meta.instrument.name != 'MIRI':
            input = self.superbias(input)

        # apply reference pixel correction
        input = self.refpix(input)

        # apply reset and lastframe corrections to MIRI data
        if input.meta.instrument.name == 'MIRI':
            input = self.reset(input)
            input = self.lastframe(input)

        # apply linearity, dark, and jump steps
        input = self.linearity(input)
        self.dark_current.output_dir = self.output_dir
        input = self.dark_current(input)
        input = self.jump(input)

        # save the corrected ramp data, if requested
        if self.save_calibrated_ramp:
            self.save_model(input, 'ramp')

        # apply the ramp_fit step
        self.ramp_fit.output_dir = self.output_dir
        input = self.ramp_fit(input)

        # setup output_file for saving
        self.setup_output(input)

        log.info('... ending calwebb_sloper')

        return input


    def setup_output(self, input):

        # This routine doesn't actually save the final result to a file,
        # but just sets up the value of self.output_file appropriately.
        # The final data model is passed back up to the caller, which can be
        # either an interactive session or a command-line instance of stpipe.
        # If it's an interactive session, the data model is simply returned to
        # the user without saving to a file. If it's a command-line instance
        # of stpipe, stpipe will save the data model to a file using the name
        # given in self.output_file.

        # first determine the proper file name suffix to use later
        if input.meta.cal_step.ramp_fit == 'COMPLETE':
            suffix = 'rate'
        else:
            suffix = 'ramp'

        # Has an output file name already been set?
        if self.output_file is not None:

            # Check to see if the output_file name is the default set by
            # stpipe for command-line processing
            root, ext = os.path.splitext(self.output_file)
            if root[root.rfind('_')+1:] == 'SloperPipeline':

                # Remove the step name that stpipe appended to the file name,
                # as well as the original suffix on the input file name,
                # and create a new name with the appropriate output suffix
                root = root[:root.rfind('_')]
                self.output_file = root[:root.rfind('_')+1] + suffix + ext

        # If no output name was set, take no action
            
