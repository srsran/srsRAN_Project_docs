If srsRAN Project has been installed using ``sudo make install`` or installed from packages then you will be able to run srsDU from anywhere on your machine. 

If you built srsRAN Project from source and have not installed it, then you can run srsDU from: ``/srsRAN_Project/build/apps/du``. In this folder you will find the srsDU application binary. 

Run srsDU as follows, passing the YAML configuration file:  

.. code-block:: bash

   sudo ./srsDU -c du.yml
   
Run srsDU with ``sudo`` to ensure threads are configured with the correct priority. 

Example configuration files can be found in the ``configs/`` folder in the srsRAN Project codebase. For more information on the configuration files and the available parameters see the :ref:`configuration reference <manual_config_ref>`.

When running, srsDU should generate the following console output:

.. code-block:: bash

   Cell pci=1, bw=20 MHz, 1T1R, dl_arfcn=650000 (n78), dl_freq=3750.0 MHz, dl_ssb_arfcn=649632, ul_freq=3750.0 MHz

   Available radio types: uhd and zmq.
   [INFO] [UHD] linux; GNU C++ version 9.3.0; Boost_107100; UHD_4.0.0.0-666-g676c3a37
   [INFO] [LOGGING] Fastpath logging disabled at runtime.
   Making USRP object with args 'type=b200,num_recv_frames=64,num_send_frames=64'
   [INFO] [B200] Detected Device: B210
   [INFO] [B200] Operating over USB 3.
   [INFO] [B200] Initialize CODEC control...
   [INFO] [B200] Initialize Radio control...
   [INFO] [B200] Performing register loopback test...
   [INFO] [B200] Register loopback test passed
   [INFO] [B200] Performing register loopback test...
   [INFO] [B200] Register loopback test passed
   [INFO] [B200] Setting master clock rate selection to 'automatic'.
   [INFO] [B200] Asking for clock rate 16.000000 MHz...
   [INFO] [B200] Actually got clock rate 16.000000 MHz.
   [INFO] [MULTI_USRP] Setting master clock rate selection to 'manual'.
   [INFO] [B200] Asking for clock rate 23.040000 MHz...
   [INFO] [B200] Actually got clock rate 23.040000 MHz.
   F1-C: Connection to CU-CP on 127.0.10.1:38471 completed

   ==== DU started ===
   Type <h> to view help   

Entering ``t`` will enable the console trace, see :ref:`here <manual_console_ref>` for more details. 

Configuration parameters can also be passed on the command line. To see the list of options, use: 

.. code-block:: bash

   ./srsdu --help