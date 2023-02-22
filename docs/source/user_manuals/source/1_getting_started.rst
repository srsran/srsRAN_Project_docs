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

Users can read about downloading and configuring Open5GS :ref:`here <https://github.com/open5gs/open5gs>`_. We suggest you do this before trying to run the gNB. 

Configuring the gNB
*******************

As discussed in detail in the :ref:`configuration reference <config_ref>` section of the documentation, the gNB can be configured via the command line or via a custom config file, 

They key things to configure for a base implementation are: 

    - The AMF address of the core
    - The correct RF-device parameters for the frontend you are using 

These parameters will be unique to each set-up.

We suggest users use a configuration file when running the gNB, as it is both easier to edit and debug. 

Running the gNB
***************

To run the gNB navigate to */srsRAN_Project/build/apps/gnb*. In this folder you will find the gNB application binary. This can be run with the following command: 

.. code-block:: bash

   sudo ./gnb

This will run the gNB in its default state. To run the gNB with a user defined configuration file use: 

.. code-block:: bash

   sudo ./gnb -c [PATH TO CONFIG FILE]

.. note::
   Users should always run the gNB with sudo, this ensures threads are configured with the correct priority.

Performance Tuning
******************

The following sections outline some of the key things to do to increase performance of the gNB. 

Performance Mode
================

The CPU governor of the PC should be set to performance mode to allow for maximum compute power and throughput. This can be configured for e.g. Ubuntu using:

.. code-block:: bash

   echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

It is also recommended that users running on a laptop keep the PC connected to a power-source at all times while running the gNB, as this will avoid performance loss due to CPU frequency scaling on the machine.


Example Applications
********************


