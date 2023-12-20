#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import shutil
import subprocess
import sys

import click_completion
import rich_click as click
from sequana_pipetools import SequanaManager
from sequana_pipetools.options import *

NAME = "revcomp"


help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--threads",
        ],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions)
@include_options_from(ClickGeneralOptions)
@click.option("--threads", default=4, type=click.INT)
def main(**options):

    if options["from_project"]:
        click.echo("--from-project Not yet implemented")
        sys.exit(1)

    # the real stuff is here
    manager = SequanaManager(options, NAME)
    manager.setup()

    options = manager.options
    cfg = manager.config.config

    manager.fill_data_options()

    cfg.revcomp.threads = options.threads

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
