
.. image:: https://badge.fury.io/py/sequana-revcomp.svg
     :target: https://pypi.python.org/pypi/sequana_revcomp

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

.. image:: https://github.com/sequana/revcomp/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/revcomp/actions/workflows


.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C3.10-blue.svg
    :target: https://pypi.python.org/pypi/sequana
    :alt: Python 3.8 | 3.9 | 3.10

This is is the **revcomp** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: revert and complement input Fast files
:Input: A set of FastQ files (paired or single-end) compressed or not
:Output: A set of reverse completed files
:Status: production
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352




Installation
~~~~~~~~~~~~

If you already have all requirements, you can install the packages using pip::

    pip install sequana_revcomp --upgrade

Usage
~~~~~

This command will scan all files ending in .fastq.gz found in the local
directory, create a directory called revcomp where a snakemake pipeline can be executed.::

::

    sequana_revcomp --input-directory DATAPATH

This creates a directory with the pipeline and configuration file. You will then need
to execute the pipeline::

    cd revcomp
    sh revcomp.sh  # for a local run
    make clean

This launch a snakemake pipeline. If you are familiar with snakemake, you can
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s revcomp.rules -c config.yaml --cores 4 \
        --wrapper-prefix https://raw.githubusercontent.com/sequana/sequana-wrappers/

Or use `sequanix <https://sequana.readthedocs.io/en/main/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- seqtk


Details
~~~~~~~~~

This pipeline runs **seqtk** in parallel on the input fastq files.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_revcomp/main/sequana_pipelines/revcomp/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file.


Changelog
~~~~~~~~~

========= ======================================================================
Version   Description
========= ======================================================================
0.9.0     * set singularity container
0.8.4     * implemented --from-project option
0.8.3     * Uses new sequana framework to spee up --help calls
          * --threads option
0.8.2     Fix schema and rule. output files are now saved in the ./rc directory
0.8.1     Improve the --help message
0.8.0     First version from sequana 0.8.0
========= ======================================================================


Contribute & Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To contribute to this project, please take a look at the
`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.
