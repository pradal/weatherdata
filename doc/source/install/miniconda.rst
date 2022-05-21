=================================================
Installation with Miniconda (Windows, linux, OSX)
=================================================

0. Install Miniconda
--------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

1. Install conda-build if not already installed
-----------------------------------------------

.. code:: shell

    conda install conda-build

2. Create virtual environment and activate it
---------------------------------------------

.. code:: shell

    conda create --name weatherdata -c openalea3 -c conda-forge weatherdata  xarray python
    source activate weatherdata

1. Build and install weatherdata package
------------------------------------------------

(Optional) Install several package managing tools :

.. code:: shell

    conda install -c conda-forge  notebook pytest sphinx sphinx_rtd_theme 