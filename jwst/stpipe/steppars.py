"""Step parameters model"""
from copy import copy
from asdf.extension import Converter
#from .model_base import JwstDataModel


__all__ = ['StepParsModel']


DEFAULT_META = {
    'date': 'SPECIFY DATE',
    'origin': 'STScI',
    'telescope': 'JWST',
    'reftype': 'pars-step',
    'pedigree': 'SPECIFY PEDIGREE',
    'description': 'Parameters for calibration step SPECIFY',
    'author': 'SPECIFY AUTHOR',
    'useafter': 'SPECIFY',
    'instrument': {
        'name': 'SPECIFY',
    },
}


class StepParsModel:
    """
    An ASDF model for `Step` parameters.
    """

    # def __init__(self, init=None, **kwargs):
    #     super().__init__(init=init, **kwargs)
    #     meta = copy(DEFAULT_META)
    #     meta.update(self.meta.instance)
    #     self.meta.instance.update(meta)

    def __init__(self, meta, parameters):
        self.meta = copy(DEFAULT_META)
        self.meta.update(model.meta)
        self.parameters = parameters


class StepParsConverter(Converter):

    tags = ["tag:stsci.edu:stpie/step_pars-*"]

    types = ["StepParsModel"]

    def to_yaml_tree(self, model, tag, ctx):
        return {'meta': model.meta,
                'parameters': model.parameters
                }

    def from_yaml_tree(self, node, tag, ctx):
        return StepParsModel(node['meta'], node['parameters'])
