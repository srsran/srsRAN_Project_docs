.. _getting_started:

Getting Started
###############

Baseline Hardware Requirements
******************************

To successfully run an end-to-end system using the srsRAN Project gNB you will need the following: 

    - A PC with a Linux based OS WITH srsRAN Project downloaded and built
    - An RF-frontend (we recommend a USRP)
    - A 3rd-party 5G core (we recommend open5Gs)
    - A 3rd-party 5G UE

Recommended: 

    - External clock source 

If you plan to connect the gNB to a COTS UE we recommend that you use an external clock source such as an Octoclock of GPSDO that is compatible with your RF-frontend, as the on-board clock within the USRP is not accurate enough to enable a connection with the UE.
This is discussed further in the relevant app note. 

Users can read about downloading and configuring Open5GS `here <https://github.com/open5gs/open5gs>`_. We suggest you do this before trying to run the gNB. 

----

Running the gNB
***************

To run the gNB navigate to ``/srsRAN_Project/build/apps/gnb`` in this folder you will find the gNB application binary. 

The gNB must be run using either command line arguments or a user defined configuration file. THe configuration file is .yml file and is used to configure gNB parameters such as: 

    - The RF-device being used
    - The cell configuration
    - Log levels

An example command for running the gNB with command line arguments is given below:

.. code-block:: bash

   sudo ./gnb amf --addr [AMF IP] --bind_addr [LOCAL IP] rf_driver --device_driver uhd --device_args type=b200 --srate 11.52 --tx_gain 50 --rx_gain 60 common_cell --dl_arfcn 368640 --band 3 --channel_bandwidth_MHz 10 --clock gpsdo --sync gpsdo 

This example command will connect the gNB to the 5GC, using a B200 as the RF-frontend, with a FDD cell transmitting with 10 MHZ bandwdith in band 3, an external GPSDO clock source is also set to ensure an accurate clock.  

To run the gNB with a user defined configuration file use: 

.. code-block:: bash

   sudo ./gnb -c [PATH TO CONFIG FILE]

Example configuration files can be found in the ``configs/`` folder in the srsRAN Project codebase. 

.. note::
   Users should always run the gNB with sudo, this ensures threads are configured with the correct priority.

To see a full list of the configurable parameters use the following command: 

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


