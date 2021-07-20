==================================
Developer Install - Windows 
==================================

.. contents::


1. Miniconda installation
-------------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

2. Create virtual environment and activate it
---------------------------------------------

.. code:: shell

    conda create --name weatherdata python=3.8 -c conda-forge -y
    conda activate weatherdata


3. Install dependencies with conda
----------------------------------

.. code:: shell

    conda install -c conda-forge pandas numpy xarray 
    
    git clone https://github.com/H2020-IPM-openalea/agroservices.git
    cd agroservices ; python setup.py install


1. Install the weatherdata package
-----------------------------------

.. code:: shell

    git clone https://github.com/H2020-IPM-openalea/weatherdata.git
    cd strawberry; python setup.py install; cd ..

5. Optional packages
---------------------

.. code:: shell

    conda install -c conda-forge pytest sphinx nbsphinx nbsphin-link nbsphinx_rtd_theme