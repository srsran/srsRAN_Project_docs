.. _getting_started:

Getting Started
###############

Baseline Hardware Requirements
******************************

To successfully run an end-to-end system using the srsRAN Project gNB you will need the following: 

    - A PC with a Linux based OS (Ubuntu 20.04 or later)
    - Required Dependencies (see :ref:`here <dependencies>`)
    - A USRP and UHD installed on your machine
    - srsRAN built and installed (see :ref:`here <build>`)
    - A 3rd-party 5G core (we recommend `Open5GS <https://github.com/open5gs/open5gs>`_)
    - A 3rd-party 5G UE or COTS 5G UE

Recommended: 

    - External clock source 

If you plan to connect the gNB to a COTS UE we recommend that you use an external clock source such as an Octoclock of GPSDO that is compatible with your RF-frontend, as the on-board clock within the USRP is not accurate enough to enable a connection with the UE.
This is discussed further in the relevant app note. 

----

Running the gNB
***************

If the gNB has been installed using ``sudo make install`` or installed from packages then you will be able to run the gNB from anywhere on your machine. If you built the gNB from source and have not installed it, then you can run the 
gNB from: ``/srsRAN_Project/build/apps/gnb``. In this folder you will find the gNB application binary. 

It is recommended that users **always** run the gNB using a configuration file. The following is a list of recommended parameters that should always be configured: 

    - The AMF parameters
    - The RF-device being used
    - The cell configuration
    - Log levels

An example configuration file may look like the following: 

.. literalinclude:: .config/gnb_rf_b200_tdd_n78_10mhz.yml  
    :language: yaml

This configuration file configures the gNB to run using a B200 as the RF-frontend, with a TDD cell transmitting with 10 MHZ bandwdith in band 78, an external GPSDO clock source is also set to ensure an accurate clock. This file also configures the log files and the PCAPs.

Assuming that the gNB has been built from source, and installed, the gNB can be run with the following commands from the folder containing the configuration file:  

.. code-block:: bash

   sudo gnb -c gnb_rf_b200_tdd_n78_10mhz.yml

.. tip::
   Users should always run the gNB with sudo, this ensures threads are configured with the correct priority.

After running the gNB users can expect to see the following: 

.. code-block:: bash

   Available radio types: uhd.

   --== srsRAN gNB (commit 77be7d339) ==--

   [INFO] [UHD] linux; GNU C++ version 9.4.0; Boost_107100; UHD_4.2.0.HEAD-0-g197cdc4f
   Making USRP object with args 'type=b200'
   Cell pci=1, bw=10 MHz, dl_arfcn=632628 (n78), dl_freq=3489.42 MHz, dl_ssb_arfcn=632640, ul_freq=3489.42 MHz

   ==== gNodeB started ===
   Type <t> to view trace

When the gNB is running, pressing ``t`` will enable to console trace, see :ref:`here <console_ref>` for a breakdown on what the trace shows. 

The example configuration files can be found in the ``configs/`` folder in the srsRAN Project codebase. The configuration options are discussed further :ref:`here <config_ref>`.

There is an option to run the gNB using command line arguments to change the configuration of the gNB. Although, this is not the recommended way to configure the gNB. To see the list of options for running from command line, use the following command: 

.. code-block:: bash

   ./gnb --help

----

Performance Tuning
******************

The following sections outline some of the key things to do to increase performance of the gNB. 

Performance Mode
================

The CPU governor of the PC should be set to performance mode to allow for maximum compute power and throughput. This can be configured for e.g. Ubuntu using:

.. code-block:: bash

   echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

It is also recommended that users running on a laptop keep the PC connected to a power-source at all times while running the gNB, as this will avoid performance loss due to CPU frequency scaling on the machine.

Configuring USRP
================

Users should always ensure that the USRP they are using is running over USB 3.0 and correctly configured. If UHD is built from source, users will have multiple example applications available in ``/usr/lib/uhd/examples/``. User can verify their USRP 
is correctly configured by running the ``uhd_benchmark`` application.

Use the following command to  this: 

.. code-block:: bash

   sudo ./benchmark_rate --rx_rate [rate in Hz] --tx_rate [rate in Hz]

More on this can be found in `this <https://kb.ettus.com/Verifying_the_Operation_of_the_USRP_Using_UHD_and_GNU_Radio>`_ guide on the `Ettus Knowledge Base <https://kb.ettus.com/Knowledge_Base>`. 