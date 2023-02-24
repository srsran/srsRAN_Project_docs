.. _installation:

Installation Guide
##################

The following steps need to be taken in order to download and build the srsRAN Project gNB:

    1. Install all necessary dependencies
    2. Install RF driver
    3. Clone the repository
    4. Build the codebase

----

Requirements
************

Before installing srsRAN Project, users will first need to download the necessary dependencies and RF drivers. The gNB currently **only** supports the use of UHD or ZeroMQ.

User running on Ubuntu require Ubuntu 20.04 or later, we recommend 22.04. 

.. _dependencies: 

Dependencies
============

srsRAN Project has the following necessary dependencies: 

    - `cmake <https://cmake.org/>`_
    - `libfftw <https://www.fftw.org/>`_
    - `libsctp <https://github.com/sctp/lksctp-tools>`_
    - `yaml-cpp <https://github.com/jbeder/yaml-cpp>`_
    - `PolarSSL/mbedTLS <https://www.trustedfirmware.org/projects/mbed-tls/>`_
    - `googletest <https://github.com/google/googletest/>`_
    - `gcc <https://gcc.gnu.org/>`_ (v9.4.0 or later) **OR** `Clang <https://clang.llvm.org/>`_ (v10.0.0 or later)

You can install the required libraries with the commands below for various distributions: 

Ubuntu 22.04:

.. code-block:: bash

    sudo apt-get install cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev

Fedora:

.. code-block:: bash

    sudo yum install cmake make gcc gcc-c++ fftw-devel lksctp-tools-devel yaml-cpp-devel mbedtls-devel gtest-devel

Arch Linux:

.. code-block:: bash

    sudo pacman -S cmake make base-devel fftw mbedtls yaml-cpp lksctp-tools gtest

RF-drivers
==========
You must ensure that the correct drivers are installed prior to building and running srsRAN Project. The following drivers are supported: 

.. _Drivers:

  * `UHD <https://github.com/EttusResearch/uhd>`_ 
  * `ZeroMQ <https://github.com/zeromq>`_

.. note::
	We recommended the LTS version of UHD, i.e. either 3.15 or 4.0.

----

Packages
********

srsRAN Project is available to download directly from packages for various linux distributions. Users looking for a simple installation who do not wish to edit the source code should use the package installation

Arch Linux
==========

Arch Linux users can download the srsRAN Project packages using an AUR helper, e.g. 'yay', using the following command: 

.. code-block:: bash

   yay -Sy srsran-project-git

This will build and install the latest version of srsRAN Project from git. Once installed users can run the srsRAN Project gNB using: 

.. code-block:: bash

   sudo gnb -c [PATH TO CONFIG FILE]

.. tip::
   Users should always run the gNB with sudo, this ensures threads are configured with the correct priority.

When installed from packages srsRAN Project example configs can be found in ``/usr/share/srsran``. For info on these config files, see :ref:`here <config_ref>`

----

.. _build: 

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

You can now run the gNB from ``srsRAN_Project/build/apps/gnb/``. If you wish to install the srsRAN Project gNB, you can use the following command: 

.. code-block:: bash

    sudo make install

This will allow you to run the gNB from anywhere on your machine using:

.. code-block:: bash

   sudo gnb -c [PATH TO CONFIG]

.. note::
   The gNB **must** be passed a configuration file in order to run correctly.

The :ref:`Getting Started <getting_started>` section of the documentation further discusses how to configure and run the gNB application.  
