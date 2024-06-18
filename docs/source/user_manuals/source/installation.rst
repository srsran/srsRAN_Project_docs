.. _manual_installation:

Installation Guide
##################

The following steps need to be taken in order to download and build the srsRAN Project:

    1. Install dependencies
    2. Install RF driver (only required for Split 8 deployments)
    3. Clone the repository
    4. Build the codebase

----


.. _manual_installation_dependencies: 

Build Tools and Dependencies
****************************

The srsRAN Project uses CMake and C++17. We recommend the following build tools:

    - `cmake <https://cmake.org/>`_
    - `gcc <https://gcc.gnu.org/>`_ (v9.4.0 or later) **OR** `Clang <https://clang.llvm.org/>`_ (v10.0.0 or later)

The srsRAN Project has the following necessary dependencies: 

    - `libfftw <https://www.fftw.org/>`_
    - `libsctp <https://github.com/sctp/lksctp-tools>`_
    - `yaml-cpp <https://github.com/jbeder/yaml-cpp>`_
    - `mbedTLS <https://www.trustedfirmware.org/projects/mbed-tls/>`_
    - `googletest <https://github.com/google/googletest/>`_

You can install the required build tools and dependencies for various distributions as follows: 

.. tabs::

    .. tab:: Ubuntu 22.04

        .. code-block:: bash

            sudo apt-get install cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev

    .. tab:: Fedora

        .. code-block:: bash

            sudo yum install cmake make gcc gcc-c++ fftw-devel lksctp-tools-devel yaml-cpp-devel mbedtls-devel gtest-devel

    .. tab:: Arch Linux

        .. code-block:: bash

            sudo pacman -S cmake make base-devel fftw mbedtls yaml-cpp lksctp-tools gtest

It is also recommended users install the following (although they are not required): 

    - `Ccache <https://ccache.dev/>`_: This will help to speed up re-compilation
    - `backward-cpp <https://github.com/bombela/backward-cpp>`_: This library helps to generate more informative backtraces in the stdout if an error occurs during runtime  

----


RF-drivers
**********

.. note:: 

    UHD and/or ZMQ are only required for Split 8 deployments, if you are planning on using a Split 7.2 deployment you may skip this step. 

The srsRAN Project uses RF drivers to support different radio types. Currently, only UHD and ZMQ are supported:

.. _Drivers:

  * `UHD <https://github.com/EttusResearch/uhd>`_ (We recommended the LTS version of UHD, i.e. either 3.15 or 4.0.)
  * `ZMQ <https://zeromq.org/>`_

----

.. _manual_installation_build: 

Clone and Build
***************

.. tabs:: 

   .. tab:: Vanilla Installation 

      .. include:: installation_vanilla.rst

   .. tab:: ZMQ Enabled Installation   

      .. include:: installation_zmq.rst 

The :ref:`Running srsRAN Project <manual_running>` section of the documentation further discusses how to configure and run the gNB application. 

----

Packages
********

srsRAN Project is available to download directly from packages for various linux distributions. Users looking for a simple installation who do not wish to edit the source code should use the package installation.

.. tabs:: 

    .. tab:: Ubuntu 

        Ubuntu users can download the srsRAN Project packages using the following commands: 

        .. code-block:: bash

            sudo add-apt-repository ppa:softwareradiosystems/srsran-project
            sudo apt-get update
            sudo apt-get install srsran-project -y

    .. tab:: Arch Linux

        Arch Linux users can download the srsRAN Project packages using an AUR helper, e.g. 'yay', using the following command: 

        .. code-block:: bash

            yay -Sy srsran-project-git

This will build and install the latest version of srsRAN Project from git. 

When installed from packages, srsRAN Project example configs can be found in ``/usr/share/srsran``. For info on these config files, see :ref:`here <manual_config_ref>`

The application can then be run using: 

.. code-block:: bash

   sudo gnb -c <config file>

---- 

PHY testvectors 
***************

A number of PHY tests are based on MATLAB generated testvectors. By default, those tests are disabled.
The following steps are required to enable them:

1. Download the `PHY testvector set <https://github.com/srsran/srsRAN_Project/releases>`_.
2. Copy the PHY testvectors to its location within srsRAN:

.. code-block:: bash

    tar -xzf phy_testvectors.tar.gz -C /path_to_your_local_repository/srsgnb/

3. Enable the use of PHY testvectors by modifying the root CMakeLists.txt as shown below:

.. code-block:: bash

    option(USE_PHY_TESTVECTORS   "Enable testvector PHY tests"              ON)

4. Rebuild srsRAN Project. 


