from asdf.extension import ManifestExtension, Converter
#from .stpars import WfiImageConverter, ExposureConverter, WfiConverter


STEPPARS_CONVERTERS = [
    StepParsConverter(),
]

STEPAPARS_EXTENSIONS = [
    ManifestExtension.from_uri("http://stsci.edu/asdf/extensions/stpipe/manifests/stpipe-1.0", 
    	converters=STPARS_CONVERTERS)
]


class StepParsConverter(Converter):
    types = ["StepPars"]
    tags = ["tag:stsci.edu:stpipe/step_pars-1.0.0"]

    def to_yaml_tree(self, obj, tags, ctx):
        return obj.meta

    def from_yaml_tree(self, node, tag, ctx):
        return StepPars(**node["meta"])


class StepPars:
    def __init__(self, init=None, **kwargs):
        super().__init__()
        self.meta = None
        if isinstance(init, str):
            # What is init in this case?
            # - asdf file
            # dict 
            # COuld it be a StepPars object?
            self.meta = self.from_file(init)
    
