If |project_name| has been installed using ``sudo make install`` or installed from packages then you will be able to run the gNB from anywhere on your machine. 

If you have built |project_name| from source and have not installed it, then you can run the gNB from: ``/srsRAN_Project/build/apps/gnb``. In this folder you will find the gNB application binary. 

Run the gNB as follows, passing the YAML configuration file:  

.. code-block:: bash

   sudo ./gnb -c gnb_rf_b200_tdd_n78_10mhz.yml
   
Run the gNB with ``sudo`` to ensure threads are configured with the correct priority. 

Example configuration files can be found in the ``configs/`` folder in |project_name| codebase. For more information on the configuration files and the available parameters see the :ref:`configuration reference <manual_config_ref>`.

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