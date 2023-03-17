.. _manual_running:

Running srsRAN Project
######################

Baseline Requirements
*********************

To successfully run the srsRAN Project gNB you will need the following: 

    - A PC with a Linux based OS (Ubuntu 20.04 or later)
    - A USRP device
    - srsRAN Project (see the :ref:`Installation Guide <manual_installation_build>`)
    - A 3rd-party 5G core (we recommend `Open5GS <https://github.com/open5gs/open5gs>`_)
    - A 3rd-party 5G UE

Recommended: 

    - External clock source 

If you plan to connect the gNB to a COTS UE we recommend that you use an external clock source such as an Octoclock or GPSDO that is compatible with your RF-frontend, as the on-board clock within the USRP may not be accurate enough to enable a connection with the UE.
This is discussed further in the relevant app note. 

----

System Preparation
******************

Before running the gNB application, we recommend tuning your system for best performance. We provide a script to configure known performance parameters:

   - `srsran_performance <https://github.com/srsran/srsRAN_Project/tree/main/scripts/srsran_performance>`_
   

The script does the following: 

   1. Sets the scaling governor to performance
   2. Disables DRM KMS polling
   3. Tunes network buffers (Ethernet based USRPs only)
   
Run the script as follows from the main project folder:

.. code-block:: bash

   sudo ./scripts/srsran_performance

----

Running the gNB
***************

| If the gNB has been installed using ``sudo make install`` or installed from packages then you will be able to run the gNB from anywhere on your machine. 
| If you built the gNB from source and have not installed it, then you can run the gNB from: ``/srsRAN_Project/build/apps/gnb``. In this folder you will find the gNB application binary. 

Run the gNB as follows, passing the YAML configuration file:  

.. code-block:: bash

   sudo gnb -c gnb_rf_b200_tdd_n78_10mhz.yml
   
| Run the gNB with sudo to ensure threads are configured with the correct priority. 
| Run the gNB with an explicit configuration file. See the :ref:`configuration reference <manual_config_ref>` for more details.
| Example configuration files can be found in the ``configs/`` folder in the srsRAN Project codebase.

When running, the gNB should generate the following console output:

.. code-block:: bash

   Available radio types: uhd.

   --== srsRAN gNB (commit 77be7d339) ==--

   [INFO] [UHD] linux; GNU C++ version 9.4.0; Boost_107100; UHD_4.2.0.HEAD-0-g197cdc4f
   Making USRP object with args 'type=b200'
   Cell pci=1, bw=10 MHz, dl_arfcn=632628 (n78), dl_freq=3489.42 MHz, dl_ssb_arfcn=632640, ul_freq=3489.42 MHz

   ==== gNodeB started ===
   Type <t> to view trace

Entering ``t`` will enable the console trace, see :ref:`here <manual_console_ref>` for more details. 

Configuration parameters can also be passed on the command line. To see the list of options, use: 

.. code-block:: bash

   ./gnb --help
