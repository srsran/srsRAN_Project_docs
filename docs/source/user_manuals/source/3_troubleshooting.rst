.. _manual_troubleshooting: 

Troubleshooting
###############

For support and help using srsRAN Project, check out the community driven `discussion forum <https://github.com/srsran/srsRAN_Project/discussions>`_.

Performance Tuning
******************

The following sections outline key steps to improve gNB performance. 

Performance Mode
================

The CPU governor of the PC should be set to performance mode to allow for maximum compute power and throughput. This can be configured for e.g. Ubuntu using:

.. code-block:: bash

   echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

It is also recommended that users running on a laptop keep the PC connected to a power-source at all times while running the gNB, as this will avoid performance loss due to CPU frequency scaling on the machine.

Configuring USRP
================

Users should always ensure that the USRP they are using is running over USB 3.0 or ethernet and correctly configured. If UHD is built from source, users will have multiple example applications available in ``/usr/lib/uhd/examples/``. User can verify their USRP is correctly configured by running the ``uhd_benchmark`` application as follows:

.. code-block:: bash

   sudo ./benchmark_rate --rx_rate [rate in Hz] --tx_rate [rate in Hz]

More details can be found in `this <https://kb.ettus.com/Verifying_the_Operation_of_the_USRP_Using_UHD_and_GNU_Radio>`_ guide on the `Ettus Knowledge Base <https://kb.ettus.com/Knowledge_Base>`_. 
