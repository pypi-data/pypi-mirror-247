# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sequana_pipelines', 'sequana_pipelines.revcomp']

package_data = \
{'': ['*']}

install_requires = \
['click-completion>=0.5.2,<0.6.0',
 'click>=8.1.7,<9.0.0',
 'rich-click>=1.7.2,<2.0.0',
 'sequana>=0.16.4',
 'sequana_pipetools>=0.16.6']

entry_points = \
{'console_scripts': ['sequana_revcomp = sequana_pipelines.revcomp.main:main']}

setup_kwargs = {
    'name': 'sequana-revcomp',
    'version': '1.1.0',
    'description': 'reverse complement a set of FastQ files',
    'long_description': "\n.. image:: https://badge.fury.io/py/sequana-revcomp.svg\n     :target: https://pypi.python.org/pypi/sequana_revcomp\n\n.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg\n    :target: http://joss.theoj.org/papers/10.21105/joss.00352\n    :alt: JOSS (journal of open source software) DOI\n\n.. image:: https://github.com/sequana/revcomp/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/sequana/revcomp/actions/workflows\n\n\n.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C3.10-blue.svg\n    :target: https://pypi.python.org/pypi/sequana\n    :alt: Python 3.8 | 3.9 | 3.10\n\nThis is is the **revcomp** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet\n\n:Overview: revert and complement input Fast files\n:Input: A set of FastQ files (paired or single-end) compressed or not\n:Output: A set of reverse completed files\n:Status: production\n:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352\n\n\n\n\nInstallation\n~~~~~~~~~~~~\n\nIf you already have all requirements, you can install the packages using pip::\n\n    pip install sequana_revcomp --upgrade\n\nUsage\n~~~~~\n\nThis command will scan all files ending in .fastq.gz found in the local\ndirectory, create a directory called revcomp where a snakemake pipeline can be executed.::\n\n::\n\n    sequana_revcomp --input-directory DATAPATH\n\nThis creates a directory with the pipeline and configuration file. You will then need\nto execute the pipeline::\n\n    cd revcomp\n    sh revcomp.sh  # for a local run\n    make clean\n\nThis launch a snakemake pipeline. If you are familiar with snakemake, you can\nretrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::\n\n    snakemake -s revcomp.rules -c config.yaml --cores 4 \\\n        --wrapper-prefix https://raw.githubusercontent.com/sequana/sequana-wrappers/\n\nOr use `sequanix <https://sequana.readthedocs.io/en/main/sequanix.html>`_ interface.\n\nRequirements\n~~~~~~~~~~~~\n\nThis pipelines requires the following executable(s):\n\n- seqtk\n\n\nDetails\n~~~~~~~~~\n\nThis pipeline runs **seqtk** in parallel on the input fastq files.\n\n\nRules and configuration details\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nHere is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_revcomp/main/sequana_pipelines/revcomp/config.yaml>`_\nto be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file.\n\n\nChangelog\n~~~~~~~~~\n\n========= ======================================================================\nVersion   Description\n========= ======================================================================\n0.9.0     * set singularity container\n0.8.4     * implemented --from-project option\n0.8.3     * Uses new sequana framework to spee up --help calls\n          * --threads option\n0.8.2     Fix schema and rule. output files are now saved in the ./rc directory\n0.8.1     Improve the --help message\n0.8.0     First version from sequana 0.8.0\n========= ======================================================================\n\n\nContribute & Code of Conduct\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTo contribute to this project, please take a look at the\n`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a\n`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.\n",
    'author': 'Sequana Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sequana/revcomp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
