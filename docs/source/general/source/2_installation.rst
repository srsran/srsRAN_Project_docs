.. _installation:

Installation Guide
##################

Requirements
************

srsRAN Project has the following necessary requirements: 

    - `cmake <https://cmake.org/>`_
    - `libfftw <https://www.fftw.org/>`_
    - `libsctp <https://github.com/sctp/lksctp-tools>`_
    - `yaml-cpp <https://github.com/jbeder/yaml-cpp>`_
    - `PolarSSL/mbedTLS <https://www.trustedfirmware.org/projects/mbed-tls/>`_
    - `googletest <https://github.com/google/googletest/>`_

You can install the required libraries for some example distributions with the commands below: 

**Ubuntu 22.04**

.. code-block:: bash

    sudo apt-get install cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev git-lfs

**Fedora**

.. code-block:: bash

    sudo yum install cmake make gcc gcc-c++ fftw-devel lksctp-tools-devel yaml-cpp-devel mbedtls-devel gtest-devel git-lfs

**Arch Linux**

.. code-block:: bash

    sudo pacman -S cmake make base-devel fftw mbedtls yaml-cpp lksctp-tools gtest git-lfs
   

Optional Requirements
*********************

If using RF-hardware you must ensure that the correct drivers are installed prior to building and running srsRAN Project. Some of the most popular drivers can be found in the following list: 

.. _Drivers:

  * `UHD <https://github.com/EttusResearch/uhd>`_ 
  * `SoapySDR <https://github.com/pothosware/SoapySDR>`_
  * `BladeRF <https://github.com/Nuand/bladeRF>`_
  * `ZeroMQ <https://github.com/zeromq>`_

.. note::
	If using UHD we recommended the LTS version of UHD, i.e. either 3.15 or 4.0.

Build from Source
*****************

First, clone the srsRAN Project repository: 

.. code-block:: bash

    git clone https://github.com/srsRAN/srsRAN_Project.git

Then build the code-base: 

.. warning::
  All mandatory requirements, optional requirements, and RF front-end drivers must be installed **prior** to building srsRAN. Failing to do this will result in
  errors at run-time or prevent srsRAN from building correctly.  

.. code-block:: bash 

    cd srsRAN_Project
    mkdir build
    cd build
    cmake ../ 
    make -j $(nproc)
    make test -j $(nproc) 

You can now run the gNB from *srsRAN_Project/build/apps/gnb/*. Here you will find the gNB binary. 

   

