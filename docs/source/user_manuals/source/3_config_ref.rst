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

   sudo ./gnb [OPTIONS] [SUBCOMMAND]

Each of these options and subcommands can be set in a configuration file, or passed as an argument when running the gNB as shown above. 

To see a full list of the configurable parameters use the following command: 

.. code-block:: bash

   ./gnb --help

Configuration File
******************

The gNB takes a yaml type configuration file (.yml). From which users can easily configure each of the available parameters of the gNB.

To run the gNB with a config file, the following command can be used: 

.. code-block:: bash

   sudo ./gnb -c [PATH TO FILE]
