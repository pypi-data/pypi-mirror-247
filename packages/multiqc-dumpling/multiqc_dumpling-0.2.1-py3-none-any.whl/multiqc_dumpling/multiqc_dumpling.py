#!/usr/bin/env python

from __future__ import print_function
from pkg_resources import get_distribution
import logging

from multiqc.utils import report, util_functions, config


# Add default config options for the things that are used in MultiQC_dumpling
def dumpling_plugin_execution_start():
    """Code to execute after the config files and
    command line flags have been parsedself.

    This setuptools hook is the earliest that will be able
    to use custom command line flags.
    """

    # Halt execution if we've disabled the plugin
    #if config.kwargs.get("disable_plugin", True):
    #    return None
    

    # Add to the main MultiQC config object.
    # User config files have already been loaded at this point
    #   so we check whether the value is already set. This is to avoid
    #   clobbering values that have been customised by users.

    counts_header = "count,pos,mutation_type,name,codon,mutation,length,hgvs"

    # Add to the search patterns used by modules

    if "dumpling/key_value_pairs" not in config.sp:
        config.update_dict(config.sp, {"dumpling/key_value_pairs": {"fn": "baseline_1.csv"}})

    if "dumpling" not in config.sp:
        # config.update_dict( config.sp, { 'dumpling': { 'fn': '*.csv' }, {'num_lines': 1}, {'contents': counts_header} } )
        config.update_dict(config.sp, {"dumpling": {"fn": "baseline_w.csv"}})

    config.update_dict(config.sp, {"dumpling": {"fn": "baseline_3.csv"}})
