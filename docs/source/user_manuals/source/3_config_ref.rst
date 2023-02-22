.. _config_ref: 

Configuration Reference
#######################

The srsRAN Project gNB can be configured in two ways: 

    - Parameters can be changed via command line arguments when starting up the gNB
    - Users can run the gNB with a custom configuration file

The srsRAN Project gNB uses a yaml configuration file. This file can be created and customized by users as needed, and comes with a vast array of configuration options to suit all use-cases. 

Configuration Options
*********************

The gNB application can be run with the following arguments: 

.. code-block:: bash 

   sudo gnb [OPTIONS] [SUBCOMMAND]

Each of these options and subcommands can be set in a configuration file, or passed as an argument when running the gNB as shown above. 

The following example shows how to configure the gNB to use a B200 USRP and enable logs from the command line:

.. code-block:: bash 

   sudo gnb rf_driver --device_driver uhd --device_args type=b200 --srate 11.52 --tx_gain 50 --rx_gain 60 common_cell --channel_bandwidth_MHz 10 --clock gpsdo --sync gpsdo 

Configuration File
******************

The gNB takes a yaml type configuration file (.yml). From which users can easily configure each of the available parameters of the gNB.

To run the gNB with a config file, the following command can be used: 

.. code-block:: bash

   sudo gnb -c [PATH TO FILE]
