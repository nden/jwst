# The jwst.datamodels submodule was moved to stdatamodels.jwst.datamodels
# https://github.com/spacetelescope/jwst/pull/7439

import importlib
from inspect import ismodule
import sys

from stdatamodels.jwst.datamodels.util import open

from .container import ModelContainer
from .source_container import SourceModelContainer

import stdatamodels.jwst.datamodels

# Import everything defined in stdatamodels.jwst.datamodels.__all__
from stdatamodels.jwst.datamodels import * # noqa: F403

# Define __all__ to include stdatamodels.jwst.datamodels.__all__
__all__ = [
    'open',
    'ModelContainer', 'SourceModelContainer',
] + stdatamodels.jwst.datamodels.__all__


# Modules that are not part of stdatamodels
_jwst_modules = ["container", "source_container"]

# Models that are not part of stdatamodels
_jwst_models = ["ModelContainer", "SourceModelContainer"]

# Deprecated modules in stdatamodels
_deprecated_modules = ['drizproduct', 'multiprod', 'schema']

# Deprecated models in stdatamodels
_deprecated_models = ['DrizProductModel', 'MultiProductModel', 'MIRIRampModel']

# Import all submodules from stdatamodels.jwst.datamodels
for attr in dir(stdatamodels.jwst.datamodels):
    if attr[0] == '_':
        continue
    if attr in _jwst_models or attr in _deprecated_modules or attr in _deprecated_models:
        continue
    obj = getattr(stdatamodels.jwst.datamodels, attr)
    if ismodule(obj):
        # Make the submodule available locally
        locals()[attr] = obj
        # Add the submodule to sys.modules so that a call
        # to jwst.datamodels.dqflags will return the submodule
        # stdatamodels.jwst.datamodels.dqflags
        sys.modules[f"jwst.datamodels.{attr}"] = obj

# Add a few submodules to sys.modules without exposing them locally
for _submodule_name in ['schema_editor', 'validate']:
    _submodule = importlib.import_module(f"stdatamodels.jwst.datamodels.{_submodule_name}")
    sys.modules[f"jwst.datamodels.{_submodule_name}"] = _submodule


def asn_to_source_containers(asn_file, save_output=True):
    import os
    from collections import defaultdict

    MULTISOURCE_MODELS = ['MultiSlitModel']

    input_models = open(asn_file)
    # Immediately update the ASNTABLE keyword value in all inputs,
    # # so that all outputs get the new value
    for model in input_models:
        model.meta.asn.table_name = os.path.basename(input_models.asn_table_name)
    exptype = input_models[0].meta.exposure.type
    model_type = input_models[0].meta.model_type
    output_file = input_models.meta.asn_table.products[0].name
    output_file_base = output_file
    # Find all the member types in the product
    members_by_type = defaultdict(list)
    product = input_models.meta.asn_table.products[0].instance
    for member in product['members']:
        members_by_type[member['exptype'].lower()].append(member['expname'])

    # There are modes in which the exposures contain data
    # from multiple sources. In that case, the data must be
    # rearranged, collecting the exposures representing each
    # source into its own ModelContainer. This produces a list of
    # sources, each represented by a MultiExposureModel instead of
    # a single ModelContainer.
    ## sources = [source_models]
    if model_type in MULTISOURCE_MODELS:
        #self.log.info
        print('Convert from exposure-based to source-based data.')
        sources = exposure_to_source(input_models)
        source_container_output(sources, output_file_base, save_output=save_output)


def source_container_output(sources, output_file_base, save_output=True):
    from jwst.associations.lib.rules_level3_base import format_product

    for source in sources:

        # If each source is a SourceModelContainer,
        # the output name needs to be updated with the source ID, and potentially
        # also the slit name (for NIRSpec fixed-slit only).
        if isinstance(source, tuple):
            source_id, result = source
            if result[0].meta.exposure.type == "NRS_FIXEDSLIT":
                slit_name = create_nrsfs_slit_name(result)
                output_file = format_product(
                    output_file_base, source_id=source_id.lower(), slit_name=slit_name)
            else:
                output_file = format_product(
                    output_file_base, source_id=source_id.lower())
        else:
            result = source

        # The MultiExposureModel is a required output.
        if isinstance(result, SourceModelContainer) and save_output:
            #save_model(result, 'cal')
            save_model(result, output_file, 'cal', 'fits')


def save_model(model, output_file, suffix="cal", format="fits"):
    output_file = f"{output_file}_{suffix}.{format}"
    print(f"Saving output file {output_file}")
    model.save(output_file)


def exposure_to_source(source_models):
    """Convert from exposure-based to source-based data."""

    # import logging
    # log = logging.log('exp_to_source')
    import numpy as np
    from jwst.exp_to_source import multislit_to_container


    sources = [
        (name, model)
        for name, model in multislit_to_container(source_models).items()
    ]

    # Check for negative and large source_id values
    if len(sources) > 99999:
        #log.critical
        print("Data contain more than 100,000 sources;"
                          "filename does not support 6 digit source ids.")
        raise Exception

    available_src_ids = set(np.arange(99999) + 1)
    used_src_ids = set()
    for src in sources:
        src_id, model = src
        src_id = int(src_id)
        used_src_ids.add(src_id)
        if 0 < src_id <= 99999:
            available_src_ids.remove(src_id)

    hotfixed_sources = []
    # now find and reset bad source_id values
    for src in sources:
        src_id, model = src
        src_id = int(src_id)
        # Replace ids that aren't positive 5-digit integers
        if src_id < 0 or src_id > 99999:
            src_id_new = available_src_ids.pop()
            #log.info
            print(f"Source ID {src_id} falls outside allowed range.")
            #log.info
            print(f"Reassigning {src_id} to {str(src_id_new).zfill(5)}.")
            # Replace source_id for each model in the SourceModelContainers
            for contained_model in model:
                contained_model.source_id = src_id_new
            src_id = src_id_new
        hotfixed_sources.append((str(src_id), model))

    sources = hotfixed_sources
    return sources


def create_nrsfs_slit_name(source_models):
    """Create the complete slit_name product field for NIRSpec fixed-slit products

    Each unique value of slit name within the list of input source models
    is appended to the final slit name string.
    """

    slit_names = []
    slit_names.append(source_models[0].name.lower())
    for i in range(len(source_models)):
        name = source_models[i].name.lower()
        if name not in slit_names:
            slit_names.append(name)
    slit_name = "-".join(slit_names)  # append slit names using a dash separator

    return slit_name
