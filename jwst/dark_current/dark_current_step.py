from jwst.stpipe import Step
from jwst import datamodels
from . import dark_sub


class DarkCurrentStep(Step):
    """
    DarkCurrentStep: Performs dark current correction by subtracting
    dark current reference data from the input science data model.
    """

    spec = """
        dark_output = output_file(default = None)
    """

    reference_file_types = ['dark']

    def process(self, input):

        # Open the input data model
        with models.open(input) as input_model:

            # Get the name of the dark reference file to use
            self.dark_name = self.get_reference_file(input_model, 'dark')
            self.log.info('Using DARK reference file %s', self.dark_name)

            # Check for a valid reference file
            if self.dark_name == 'N/A':
                self.log.warning('No DARK reference file found')
                self.log.warning('Dark current step will be skipped')
                result = input_model.copy()
                result.meta.cal_step.dark = 'SKIPPED'
                return result

            # Open the dark ref file data model
            dark_model = models.DarkModel(self.dark_name)

            # Do the dark correction
            result = dark_sub.do_correction(input_model, dark_model,
                                            self.dark_output)

            dark_model.close()

        return result

